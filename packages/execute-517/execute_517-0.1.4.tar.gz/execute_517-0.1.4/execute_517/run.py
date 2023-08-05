import os
import sys
import subprocess
import tempfile
from pathlib import Path

from build import ProjectBuilder
from build.env import IsolatedEnvBuilder

__all__ = ['run_python_in_env']


# Copied from build but changing subprocess options to ouput to stderr
def silent_install(env, requirements):
    """
    Installs the specified PEP 508 requirements on the environment
    :param requirements: PEP-508 requirement specification to install
    :note: Passing non PEP 508 strings will result in undefined behavior, you *should not* rely on it. It is \
            merely an implementation detail, it may change any time without warning.
    """
    if not requirements:
        return

    with tempfile.NamedTemporaryFile('w+', prefix='build-reqs-', suffix='.txt', delete=False) as req_file:
        req_file.write(os.linesep.join(requirements))
    try:
        cmd = [
            env._pip_executable,
            # on python2 if isolation is achieved via environment variables, we need to ignore those while calling
            # host python (otherwise pip would not be available within it)
            '-{}m'.format('E' if env._pip_executable == env.executable and sys.version_info[0] == 2 else ''),
            'pip',
            'install',
            '--prefix',
            env.path,
            '--ignore-installed',
            '--no-warn-script-location',
            '-r',
            os.path.abspath(req_file.name),
        ]
        subprocess.check_call(cmd, stdout=sys.stderr)
    finally:
        os.unlink(req_file.name)


def run_python_in_env(srcdir, args, **kwargs):
    """
    Execute ``python <args>`` in path in the build environment.

    The build environment will be read from the ``srcdir/pyproject.toml`` file.

    Notes
    -----

    The ``cwd`` keyword argument to `subprocess.call` will default to
    ``srcdir`` unless passed in ``kwargs``.

    The output from the pip command installing the build dependencies is
    redirected to stderr.

    """
    srcdir = Path(srcdir).expanduser().absolute()
    builder = ProjectBuilder(srcdir)

    cwd = kwargs.pop("cwd", srcdir)

    with IsolatedEnvBuilder() as env:
        builder.python_executable = env.executable

        silent_install(env, builder.build_dependencies)

        sub_args = [builder.python_executable] + list(args)
        return subprocess.call(sub_args, cwd=cwd, **kwargs)

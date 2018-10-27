import os
import re
import sys
import shutil
import subprocess

from setuptools import setup
from setuptools.command.develop import develop
from distutils.util import get_platform
from distutils.command.build import build


package_dir = os.path.dirname(os.path.abspath(__file__))

if sys.platform == 'darwin':
    library_name = 'libZydis.dylib'
elif sys.platform in ('cygwin', 'win32'):
    library_name = 'Zydis.dll'
else:
    library_name = 'libZydis.so'


def cmake_build(source_dir, library_name, clean_build=False, build_dir=os.path.join(package_dir, 'build'),
                dest_dir=os.path.join(package_dir, 'lib'), debug_build=False):
    release_mode = 'Debug' if debug_build else 'Release'

    on_windows = sys.platform in ('cygwin', 'win32')
    if on_windows:
        library_path = os.path.join(build_dir, release_mode, library_name)
    else:
        library_path = os.path.join(build_dir, library_name)

    if clean_build:
        shutil.rmtree(build_dir)
    elif os.path.exists(library_path):
        # The library is already built.
        return True

    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    build_options = ['-DBUILD_SHARED_LIBS=ON']

    # If the python interpreter is 64bit tell cmake to build the 64bit module.
    if on_windows and 'amd64' in get_platform():
        build_options += ['-A',  'x64']

    subprocess.check_call(['cmake', os.path.abspath(source_dir)] + build_options, cwd=build_dir)
    subprocess.check_call(['cmake', '--build', '.', '--config', release_mode], cwd=build_dir)

    if not os.path.exists(library_path):
        raise Exception(f'Unable to find library after building at {library_path}')

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    dest_file = os.path.join(dest_dir, library_name)
    if os.path.exists(dest_file):
        os.unlink(dest_file)

    shutil.move(library_path, dest_file)


def build_zydis(command, debug_build):
    library_path = os.path.join(package_dir, 'pydis', 'lib')
    library = os.path.join(library_path, library_name)

    if not os.path.exists(os.path.join(package_dir, 'zydis')):
        subprocess.check_call(['git', 'submodule', 'init'], cwd=package_dir)

    if not os.path.exists(library):
        cmake_build(os.path.join(package_dir, 'zydis'), library_name, dest_dir=library_path,
                    debug_build=debug_build)
    else:
        command.announce('Zydis already built')


class DevelopCommand(develop):
    def run(self):
        self.execute(build_zydis, (self, True), msg='Building Zydis')
        develop.run(self)


class BuildCommand(build):
    def run(self):
        self.execute(build_zydis, (self, False), msg='Building Zydis')
        return build.run(self)


def set_wheel_tags(at_index):
    """
    See:
        https://www.python.org/dev/peps/pep-0425/
        https://www.python.org/dev/peps/pep-0491/#file-name-convention
    and for macs:
        https://github.com/MacPython/wiki/wiki/Spinning-wheels

    If the wheel is not supported on the platform you can debug why by looking
    at the result of:
        python3 -c 'from pip._internal import pep425tags; print(pep425tags.get_supported())
    The result is all the valid tag combinations your platform supports.
    """
    if '--plat-name' not in sys.argv:
        sys.argv.insert(at_index + 1, '--plat-name')

        platform_name = get_platform()
        platform_name = platform_name.replace('-', '_').replace('.', '_')

        # https://www.python.org/dev/peps/pep-0513/
        if 'linux' in platform_name:
            platform_name = platform_name.replace('linux', 'manylinux1')

        sys.argv.insert(at_index + 2, platform_name)

    if '--python-tag' not in sys.argv:
        # Currently this is only tested on CPython
        # Since ctypes is used it may not work on other python interpreters.
        sys.argv.insert(at_index + 1, '--python-tag')
        sys.argv.insert(at_index + 2, 'cp36')


def get_version():
    with open(os.path.join('pydis', '__init__.py')) as f:
        return re.search(r'__version__ = \'(.*?)\'', f.read()).group(1) or '0.0'


def setup_package():
    try:
        bdist_index = sys.argv.index('bdist_wheel')
        set_wheel_tags(bdist_index)
    except ValueError:
        pass

    with open('README.md') as readme:
        long_description = readme.read()

    setup(name='py-dis',
          author='Kyle',
          author_email='kyle@novogen.org',
          description='Python bindings for Zydis library',
          long_description=long_description,
          long_description_content_type='text/markdown',
          version=get_version(),
          packages=['pydis'],
          python_requires='>=3.6',
          license='MIT',
          scripts=['scripts/pydisinfo'],
          cmdclass={
              'build': BuildCommand,
              'develop': DevelopCommand
          },
          package_data={'pydis': [os.path.join('lib', library_name)]},
          classifiers=(
              'Development Status :: 5 - Production/Stable',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: MIT License',
              'Programming Language :: C',
              'Programming Language :: Python :: 3.6',
              'Programming Language :: Python :: Implementation :: CPython',
              'Topic :: Software Development :: Disassemblers',
              'Operating System :: MacOS',
              'Operating System :: Unix',
              'Operating System :: Microsoft'
          ))


if __name__ == '__main__':
    setup_package()

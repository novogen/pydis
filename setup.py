import os
import sys
import shutil
import subprocess

from setuptools import setup
from setuptools.command.develop import develop
from distutils.command.build import build
from distutils.command.sdist import sdist


package_dir = os.path.dirname(os.path.abspath(__file__))

if sys.platform == 'darwin':
    library_name = 'libZydis.dylib'
elif sys.platform in ('cygwin', 'win32'):
    library_name = 'libZydis.dll'
else:
    library_name = 'libZydis.so'


def clone_zydis():
    zydis_path = os.path.join(package_dir, 'zydis/')
    if os.path.exists(zydis_path):
        # Assume that the repo is cloned already
        return True

    subprocess.check_call(['git', 'submodule', '--init'], cwd=package_dir)

    return True


def cmake_build(source_dir, library_name, clean_build=False, build_dir=os.path.join(package_dir, 'build/'),
                dest_dir=os.path.join(package_dir, 'lib/')):
    library_path = os.path.join(build_dir, library_name)

    if clean_build:
        shutil.rmtree(build_dir)
    elif os.path.exists(library_path):
        # The library is already built.
        return True

    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    subprocess.check_call(['cmake', os.path.abspath(source_dir), '-DBUILD_SHARED_LIBS=ON'], cwd=build_dir)
    subprocess.check_call(['cmake', '--build', '.'], cwd=build_dir)

    if not os.path.exists(library_path):
        print('Unable to find library', file=sys.stderr)
        return False

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    dest_file = os.path.join(dest_dir, library_name)
    if os.path.exists(dest_file):
        os.unlink(dest_file)

    shutil.move(library_path, dest_file)

    return True

class DevelopCommand(develop):
    def run(self):
        library_path = os.path.join(package_dir, 'pydis/lib/')
        library = os.path.join(library_path, library_name)
        if os.path.exists(library):
            clone_zydis()
            cmake_build(os.path.join(package_dir, 'zydis/'), library_name, dest_dir=library_path)
        return develop.run(self)


def setup_package():
    setup(
        name='pydis',
        description='Python bindings for Zydis',
        version=0.0,
        packages=['pydis'],
        python_requires='>=3.6',
        scripts=['scripts/pydisinfo'],
        cmdclass={
            'develop': DevelopCommand
        },
        package_data={
            'pydis': [os.path.join('lib', library_name)]
        },
    )


if __name__ == '__main__':
    setup_package()
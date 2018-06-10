from setuptools import setup

def setup_package():
    setup(
        name='pydis',
        description='Python bindings for Zydis',
        version=0.0,
        packages=['pydis'],
        python_requires='>=3.6',
    )


if __name__ == '__main__':
    setup_package()
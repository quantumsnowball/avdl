from setuptools import setup

setup(
    name='avdl',
    version='0.1.0',
    description='avdl - async video downloader',
    url='https://github.com/quantumsnowball/avdl',
    author='Quantum Snowball',
    author_email='quantum.snowball@gmail.com',
    license='MIT',
    packages=['avdl'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'avdl=avdl.cli:avdl',
        ]
    }
)

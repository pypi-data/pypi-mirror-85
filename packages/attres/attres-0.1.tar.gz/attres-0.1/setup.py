from distutils.core import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
from subprocess import check_call
from pathlib import Path


class PostDevelopCommand(develop):
    def run(self):
        raise Exception("This is not the package you're looking for")
        develop.run(self)


class PostInstallCommand(install):
    def run(self):
        raise Exception("This is not the package you're looking for")
        install.run(self)


class EggInfoCommand(egg_info):
    def run(self):
        print("This is not the package you're looking for")
        egg_info.run(self)


setup(
    name="attres",
    packages=["attres"],
    version="0.1",
    description="A harmless package to prevent exploitation",
    author="htdge",
    author_email="htdge@protonmail.com",
    long_description=Path("attres/README.md").read_text(),
    long_description_content_type="text/markdown",
    cmdclass={
        "develop": PostDevelopCommand,
        "install": PostInstallCommand,
        "egg_info": EggInfoCommand,
    },
    entry_points={
        "console_scripts": [
            "attres = attres.cli:cli",
        ],
    },
)

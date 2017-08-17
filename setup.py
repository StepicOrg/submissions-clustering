import os

import pypandoc
from pip.req import parse_requirements
from setuptools import setup, find_packages, Command

install_requires, dependency_links = [], []
for ir in parse_requirements("requirements.txt", session="hack"):
    install_requires.append(str(ir.req))
    if ir.link:
        dependency_links.append(str(ir.link))


class CleanCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system("rm -vrf ./build ./*.egg-info")


setup(
    name="submissions-clustering",
    version="0.2",
    install_requires=install_requires,
    dependency_links=dependency_links,
    author="Stanislav Belyaev",
    author_email="stasbelyaev96@gmail.com",
    packages=find_packages(exclude=["tests*", "_legacy*"]),
    include_package_data=True,
    url="https://github.com/StepicOrg/submissions-clustering",
    license="MIT",
    description="Fine tool to split code submissions into clusters",
    long_description=pypandoc.convert('README.rst', 'rst'),
    platforms="any",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    cmdclass={
        # "clean": CleanCommand
    }
)

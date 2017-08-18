import setuptools_scm
from pip.req import parse_requirements
from setuptools import setup, find_packages

_readme_lines = open("README.rst").readlines()
_description = _readme_lines[4][:-1]
_long_description = "".join(_readme_lines)

_install_requires, _dependency_links = [], []
for requirement in parse_requirements("requirements.txt", session="hack"):
    _install_requires.append(str(requirement.req))
    if requirement.link:
        _dependency_links.append(str(requirement.link))

setup(
    name="submissions-clustering",
    version=setuptools_scm.get_version(),
    description=_description,
    long_description=_long_description,
    url="https://github.com/StepicOrg/submissions-clustering",
    author="Stanislav Belyaev",
    author_email="stasbelyaev96@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
    ],
    keywords="unsupervised learning code clusters",
    packages=find_packages(exclude=["_legacy*"]),
    install_requires=_install_requires,
    dependency_links=_dependency_links,
    python_requires=">=3.4, <4",
    use_scm_version=True
)

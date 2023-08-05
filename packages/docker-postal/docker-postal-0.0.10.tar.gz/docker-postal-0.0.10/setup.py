import setuptools
from postal.version import version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # info
    name="docker-postal",
    version=version,
    author="Stephen",
    author_email="squebe@crh.io",
    description="A light Docker control tool designed around compose and swarm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/obe-de/postal",
    download_url="https://github.com/obe-de/postal/archive/v" + version + ".tar.gz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # release
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['postal = postal.cli:main']},
    python_requires='>=3.6',
    install_requires=['boto', 'appdirs'],

    # test
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)

import setuptools
from pier_mob.cli import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pier-mob-lecovi", # Replace with your own username
    version=__version__,
    author="LeCoVi (Leandro E. Colombo Viña)",
    author_email="lecovi@ac.python.org.ar",
    description="A small example package for creating an executable CLI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lecovi/sample_cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
    'console_scripts': [
        'pier=pier_mob.__main__:main',
        ],
    },
    install_requires=[
        "typer",
    ],
)

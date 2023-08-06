import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ocp-modules',
    version='0.1.0',
    packages=setuptools.find_packages(),
    license='GNU General Public License',
    author="Jonas Schlagenhauf",
    author_email="schlagenhauf_github@mailbox.org",
    description="A library to assemble OCPs from modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/schlagenhauf/ocp-modules",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'casadi',
        'xarray'
    ],
    python_requires='>=3.6',
)

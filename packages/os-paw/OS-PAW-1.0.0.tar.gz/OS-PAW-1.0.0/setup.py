import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# CLASSIFIERS = ['Development Status :: 2 - Pre-Alpha',
#                 'License :: OSI Approved :: MIT License',
#                 'Programming Language :: Python :: 3',
#                 'Operating System :: Microsoft :: Windows']

# CLASSIFIERS = ['Programming Language :: Python :: 3.8']

setup(
    name="OS-PAW",
    version="1.0.0",
    description="OS-PAW is the Ordnance Survey Python API Wrapper designed to make data from the OS Data Hub APIs readily accessible to python developers.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Rapid Prototyping Team",
    author_email='jacob.rainbow@os.uk',
    license="MIT",
    # classifiers=[CLASSIFIERS],
    packages=["os_paw"],
    include_package_data=True
)



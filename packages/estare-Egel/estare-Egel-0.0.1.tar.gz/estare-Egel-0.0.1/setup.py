import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="estare-Egel", 
    version="0.0.1",
    author="Soheil Soltani",
    author_email="soheil@netc.eu",
    description="Package for stacking astrophoto images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soheil-soltani/estare",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
	"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)

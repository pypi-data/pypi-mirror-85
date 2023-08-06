from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name='TOPSIS-Aman-101803543' ,
	version='0.0.2' ,
	description='TOPSIS Package' ,
	long_description=long_description,
    long_description_content_type="text/markdown",
	py_modules=["topsis_aman"] ,
	author="Aman Singla",
    author_email="asingla2_be18@thapar.edu",
	url="",
	classifiers=[
        	"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
        	"License :: OSI Approved :: MIT License",
        	"Operating System :: OS Independent",
	],
	package_dir={'':'src'}
)
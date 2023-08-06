from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name='TOPSIS-Vaibhav-101803049' ,
	version='0.0.2' ,
	description='Example Package' ,
	long_description=long_description,
    long_description_content_type="text/markdown",
	py_modules=["firstpackage"] ,
	author="Vaibhav Allahbadia",
	url="",
    author_email="vallahbadia_be18@thapar.edu",
	classifiers=[
        	"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
        	"License :: OSI Approved :: MIT License",
        	"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
	package_dir={'':'src'}
)
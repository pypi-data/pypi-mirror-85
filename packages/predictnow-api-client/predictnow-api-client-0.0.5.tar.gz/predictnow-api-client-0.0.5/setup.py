import setuptools

with open("README_pdapi.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="predictnow-api-client",  # Replace with your own username
    version="0.0.5",
    author="PredictNow SDK Dev",
    author_email="rikky.hermanto@gmail.com",
    description="A restful client library, designed to access predictnow restful api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/predictnow/predictnow-mono",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'pandas==1.1.4',
        'firebase-admin==4.4.0',
        'pyarrow==2.0.0',
    ]
)

# use command: pip install -e .
# to install and test it locally before you publish it

#Packaging and publish pip
#https://packaging.python.org/tutorials/packaging-projects/
#	Generating distribution archives
#		Make sure you have the latest versions of setuptools and wheel installed:
#			python -m pip install --user --upgrade setuptools wheel
#
#		Now run this command from the same directory where setup.py is located:
#			python setup.py sdist bdist_wheel
#
#	Uploading the distribution archives
#		to upload the distribution packages. You’ll need to install Twine:
#			python -m pip install --user --upgrade twine
#
#		Once installed, run Twine to upload all of the archives under dist:
#			python -m twine upload --repository testpypi dist/*
# pypi
# python -m twine upload dist/*



# to install
# pip install -i https://test.pypi.org/simple/ predictnow-api-client
# pip install predictnow-api-client
# per october 2020
# pip install --use-feature=2020-resolver predictnow-api-client
# https://stackoverflow.com/questions/60050875/pandas-installation-failed-with-error-error-no-matching-distribution-found-for
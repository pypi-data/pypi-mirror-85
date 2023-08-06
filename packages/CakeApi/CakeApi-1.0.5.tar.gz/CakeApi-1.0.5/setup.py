import pathlib
from setuptools import setup, find_packages


HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='CakeApi',
    version='1.0.5',
    description='Using this module you can create a API collection and it also has lots of utilities to validate the response, status code, store a value in collection variable etc.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://www.linkedin.com/in/krishna-kumar-859a73134',
    author='Krishna Kumar Viswanathan',
    author_email='krishnaForTestAutomation@gmail.com',
    keywords='API, Rest API, API Collection, Test Automation, API test automation framework, Automation framework',
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[]
)

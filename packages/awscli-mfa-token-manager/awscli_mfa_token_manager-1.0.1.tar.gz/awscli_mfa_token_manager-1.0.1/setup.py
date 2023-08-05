import setuptools

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="awscli_mfa_token_manager",
    version="1.0.1",
    author="Anadi Misra",
    author_email="anadi.msr@gmail.com",
    description="Module to generate credentials from MFA device for AWS CLI ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="awscli aws-sts",
    url="https://github.com/anadimisra/awscli_mfa_token_manager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.8',
    scripts=['bin/manage_credentials'],
    install_requires=[
        'boto3==1.16.12',
    ],
    setup_requires=[
        "mock==4.0.2",
        "pytest==6.1.1",
        "setuptools==50.3.0",
        "tox==3.20.1",
        "yapf==0.30.0",
        "pip==20.2.2",
    ]
)

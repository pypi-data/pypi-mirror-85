from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="jd_nf",
    version="0.0.2",
    author="tst",
    author_email="tst@jd.com",
    description="neufoundry sdk",
    keywords=("pip", "datacanvas", "eds", "xiaoh"),

    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://aidoc.jd.com/neufoundry/quickstart/overview.html",
    packages=find_packages(),

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

    # python_requires='>=3.6',
    # include_package_data=True,
    # platforms="any",
    # install_requires=[]
)
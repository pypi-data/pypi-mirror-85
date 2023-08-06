from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="TOPSIS_Shivam_101853021",
    version="0.1",
    description="A Project based on TOPSIS",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/neoteroi/essentials-openapi",
    author="ShivamRajSingh",
    author_email="shivamrajsingh3009@gmail.com",
    keywords="core package",
    license="MIT",
    packages=["TOPSIS_Shivam_101853021"],
    install_requires=[
        "Pandas"
    ],
    include_package_data=True,
    zip_safe=False,
)
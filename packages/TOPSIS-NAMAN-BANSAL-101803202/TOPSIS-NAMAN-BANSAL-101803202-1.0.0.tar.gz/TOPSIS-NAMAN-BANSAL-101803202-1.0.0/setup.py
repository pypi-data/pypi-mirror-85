from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="TOPSIS-NAMAN-BANSAL-101803202",
    version="1.0.0",
    description="A Python package OF TOPSIS.",
    long_description_content_type="text/markdown",
    author="Naman_Bansal",
    author_email="naman.bansal101@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["TOPSIS_NAMAN_BANSAL_101803202"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "TOPSIS-NAMAN-BANSAL-101803202=TOPSIS_NAMAN_BANSAL_101803202.topsis:main",
        ]
    },
)

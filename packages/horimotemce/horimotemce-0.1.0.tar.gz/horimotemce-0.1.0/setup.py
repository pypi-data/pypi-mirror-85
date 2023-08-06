import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="horimotemce",
    version="0.1.0",
    author="Crowbar Z",
    author_email="crowbarz@outlook.com",
    description="Bridge MCE IR remote events to a Horimote client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crowbarz/horimotemce",
    packages=["horimotemce"],
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Multimedia",
    ],
    keywords="horimote mce",
    python_requires=">=3.6",
    install_requires=["horimote==0.4.1"],
    entry_points={
        "console_scripts": [
            "horimotemce=horimotemce.horimotemce:main",
        ]
    },
)

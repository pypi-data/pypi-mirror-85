import setuptools

setuptools.setup(
    name="bluprnt",
    version="0.1.16",
    author="Chris Wacker",
    author_email="chriswacker228@gmail.com",
    description="A small helper package for Blueprint project.",
    packages=setuptools.find_packages(),
    install_requires=["requests", "google-cloud-firestore==1.7.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

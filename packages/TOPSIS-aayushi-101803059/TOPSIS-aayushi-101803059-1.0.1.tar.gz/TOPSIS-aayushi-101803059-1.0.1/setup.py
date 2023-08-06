
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS-aayushi-101803059",
    version="1.0.1",
    author="Aayushi Gupta",
    author_email="aayushi2508gupta@gmail.com",
    description="Topsis Calculator ---PARAMRTERS--- CSV file , Weight and Impact array",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/aayu2508/topsis_2508aayushi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["topsis_2508aayushi"],
    include_package_data=True,
    install_requires='pandas',
    entry_points={
        "console_scripts": [
            "topsis_aayushi=topsis_2508aayushi.topsis:main",
        ]
    },
)

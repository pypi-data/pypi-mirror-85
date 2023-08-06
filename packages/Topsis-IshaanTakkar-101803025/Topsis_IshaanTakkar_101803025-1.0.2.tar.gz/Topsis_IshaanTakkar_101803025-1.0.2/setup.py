
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Topsis_IshaanTakkar_101803025",
    version="1.0.2",
    author="Ishaan Takkar",
    author_email="ishaantakkar@gmail.com",
    description="A package -> Calculates Topsis Score and Rank them accordingly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/takkar99/Topsis_IshaanTakkar_101803025",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["Topsis_IshaanTakkar_101803025"],
    include_package_data=True,
    install_requires='pandas',
    entry_points={
        "console_scripts": [
            "topsis=Topsis_IshaanTakkar_10180305.topsis:main",
        ]
    },
)

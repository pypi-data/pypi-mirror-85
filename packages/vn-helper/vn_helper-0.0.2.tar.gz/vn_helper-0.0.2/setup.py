import setuptools

with open("README.md", "r") as rm:
    long_description = rm.read()
with open("AUTHORS.md", "r") as rm:
    long_description_content_type = rm.read()
setuptools.setup(
    name="vn_helper",
    version="0.0.2",
    author="VanhPham",
    author_email="vananh@tinhte.vn",
    description="A small lib for preprocessing text",
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    keywords="vn_helper"

)

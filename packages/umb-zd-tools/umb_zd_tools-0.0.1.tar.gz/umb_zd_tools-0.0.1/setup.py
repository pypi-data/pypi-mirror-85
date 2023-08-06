import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="umb_zd_tools", # Replace with your own username
    version="0.0.1",
    author="Geoff Gallinger (ggalling)",
    author_email="ggalling@cisco.com",
    description="Common HTTP calls for Umbrella Zendesk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.office.opendns.com/CustomerSuccess/zendesk_api_wrapper.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

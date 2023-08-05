import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pfx_insights", # Replace with your own username
    version="0.0.7",
    author="PX PACE Insights",
    author_email="px-pace-insights@microsoft.com",
    description="Reusable python utilities for PFX Insights team",
    long_description="Reusable python utilities for PFX Insights team",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_date={
        'resources': ['*']
    },
    include_package_data = True
)

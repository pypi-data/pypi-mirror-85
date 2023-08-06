import setuptools

with open("GetNew.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GetNew",
    version="0.0.1",
    author="LoveNishimiyaShouko",
    author_email="LoveNishimiyaShouko@LoveNishimiyaShouko.LoveNishimiyaShouko",
    description="Get Version.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LoveNishimiyaShouko/GetNew",
    license="AGPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords="new version,latest version,version,get new version,get latest version,get version",
    project_urls={
        "Documentation": "https://github.com/LoveNishimiyaShouko/GetNew/tree/main/docs",
        "Source": "https://github.com/LoveNishimiyaShouko/GetNew/tree/main/code"
    },
    packages=setuptools.find_packages(include=['GetNew']),
    install_requires=["requests"],
    python_requires='>=3',
    package_data={
        'GetNew_log': ['GetNew_log.txt'],
        'GetNew_error': ['GetNew_error.txt']
    },
    entry_points={
        'console_scripts': [
            'GetNew=GetNew:main',
        ],
    },
)

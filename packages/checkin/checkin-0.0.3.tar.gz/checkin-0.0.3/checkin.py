import setuptools

with open("checkin.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="checkin",
    version="0.0.3",
    author="LoveNishimiyaShouko",
    author_email="LoveNishimiyaShouko@LoveNishimiyaShouko.LoveNishimiyaShouko",
    description="Auto check in.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LoveNishimiyaShouko/autocheckin",
    license="AGPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords="auto,check in,auto check in",
    project_urls={
        "Documentation": "https://github.com/LoveNishimiyaShouko/autocheckin/tree/main/docs",
        "Source": "https://github.com/LoveNishimiyaShouko/autocheckin/tree/main/code"
    },
    packages=setuptools.find_packages(include=['checkin']),
    install_requires=["requests"],
    python_requires='>=3',
    package_data={
        'checkin_log': ['checkin_log.txt'],
        'checkin_error': ['checkin_error.txt']
    },
    entry_points={
        'console_scripts': [
            'checkin=__init__:allcheckin',
        ],
    },
)

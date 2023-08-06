import setuptools

with open("signin.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="signin",
    version="0.0.2",
    author="LoveNishimiyaShouko",
    author_email="LoveNishimiyaShouko@LoveNishimiyaShouko.LoveNishimiyaShouko",
    description="Auto sign in.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LoveNishimiyaShouko/signin",
    license="AGPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords="auto,sign in,auto sign in",
    project_urls={
        "Documentation": "https://github.com/LoveNishimiyaShouko/signin/tree/main/docs",
        "Source": "https://github.com/LoveNishimiyaShouko/signin/tree/main/code"
    },
    packages=setuptools.find_packages(include=['signin']),
    install_requires=["requests"],
    python_requires='>=3',
    package_data={
        'signin_log': ['signin_log.txt'],
        'signin_error': ['signin_error.txt']
    },
    entry_points={
        'console_scripts': [
            'signin=signin:main',
        ],
    },
)

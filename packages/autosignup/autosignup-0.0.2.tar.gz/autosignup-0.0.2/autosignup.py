import setuptools

with open("autosignup.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autosignup",
    version="0.0.2",
    author="LoveNishimiyaShouko",
    author_email="LoveNishimiyaShouko@LoveNishimiyaShouko.LoveNishimiyaShouko",
    description="Auto sign up.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LoveNishimiyaShouko/autosignup",
    license="AGPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords="auto,sign up,auto sign up",
    project_urls={
        "Documentation": "https://github.com/LoveNishimiyaShouko/autosignup/tree/main/docs",
        "Source": "https://github.com/LoveNishimiyaShouko/autosignup/tree/main/code"
    },
    packages=setuptools.find_packages(include=['autosignup']),
    install_requires=["requests"],
    python_requires='>=3',
    package_data={
        'autosignup_log': ['autosignup_log.txt'],
        'autosignup_error': ['autosignup_error.txt']
    },
    entry_points={
        'console_scripts': [
            'autosignup=autosignup:main',
        ],
    },
)

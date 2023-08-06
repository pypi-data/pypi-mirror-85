import setuptools

with open("hMailServerConsole.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hMailServerConsole",
    version="0.0.1",
    author="LoveNishimiyaShouko",
    author_email="LoveNishimiyaShouko@LoveNishimiyaShouko.LoveNishimiyaShouko",
    description="hMailServerConsole",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LoveNishimiyaShouko/hMailServerConsole",
    license="AGPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords="NishimiyaShouko,LoveNishimiya,Nishimiya,LoveNishimiya,Shouko,hMailServerConsole",
    project_urls={
        "Documentation": "https://github.com/LoveNishimiyaShouko/hMailServerConsole/tree/main/docs",
        "Source": "https://github.com/LoveNishimiyaShouko/hMailServerConsole/tree/main/code"
    },
    packages=setuptools.find_packages(include=['hMailServerConsole']),
    install_requires=["requests"],
    python_requires='>=3',
    package_data={
        'hMailServerConsole_log': ['hMailServerConsole_log.txt'],
        'hMailServerConsole_error': ['hMailServerConsole_error.txt']
    },
    entry_points={
        'console_scripts': [
            'hMailServerConsole=hMailServerConsole:main',
        ],
    },
)

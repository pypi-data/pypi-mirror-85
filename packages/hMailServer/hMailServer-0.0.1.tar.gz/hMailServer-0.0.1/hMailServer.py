import setuptools

with open("hMailServer.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hMailServer",
    version="0.0.1",
    author="LoveNishimiyaShouko",
    author_email="LoveNishimiyaShouko@LoveNishimiyaShouko.LoveNishimiyaShouko",
    description="hMailServer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LoveNishimiyaShouko/hMailServer",
    license="AGPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords="NishimiyaShouko,LoveNishimiya,Nishimiya,LoveNishimiya,Shouko,hMailServer",
    project_urls={
        "Documentation": "https://github.com/LoveNishimiyaShouko/hMailServer/tree/main/docs",
        "Source": "https://github.com/LoveNishimiyaShouko/hMailServer/tree/main/code"
    },
    packages=setuptools.find_packages(include=['hMailServer']),
    install_requires=["requests"],
    python_requires='>=3',
    package_data={
        'hMailServer_log': ['hMailServer_log.txt'],
        'hMailServer_error': ['hMailServer_error.txt']
    },
    entry_points={
        'console_scripts': [
            'hMailServer=hMailServer:main',
        ],
    },
)

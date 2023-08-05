import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="SexyNutella",
    version="9.0",
    author="Pirxcy",
    description="A Multi Action Discord Bot Based On Anime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PirxcyFinal/AnimeBot/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=[
        'crayons',
        'dhooks',
        'discord.py',
        'timeago',
        'jinja2',
        'jaconv',
        'requests',
        'psutil',
        'pypresence',
        'uvloop',
        'sanic',
        'aiohttp'
    ],
)

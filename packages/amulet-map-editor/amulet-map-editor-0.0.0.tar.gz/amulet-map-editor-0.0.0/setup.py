from typing import List
from setuptools import setup, find_packages
import os
import glob
import shutil

# there were issues with other builds carrying over their cache
for d in glob.glob("*.egg-info"):
    shutil.rmtree(d)

setup(
    name="amulet-map-editor",
    version="0.0.0",
    description="A new Minecraft world editor and converter that supports all versions since Java 1.12 and Bedrock 1.7.",
    author="James Clare, Ben Gothard et al.",
    author_email="amuleteditor@gmail.com",
    dependency_links=[
        "https://github.com/Amulet-Team/Amulet-Core",
        "https://github.com/gentlegiantJGC/Minecraft-Model-Reader",
        "https://github.com/gentlegiantJGC/PyMCTranslate",
        "https://github.com/Amulet-Team/Amulet-NBT",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

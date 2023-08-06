from setuptools import setup, find_packages
import glob
import shutil

# there were issues with other builds carrying over their cache
for d in glob.glob("*.egg-info"):
    shutil.rmtree(d)


setup(
    name="minecraft-behavior-pack",
    version="0.0.0",
    description="A Python library reading Minecraft's various behavior pack formats.",
    author="James Clare",
    author_email="amuleteditor@gmail.com",
    packages=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

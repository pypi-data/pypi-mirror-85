import os

import setuptools

from tf2_vgpu import __version__

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="tf2-vgpu",
    version=__version__,
    author="Gareth Jones",
    author_email="garethgithub@gmail.com",
    description="",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/garethjns/tf2-vgpu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"],
    python_requires='>=3.6',
    install_requires=["tensorflow>=2.2", "joblib", "numpy", "dataclasses"])

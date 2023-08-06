import setuptools

from tf2_vgpu import __version__

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

from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="marzeqdiscord",
    version='0.1',
    packages=['marzeqdiscord'],
    url='https://github.com/marzeq/marzeqdiscord',
    license='Creative Commons Attribution NonCommercial (CC-BY-NC)',
    author='marzeq',
    author_email='marzeqmarzeq@gmail.com',
    install_requires=["discord.py>=1.5.1"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_required=">=3.6",
    description='Custom extensions for discord.py'
)

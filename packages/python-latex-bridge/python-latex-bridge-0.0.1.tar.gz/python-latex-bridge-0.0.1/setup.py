from pathlib import Path
from setuptools import setup, find_packages

folder = Path(__file__).parent
readme = (folder / 'README.md').read_text()

setup(
    name='python-latex-bridge',
    version='0.0.1',
    description='Include python variable values in a LaTeX document',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/timmedia/python-latex-bridge',
    author='Tim Mutkala',
    author_email='contact@tim-media.com',
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)
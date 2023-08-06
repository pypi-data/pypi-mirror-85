import os
from setuptools import setup, find_packages


setup(
    name='zipfolder',
    version='1.0.1',
    keywords="test",
    description='zip path',
    long_description='zip path',
    author='heifade',
    author_email='heifade@126.com',
    url='https://heifade.com',
    packages=[''],
    package_dir={"": "src"},
    # data_files=file_data,
    # include_package_data=True,
    python_requires=">=3.0, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3*",
    install_requires=["pyminizip>=0.2.4"],
    zip_safe=False
)
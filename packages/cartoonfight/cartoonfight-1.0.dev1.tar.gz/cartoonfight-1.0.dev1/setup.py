"""
from setuptools import setup
 
setup(
 name='cartoon-fight',    
 version='0.1.dev1',                          
 author='Kilian Melcher, Filipe Ramalho, Isabella Costa',
 author_email='kilian.melcher@gmail.com, filiperamalhodasilva@gmail.com, isabella.lucio1@gmail.com',
 description='2D Fighting game with cartoon characters',
 url='https://github.com/kmmelcher/cartoon-fight',
 packages=['cartoon-fight'],
 install_requires=['pygame>=2.0.0'],
 classifiers=[
 	'Development Status :: 1 - Planning',
 	'License :: OSI Approved :: MIT License',
 	'Operating System :: Unix',
 	'Programming Language :: Python :: 3.9',		
 ],              
)
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cartoonfight", 
    version="1.0.dev1",
    author="Kilian Melcher",
    author_email="kilian.melcher@gmail.com",
    description="2D Fighting game with cartoon characters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kmmelcher/cartoonfight",
    packages=setuptools.find_packages(),
    install_requires=['pygame>=2.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
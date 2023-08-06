from setuptools import setup
import setuptools

with open('README.md') as f:
    long_description = f.read()

setup(
name='greenlab-library',
version='0.1.4.9',
description='HungLV package',
url='https://gitlab.com/greenlabs/greenlab_libraries',
author='Hung LV',
long_description= long_description,
long_description_content_type="text/markdown",
author_email='hunglv@greenglobal.vn',
license='MIT',
packages=setuptools.find_packages(),
package_data={'cutils':['Aller_Bd.ttf']},
classifiers=[
     "Programming Language :: Python :: 3",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
 ],
 python_requires='>=3.6',
zip_safe=False)

from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
     name='image_dehazer',
     version='0.0.1',
     author="utkarsh-deshmukh",
     author_email="utkarsh.deshmukh@gmail.com",
     description="remove haze from images",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Utkarsh-Deshmukh/Single-Image-Dehazing-Python",
     download_url="https://github.com/Utkarsh-Deshmukh/Single-Image-Dehazing-Python/archive/master.zip",
     install_requires=['numpy==1.19.0', 'opencv-python', 'scipy'],
     license='MIT',
     keywords=['Single Image Dehazing', 'Haze Removal'],
     packages=find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
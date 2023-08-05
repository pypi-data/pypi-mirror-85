from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
     name='fingerprint_enhancer',
     version='0.0.10',
     author="utkarsh-deshmukh",
     author_email="utkarsh.deshmukh@gmail.com",
     description="enhance fingerprint images",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Utkarsh-Deshmukh/Fingerprint-Enhancement-Python",
     download_url="https://github.com/Utkarsh-Deshmukh/Fingerprint-Enhancement-Python/archive/develop.zip",
     install_requires=['numpy==1.19.0', 'opencv-python', 'scipy'],
     license='MIT',
     keywords='Fingerprint Image Enhancement',
     packages=find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
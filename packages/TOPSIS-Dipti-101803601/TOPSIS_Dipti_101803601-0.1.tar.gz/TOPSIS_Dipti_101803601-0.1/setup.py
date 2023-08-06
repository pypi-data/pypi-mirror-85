from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README
setup(name = 'TOPSIS_Dipti_101803601' ,
    packages = ['TOPSIS_Dipti_101803601'], 
    version= '0.1' , 
    license = 'MIT', 
    description = 'Pyhon Package for TOPSIS score' ,
    long_description = readme() ,
    long_description_content_type = "text/markdown" ,
    author = 'Dipti', 
    author_email = 'dkaushal_be18@thapar.edu', 
    url= 'https://github.com/diptikaushal/TOPSIS-Dipti-101803601' , 
    install_requires = [
        'pandas',
        'numpy'
        ] ,
    classifiers = [
        'Development Status :: 3 - Alpha' ,
        'Intended Audience :: Developers' ,
        'License :: OSI Approved :: MIT License' ,
        'Programming Language :: Python :: 3.4' ,
        'Programming Language :: Python :: 3.5' ,
        'Programming Language :: Python :: 3.6' ,
        'Programming Language :: Python :: 3.7' ,
        'Programming Language :: Python :: 3.8' ,
        ]    
    ) 
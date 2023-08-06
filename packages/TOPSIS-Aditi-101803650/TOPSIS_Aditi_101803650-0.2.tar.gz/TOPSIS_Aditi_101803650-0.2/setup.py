from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README
setup(name = 'TOPSIS_Aditi_101803650' ,
    packages = ['TOPSIS_Aditi_101803650'], 
    version= '0.2' , 
    license = 'MIT', 
    description = 'Pyhon Package for TOPSIS score' ,
    long_description = readme() ,
    long_description_content_type = "text/markdown" ,
    author = 'Aditi Bansal', 
    author_email = 'abansal2_be18@thapar.edu', 
    url= 'https://github.com/Aditibansal2603/TOPSIS_Aditi_101803650' , 
    download_url = 'https://github.com/Aditibansal2603/TOPSIS_Aditi_101803650/archive/v_01.tar.gz' ,
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
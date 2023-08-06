from setuptools import setup, find_packages
from os import path


URL = 'https://github.com/Vipul767/TOPSIS_Vipul_101803491'

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='TOPSIS_Vipul_101803491',
    version='1.3',
    license='MIT',
    author='Vipul Goel',
    packages=['TOPSIS_Vipul_101803491'],
    author_email='vgoel_be18@thapar.edu',
    description='TOPSIS implementation',
    long_description=LONG_DESCRIPTION,
    long_description_content_type = "text/markdown",
    url = URL,
    download_url = "https://github.com/Vipul767/TOPSIS_Vipul_101803491/archive/v_13.tar.gz",  
    keywords=['TOSPSIS','Normalised_Matrix','Performance_score','Rank','Weighted_Normalised_matrix'],
    install_requires=[
                      'pandas',
     ],
	classifiers=[
	'Development Status :: 3 - Alpha',     
        'Intended Audience :: Developers',     
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.4',
	'Programming Language :: Python :: 3.5',
	'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    
    
)

from distutils.core import setup


setup(
    name='TOPSIS_Vipul_101803491',
    version='1.0',
    author='Vipul Goel',
    packages=['TOPSIS_Vipul_101803491'],
    author_email='vgoel_be18@thapar.edu',
    description='TOPSIS implementation',
    long_description='''TOPSIS-Vipul-101803491 is an implementation of Technique of Order Preference Similarity to the Ideal Solution(TOPSIS). It will help you to place your data acc to preference that is by looking at the data and performing some Maths it will tell you the Preference in which you will be most benefitted. If you want to run the code from command line use the following format: python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName> Example: python topsis.py inputfile.csv “1,1,1,2” “+,+,-,+” result.csv''',
    url="https://github.com/Vipul767/TOPSIS_Vipul_1018013491",
    download_url = "https://github.com/Vipul767/TOPSIS_Vipul_1018013491/archive/v_10.tar.gz",  
    keywords=['TOSPSIS','Normalised_Matrix','Performance_score','Rank','Weighted_Normalised_matrix'],
    install_requires=[
                      'pandas'
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

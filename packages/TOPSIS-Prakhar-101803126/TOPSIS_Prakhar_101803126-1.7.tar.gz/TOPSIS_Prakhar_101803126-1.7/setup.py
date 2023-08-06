from distutils.core import setup

long_description = '''Topsis-Pypi-Package
A Pypi Package To calculate Topsis Score and Ranking on a given CSV File

Eg. 
from TOPSIS_Prakhar_101803126.topsis import CalculateTopsisScore
CalculateTopsisScore("./topsis_data.csv", "1,1,1,2", "+,+,-,+")

Note : 
    1. The package Shoud Contain All Non Categorical data 
    2. The size of wights and impacts should be equal'''

setup(
    # How you named your package folder (MyLib)
    name='TOPSIS_Prakhar_101803126',
    packages=['TOPSIS_Prakhar_101803126'],   # Chose the same as "name"
    version='1.7',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Package To Calulate the Topsis score and ranking of a given CSV File ( with non-categorical data only ).',
    long_description=long_description,
    author='Prakhar Jindal',                   # Type in your name
    author_email='iamprakharjindal@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/PrakharJindal/Topsis-Pypi-Package',
    # I explain this later on
    download_url='https://github.com/PrakharJindal/Topsis-Pypi-Package/archive/v1.7.tar.gz',
    # Keywords that define your package best
    keywords=['Topsis', 'Topsis Ranking'],
    install_requires=[            # I get to this in a second
        'pandas',
        'numpy',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
    ],
)

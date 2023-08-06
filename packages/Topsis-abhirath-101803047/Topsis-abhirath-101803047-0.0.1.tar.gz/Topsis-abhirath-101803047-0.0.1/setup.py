from setuptools import setup,find_packages

classifiers=[
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Topsis-abhirath-101803047',
    version='0.0.1',
    description='It is method to find out best value among different data using mathematical calculation.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='abhirath kapoor',
    author_email='akapoor_be18@thapar.edu',
    License='MIT',
    classifiers=classifiers,
    keywords='topsis',
    packages=find_packages(),
    install_requires=['numpy','pandas']

)
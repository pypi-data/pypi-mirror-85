from setuptools import setup,find_packages

classifiers=[
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Topsis-Varun-101803405',
    version='0.0.1',
    description='It is method to find out best value among different data using mathematical calculation.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Varun Bansal',
    author_email='bansalvarun116@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords='topsis',
    packages=find_packages(),
    install_requires=['numpy','pandas']

)
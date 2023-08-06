from setuptools import setup,find_packages

classifiers=[
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Topsis-raghav-101853034',
    version='0.0.1',
    description='It is method to find out best value among different data using mathematical calculation.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='raghav chadha',
    author_email='raghavchadha9196@gmail.edu',
    License='MIT',
    classifiers=classifiers,
    keywords='topsis',
    packages=find_packages(),
    install_requires=['numpy','pandas']

)
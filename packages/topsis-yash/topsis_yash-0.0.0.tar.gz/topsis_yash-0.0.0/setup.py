from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='topsis_yash',
    description='A tool to calculate TOPSIS Score and Rank for given Dataset.',
    Long_description=open('readme.txt').read() + '\n\n' + open('changelog.txt').read(),
    url='',
    author='Yash Shukla',
    author_email='yash981815@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords='topsis calculator',
    packages=find_packages(),
    install_requires=['pandas']
)
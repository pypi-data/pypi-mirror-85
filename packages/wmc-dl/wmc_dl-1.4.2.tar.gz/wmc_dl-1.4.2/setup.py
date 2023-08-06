from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='wmc_dl',
    version='1.4.2',
    description='Functions from WMC Datalake',
    long_description=open('README.txt').read() +'\n\n'+ open('CHANGELOG.txt').read(),
    url='',
    author='Daniel Santhiago',
    autor_email='daniel.santhiago@thrive-wmccann.com',
    license='MIT',
    classifiers=classifiers,
    keywords='WMCCann',
    packages=find_packages(),
    install_requires=['unidecode','criteo_marketing']
)
'''
python setup.py sdist
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/wmseo-1.0.2.tar.gz -u lucasximeness

'''
from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='wmseo',
    version='1.0.2',
    description='SEO Functions from WMC',
    long_description=open('README.txt').read() +'\n\n'+ open('CHANGELOG.txt').read(),
    url='',
    author='Lucas Ximenes',
    autor_email='lucas.ximenes@thrive-wmccann.com',
    license='MIT',
    classifiers=classifiers,
    keywords='WMCCann',
    packages=find_packages(),
    install_requires=[]
)
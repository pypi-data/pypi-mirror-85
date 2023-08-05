from distutils.core import setup
from setuptools import find_packages
from revns import __version__
setup(
    name='revns',
    packages=find_packages(exclude=['tests*']),
    version=__version__,
    license='MIT',
    description='notification service for revteltech',
    author='Chien Hsiao',
    author_email='chien.hsiao@revteltech.com',
    url='https://github.com/revtel/rns',
    keywords=['revteltech', 'notification'],
    install_requires=[
        'django', 'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)

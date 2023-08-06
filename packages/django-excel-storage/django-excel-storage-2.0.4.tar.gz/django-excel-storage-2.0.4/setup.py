# -*- coding: utf-8 -*-

from __future__ import with_statement

from setuptools import setup


version = '2.0.4'


setup(
    name='django-excel-storage',
    version=version,
    keywords='django-excel-storage',
    description='Django Excel Storage',
    long_description=open('README.rst').read(),

    url='https://github.com/django-xxx/django-excel-storage',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['django_excel_storage'],
    py_modules=[],
    install_requires=['django-excel-base>=1.0.4', 'django-six>=1.0.4'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
    ],
)

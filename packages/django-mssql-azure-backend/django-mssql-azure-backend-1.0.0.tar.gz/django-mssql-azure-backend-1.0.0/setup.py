from setuptools import find_packages, setup

CLASSIFIERS = [
    'License :: OSI Approved :: BSD License',
    'Framework :: Django',
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Framework :: Django :: 2.2',
    'Framework :: Django :: 3.0',
]

setup(
    name='django-mssql-azure-backend',
    version='1.0.0',
    description='Django backend for Microsoft SQL Server',
    long_description=open('README.rst').read(),
    author='Sathiamoorthy M',
    author_email='shakthifuture@gmail.com',
    url='https://github.com/shakthifuture/django-mssql-azure-backend',
    license='BSD',
    packages=find_packages(),
    install_requires=[
        'pyodbc>=3.0',
        'requests>=2.24.0'
    ],
    package_data={'sql_server.pyodbc': ['regex_clr.dll']},
    classifiers=CLASSIFIERS,
    keywords='django',
)


import setuptools

setuptools.setup(
    name='sqldiff',
    packages=setuptools.find_packages(),
    version='0.0.4',
    license='MIT',
    description='Compare sql objects structure (tables, views or queries) on different databases',
    author='Mateusz Matelski',
    author_email='m.z.matelski@gmail.com',
    url='https://github.com/m-matelski/sqldiff',
    download_url = 'https://github.com/m-matelski/sqldiff/archive/v0.0.4.tar.gz',
    keywords = ['sql', 'diff', 'postgres', 'teradata'],
    install_requires=[
        'sqlparse==0.4.1', 'packaging>=20.4'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
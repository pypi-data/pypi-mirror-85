from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pg-db',
    version='1.0',
    author='Wagner Corrales',
    author_email='wagnerc4@gmail.com',
    description='Psycopg2 wrapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/wcorrales/pg-db',
    packages=['pg_db'],
    install_requires=['psycopg2-binary'],
    license='GNU',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)

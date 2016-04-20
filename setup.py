from setuptools import setup, find_packages
from io import open

setup(
    name='django-flowjs',
    version='0.1b',
    description='This is an app for Django projects to enable large uploads using flow.js',
    long_description=open('README.rst', encoding='utf-8').read(),
    author='Ashley Camba Garrido',
    author_email='ashwoods@gmail.com',
    url='https://github.com/nelsonmonteiro/django-flowjs',
    download_url='https://pypi.python.org/pypi/django-flowjs',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django>=1.7',
        'django-appconf >= 0.4',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

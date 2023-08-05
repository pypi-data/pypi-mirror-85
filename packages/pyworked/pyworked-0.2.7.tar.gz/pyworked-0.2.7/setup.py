from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='pyworked',
    version='0.2.7',
    packages=find_packages(),
    description="The easiest library for Python 3",
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='library python pywork py work worked pyworked',
    url='https://github.com/Onebet163/pywork',
    author='Onebet163, UnAnsav',
    author_email='Yandancheats@gmail.com',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests',
    ]
)
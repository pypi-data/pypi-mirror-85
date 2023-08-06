from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wiz-alilog',

    version='1.0.0',

    description='wiz-alilog',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://chnyangjie.github.io/',

    author='chnyangjie',

    author_email='chnyangjie@gmail.com',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='python ali log sdk wrapper',
    package_dir={'wiz_alilog': 'src/wiz_alilog'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['aliyun-log-python-sdk'],
    py_modules=['wiz_alilog'],
    project_urls={
        'Bug Reports': 'https://github.com/chnyangjie/wiz_alilog/issues',
        'Say Thanks!': 'https://github.com/chnyangjie/wiz_alilog/issues',
        'Source': 'https://github.com/chnyangjie/wiz_alilog',
    },
)

# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path
import os

packages = find_packages()
print(packages)

here = os.path.abspath(os.path.dirname(__file__))

with open(path.join(here, 'readme.md')) as f:
    long_description = f.read()


setup(
    name="HanZi",
    packages=find_packages(),
    version='0.0.0',
    description='HanZi: database of HanZi',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.0',
    install_requires=[
        "logzero",
    ],

    include_package_data=True,
    # package_data={
    #     # 引入任何包下面的 *.txt、*.rst 文件
    #     "": ["*.txt", "*.rst"],
    #     # 引入 hello 包下面的 *.msg 文件
    #     "HanZi": ["*.txt"],
    # },
    # data_files=[('data', ['data/ChaiZi.txt'])],

    url='https://github.com/laohur/HanZi',
    keywords=['HanZi', 'UnicodeTokenizer', "ZiCutter", "https://github.com/laohur/ZiTokenizer"
              'Chinese', 'Unicode', 'laohur'],
    author='laohur',
    author_email='laohur@gmail.com',
    license='[Anti-996 License](https: // github.com/996icu/996.ICU/blob/master/LICENSE)',
)

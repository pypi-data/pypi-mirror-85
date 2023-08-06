# -*- coding: UTF-8 -*-
import os
import setuptools

setuptools.setup(
    name='my_demo_617_20201114_04',
    version='2020.11.14.4',
    keywords='demo',
    description='A demo for python packaging.',
    long_description=open( os.path.join( os.path.dirname(__file__), 'Readme.rst' )).read(),
    author='liuyaqi',  # 替换为你的Pypi官网账户名
    author_email='yaqi_617@163.com',  # 替换为你Pypi账户名绑定的邮箱

    url='https://github.com/***/***',  # 这个地方为github项目地址，貌似非必须
    packages=setuptools.find_packages(),
    license='JD'
)

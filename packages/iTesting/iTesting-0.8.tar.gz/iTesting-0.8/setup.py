# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='iTesting',
    version='0.8',
    description='This is a demo framework',
    long_description='''此Library为本人拉勾教育专栏<测试开发入门与实战>的配套练习Library.\n
    更多关于自动化测试框架的内容，请关注我的公众号iTesting.\n
    对前端自动化测试感兴趣的同学，也可以购买我的新书<前端自动化测试框架 -- Cypress从入门到精通>.
                                                                      ---Kevin Cai
    ''',
    author='kevin.cai',
    author_email='testertalk@outlook.com',
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'pytest',
        'pyyaml'
    ],
    packages=find_packages(),
    license='MIT',
    url='https://www.helloqa.com',
    entry_points={
        'console_scripts': [
            'iTesting = iTesting.main:main'
        ]
    }
)

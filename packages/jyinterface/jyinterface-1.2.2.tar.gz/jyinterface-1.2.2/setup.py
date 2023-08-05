# -*- coding: utf-8 -*-
# Author: jysatuo
import setuptools

setuptools.setup(
    name='jyinterface', # 包的名字
    version='1.2.2',  # 版本号
    description='project for trade interface',  # 描述
    author='jy', # 作者
    author_email='jysatuo@126.com',  # 你的邮箱**
    url='https://github.com/jysatuo',  # 可以写github上的地址，或者其他地址
    packages=setuptools.find_packages(exclude=['common','interface']),  # 包内需要引用的文件夹, 'interface'
    
    # 依赖包
    install_requires=[
        'numpy',
        'ast_tools',
        'grpcio',
        'grpcio_tools',
        'protobuf'
    ],
        
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: Microsoft',  # 你的操作系统
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', # BSD认证
        'Programming Language :: Python',   # 支持的语言
        'Programming Language :: Python :: 3',  # python版本 。。。
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    zip_safe=True,
)
# -*- coding: UTF-8 -*-
import setuptools
setuptools.setup(
    name='waveuse',
    version='0.0.6',
    keywords='test',
    description='Used to process audio data.',
    author='zhang_1998',  # 替换为你的Pypi官网账户名
    author_email='727261446@qq.com',  # 替换为你Pypi账户名绑定的邮箱
    url='https://github.com/ailabnjtech/wavepro/tree/maste',  # 这个地方为github项目地址，貌似非必须
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires = ['numpy', 'torch' , 'librosa'],
)
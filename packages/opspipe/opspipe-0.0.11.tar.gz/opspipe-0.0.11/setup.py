from setuptools import setup, find_packages 

setup(
    name='opspipe',
    version='0.0.11',
    description="This is the ml pipeline",
    author='zhys513',#作者
    author_email="254851907@qq.com",
    url="https://gitee.com/zhys513/opspipe",
    packages=find_packages(exclude=['DevOps','ner']),
     
    install_requires=['requests'],
    python_requires='>=3.6',
)


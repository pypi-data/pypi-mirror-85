from setuptools import setup, find_packages

setup(
    name="nlp-utils-ch",
    version="1.0.1",
    description="nlp基础工具",
    author="peng.su",
    packages=find_packages(),
    # include_package_data=True,
    package_data={
                '':[
                    'zhconv/zhcdict.json',
                    'resources/*.txt'
                    ],
               
    			},
    install_requires=[
          
      ],
    author_email="alweeq5@163.com",
)

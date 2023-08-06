from setuptools import setup, find_packages
 
setup(
  name='TOPSIS-Yubhav-101803319',
  version='0.0.1',
  description='A very basic file of topsis',
  long_description=open('README.md',"r",encoding='utf-8').read(),
  long_description_content_type="text/markdown",  
  url='https://yubhav',  
  author='yubhav',
  author_email='yubhav.seth97@gmail.com',
  license='MIT', 
  classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",

    ],
  keywords='topsis', 
  packages=find_packages(),
  install_requires=['math',
                    'pandas'
     ],
  entry_points={
        "console_scripts": [
            "topsis=topsis_program.topsis:main",
        ]
    }
)
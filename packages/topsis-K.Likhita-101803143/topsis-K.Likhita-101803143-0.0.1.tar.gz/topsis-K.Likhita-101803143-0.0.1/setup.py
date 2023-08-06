from setuptools import setup
with open("README.md","r") as fh:
    long_description =fh.read()
setup(
    name='topsis-K.Likhita-101803143',
    version='0.0.1',
    description='Say hello!',
    py_modules=["helloworld"],
    package_dir={'': 'src'},
    classifiers=[
         'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
        
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "blessings~=1.7",
    ],
    
    extras_require={
        "dev":[
            "pytest>=3.7",
        ],
    },
    
    url="https://github.com/likhita-karanam/topsis-K.Likhita-101803143",
    author="K.Likhita",
    author_email="karanamlikhita2000@gmail.com",
)

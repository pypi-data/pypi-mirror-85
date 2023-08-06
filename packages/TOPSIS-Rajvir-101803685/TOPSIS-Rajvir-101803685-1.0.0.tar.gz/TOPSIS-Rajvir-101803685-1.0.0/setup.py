from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='TOPSIS-Rajvir-101803685',
    version='1.0.0',    
    description='A TOPSIS Python package',
    long_description=README, 
    long_description_content_type="text/markdown",
    url='https://github.com/Rajvir-Singh/TOPSIS-Rajvir-101803685.git',
    author='Rajvir Singh',
    author_email='srajvir903@gmail.com',
    license="MIT",
    packages=['TOPSIS-Rajvir-101803685'],
    install_requires=['pandas'                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    package=["TOPSIS-Rajvir-101803685"],
    include_package_data=True,

)
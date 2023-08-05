import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='npal',
    version='0.0.2',
    author='Yoong Hor Meng',
    author_email='yoong+del+hm@gmail.com',
    description='Utilities to access NPAL',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    url='https://github.com/npal2/npal/',
    packages=setuptools.find_packages(),
    install_requires = [
        'selenium>=3.141.0',
        'helium>=3.0.5',
        'cryptography>=2.9.2'        
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

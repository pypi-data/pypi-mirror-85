import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'parsrt',  
    packages=setuptools.find_packages(),
    version = '1.2',
    license='MIT',    
    description = 'A minimalistic (100LOC) library to read SRT files into a workable format.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'VukGr',
    author_email = 'vuk.grujic.5@hotmail.com',
    url = 'https://github.com/vukgr/parsrt',
    download_url = 'https://github.com/user/parsrt/archive/v_10.tar.gz',
    keywords = ['SRT', 'TINY', 'MINIMALISTIC', 'FAST'],
    install_requires=[],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)

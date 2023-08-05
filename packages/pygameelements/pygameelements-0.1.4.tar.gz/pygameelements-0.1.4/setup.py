import setuptools

with open("README.md", "r") as fh:
    long_description=fh.read()
    
setuptools.setup(
    name = 'pygameelements',
    packages = ['pygameelements'],
    version = '0.1.4',
    license='MIT',
    description = 'Elements that scale with screensize for pygame',
    long_description=long_description,
    long_description_content_type="text/markdown", 
    author = 'Bas Koning',
    author_email = 'basknng@gmail.com',
    url = 'https://github.com/QuetzalQatl/PyGameElements',
    download_url = 'https://github.com/QuetzalQatl/PyGameElements/blob/main/dist/pygameelements-0.1.4.tar.gz',
    keywords = ['pygame', 'element', 'gui', 'button', 'label', 'text', 'image', 'checkbox', 'radiobutton'],
    install_requires=[
        'pygame',
        'pygameelements',
    ],
    classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',

    "Operating System :: OS Independent"
    
    ],
)
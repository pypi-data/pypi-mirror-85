import setuptools

with open("README.md", "r") as fh:
    long_description=fh.read()
    
setuptools.setup(
    name = 'pygameelements',
    packages =['pygameElements', 'pygameElementsTest'], 
    version = '0.1.43',
    license='MIT',
    description = 'Elements that scale with screensize for pygame',
    long_description=long_description, # aka README.md
    include_package_data=True, # needed for MANIFEST.in (for including files)
    long_description_content_type="text/markdown", 
    author = 'Bas Koning',
    author_email = 'basknng@gmail.com',
    url = 'https://github.com/QuetzalQatl/PyGameElements',
    download_url = 'https://github.com/QuetzalQatl/PyGameElements/blob/main/dist/pygameelements-0.1.43.tar.gz',
    keywords = ['pygame', 'element', 'gui', 'button', 'label', 'text', 'image', 'checkbox', 'inputbox', 'line', 'square', 'ellipse', 'test'],
    
    package_data={'pygameElementsTest': ['fonts/Ballpointprint.ttf', 'images/someimage.png', 'images/SquareExamples.png']},
      
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
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',

    "Operating System :: OS Independent"
    
    ],
)
import setuptools

with open("README.org", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="a2od", 
    version="0.0.2",
    author="Yann Feunteun",
    author_email="yann.feunteun@protonmail.com",
    description="Convert Anki style flashcards to Emacs org-drill format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yfe404/anki2orgdrill",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
          'click',
      ],
    entry_points='''
    [console_scripts]
    a2od=a2od:cli
    '''
)

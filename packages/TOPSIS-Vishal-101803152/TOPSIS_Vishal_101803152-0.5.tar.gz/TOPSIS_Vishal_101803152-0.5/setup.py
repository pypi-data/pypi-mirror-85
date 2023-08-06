import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS_Vishal_101803152",
    version="0.5",
    author = "Vishal Gulati",
    author_email="vgulati_be18@thapar.edu",
    description="Topsis Assignment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/vishal-gulati/TOPSIS_Vishal_101803152',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/vishal-gulati/TOPSIS_Vishal_101803152/archive/v_05.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=[
          'numpy',
          'pandas',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
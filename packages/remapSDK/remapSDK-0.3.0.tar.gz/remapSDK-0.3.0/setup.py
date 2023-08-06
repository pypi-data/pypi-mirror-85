import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="remapSDK",
    version="0.3.0",
    author="ATOS Mobility Unit",
    author_email="alejandro.garcia@atos.net",
    description="ReMAP SDK for RUL Models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://h2020-remap.eu/",
    #packages=setuptools.find_packages(),
    install_requires=[
          'requests','flask'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.5',
    packages=['remapSDK','remapSDK.demo'],
    package_dir={'remapSDK': 'remapSDK'},
    package_data={'remapSDK': ['demo/data/*csv','demo/data/*json','demo/data/secret']},
)
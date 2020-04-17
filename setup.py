from setuptools import find_packages, setup

setup(
    name='hobbyProjectWebsite',
    version='0.1.0',
    #Tells python what package directories to include
    packages=find_packages(),
    #Tells python to include data specified in MANIFEST.in file
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)


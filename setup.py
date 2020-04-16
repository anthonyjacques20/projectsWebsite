from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='0.0.2',
    #Tells python what package directories to include
    packages=find_packages(),
    #Tells python to include data specified in MANIFEST.in file
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)


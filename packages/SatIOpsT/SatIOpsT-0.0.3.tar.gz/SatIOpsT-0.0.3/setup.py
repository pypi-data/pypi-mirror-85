import setuptools
with open("README.md") as r:
    readme=r.read()
setuptools.setup(
    name="SatIOpsT",
    version="0.0.3",
    author="Subhadip Datta, Soumyadeep Dutta",
    author_email="subhadipdatta007@gmail.com",
    description="Satellite Image Operations Toolbox",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/SubhadipDatta/SatIOpsT/wiki",
    packages=setuptools.find_packages(exclude=('tests', 'docs')),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "geopandas",
        "rasterio",
        "scipy",
        "pandas",
        "numpy",
    ],
    include_package_data=True,
)
from setuptools import setup, find_packages

setup(
    name = "media-library",
    version = "0.1",
    description = "An implementation of a full-featured, web-based media library management application.",
    author = 'Thom Linton',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools', ],
)

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in qr_suite/__init__.py
from qr_suite import __version__ as version

setup(
    name="qr_suite",
    version=version,
    description="Comprehensive QR Code management for ERPNext workflows",
    author="Brighton",
    author_email="chotiputsilp.r@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)

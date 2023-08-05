import os
import shutil
from setuptools import find_packages, setup
rootdir = os.path.abspath(os.path.dirname(__file__))
os.makedirs('/opt/netbox/docs/models/netbox_announcement', exist_ok=True)
shutil.copy2(rootdir + '/netbox_announcement/doc/announcement.md',
             '/opt/netbox/docs/models/netbox_announcement')

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name='netbox-announcement',
    version='1.0',
    description='A NetBox announcement plugin',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/vas-git/netbox-announcement',
    author='Vasilatos Vitaliy',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
)

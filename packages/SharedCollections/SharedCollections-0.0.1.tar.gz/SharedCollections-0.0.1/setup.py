from setuptools import setup
import json
import os

def readme():
    with open('./README.md') as readme_fp:
        README = readme_fp.read()
    return README

class SetupMeta:
    def __init__(self):
        self.__dict__.update(
            json.loads(
                open(
                    os.path.abspath(
                        os.path.join(
                            os.path.dirname(__file__),
                            'METADATA.json'
                        )
                    )
                ).read()
            )
        )

meta = SetupMeta()

if meta.development_status == 1:
    status = 'Planning'
elif meta.development_status == 2:
    status = 'Pre-Alpha'
elif meta.development_status == 3:
    status = 'Alpha'
elif meta.development_status == 4:
    status = 'Beta'
elif meta.development_status == 5:
    status = 'Production/Stable'
elif meta.development_status == 6:
    status = 'Mature'
else:
    status = 'Inactive'


setup(
    name=meta.module_name,
    version=meta.version_info,
    description='''
        SharedCollections contains some commonly used data structured collections, which can be accessed among some multiple access manager.
    '''.strip(),
    long_description=readme(),
    long_description_content_type='text/markdown',
    url="https://github.com/antaripchatterjee/{0}".format(meta.module_name),
    author="Antarip Chatterjee",
    author_email="antarip.chatterjee22@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Development Status :: %d - %s"%(meta.development_status, status),
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Software Development"
    ],
    packages=["sharedcollections"],
    include_package_data=True
)
import pkg_resources
import setuptools

pkg_resources.require('setuptools>=39.2')
setuptools.setup(
    version_config=True,
    setup_requires=['setuptools-git-versioning'],
)
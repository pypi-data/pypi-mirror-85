# Module                       : setup.py
# Related program              : mh_universal_functions.py
# Author                       : MH
# Date                         : see _version.py
# Version                      : see _version.py
# Python Version, Mac OS X     : 3.7.7
# Python Version, Raspberry Pi : 3.7.7

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open("mh_universal_functions/_version.py").read())

setuptools.setup(
      name='mh_universal_functions',
      version=__version__,
      author='MH',
      author_email='ibhmduu1721nhg11.11@o2mail.de',
      description='General functions library',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://pypi.org/project/mh-universal-functions',
      packages=setuptools.find_packages(),
      license='MIT',
      python_requires='>=3.7',
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      zip_safe=False
)

# Upload of package to PyPI
#
#
# 1. First upload or update of package (in a terminal in PyCharm)
# python setup.py sdist bdist_wheel
# (sudo twine upload dist/*)
# twine upload --skip-existing dist/*
#
# 2. Install on Mac OS (in a terminal in PyCharm)
# sudo -H pip install mh_universal_functions==version
# sudo -H pip install mh_universal_functions
#
# 3. Install on Raspberry Pi (in a terminal on host mh3)
# sudo /usr/local/bin/python3.7 -m pip install mh-universal-functions==2020.6.27.1
#
#
# Sources:
# a) Packaging
#     https://twine.readthedocs.io/en/latest
#     https://packaging.python.org/guides/distributing-packages-using-setuptools/#setup-py
#     https://packaging.python.org/tutorials/packaging-projects
#     https://python-packaging-tutorial.readthedocs.io/en/latest/index.html
#     https://python-packaging.readthedocs.io/en/latest/minimal.html
#     https://stackoverflow.com/questions/52016336/how-to-upload-new-versions-of-project-to-pypi-with-twine
#
# b) Versioning
#     https://martin-thoma.com/python-package-versions
#
# c) PyCharm
# c.1) Publish package on pypi
#     https://blog.jetbrains.com/pycharm/2017/05/how-to-publish-your-package-on-pypi
# c.2) Managing dependencies
#     https://www.jetbrains.com/help/pycharm/managing-dependencies.html
#
# d) __init__.py
#     https://www.reddit.com/r/Python/comments/1bbbwk/whats_your_opinion_on_what_to_include_in_init_py/

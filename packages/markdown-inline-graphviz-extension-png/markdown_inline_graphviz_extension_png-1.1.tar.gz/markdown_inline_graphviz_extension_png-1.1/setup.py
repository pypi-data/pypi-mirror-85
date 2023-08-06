import os
import sys
from setuptools import setup

VERSION = '1.1'

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(VERSION))
    print("  git push --tags")
    sys.exit()

setup(
    name="markdown_inline_graphviz_extension_png",
    version=VERSION,
    py_modules=["markdown_inline_graphviz"],
    install_requires=['Markdown>=2.3.1'],
    author="Cesar Morel",
    author_email="cesaremoreln@gmail.com",
    description="Render inline graphs with Markdown and Graphviz (python3 version)",
    long_description="This is just a continuation of the great job of Steffen Prince (sprin/markdown-inline-graphviz) in order to get it work with pip3. If you use python 2, please use the original extension instead.",
    license="MIT",
    url="https://github.com/cesaremorel/markdown-inline-graphviz",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'Topic :: Text Processing',
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

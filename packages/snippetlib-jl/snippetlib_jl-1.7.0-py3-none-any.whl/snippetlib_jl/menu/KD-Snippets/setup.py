"""
Setup Module to setup Python Handlers for the jupyterlab-snippets extension.
"""
import os

from setupbase import (
    create_cmdclass, install_npm, ensure_targets,
    combine_commands, ensure_python, get_version,
)
import setuptools
from setuptools import setup
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

# The name of the project
name="snippetlib_jl"

# Ensure a valid python version
ensure_python(">=3.0")

# Get our version

# version = "1"
# snapshot_version = None

# if snapshot_version != None:
#   version = version + "." + snapshot_version
# else:
#   version = version + "0" + str(snapshot_version)
version = get_version(os.path.join(name, "_version.py"))

lab_path = os.path.join(HERE, name, "labextension")

# Representative files that should exist after a successful build
jstargets = [
    os.path.join(HERE, "lib", "snippets.js"),
]

package_data_spec = {
    name: [
        "*"
    ]
}

data_files_spec = [
    ("share/jupyter/lab/extensions", lab_path, "*.tgz"),
    ("etc/jupyter/jupyter_notebook_config.d",
     "jupyter-config", "snippetlib_jl.json"),
]

cmdclass = create_cmdclass("jsdeps",
    package_data_spec=package_data_spec,
    data_files_spec=data_files_spec
)

cmdclass["jsdeps"] = combine_commands(
    install_npm(HERE, build_cmd="build:all", npm=["jlpm"]),
    ensure_targets(jstargets),
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name=name,
    version=version,
    url="",
    author="",
    description="Code Snippets Extension for JupyterLab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    packages=setuptools.find_packages(),
    install_requires=[
        "jupyterlab",
    ],
    zip_safe=False,
    include_package_data=True,
    license="MIT License",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "JupyterLab"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Jupyter",
    ],
)
cmdclass=cmdclass,

if __name__ == '__main__':
    setuptools.setup(**setup_args)

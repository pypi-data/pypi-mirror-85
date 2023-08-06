import setuptools


# All the metadata that are expected to be reused should go here.

name: str = "pystarworldsturbo"
version: str = "1.0.2"
description: str = "PyStarWorldsTurbo, an agent library."
author: str = "Emanuele Uliana"
author_email: str = "pdac002@live.rhul.ac.uk"
license: str = "GNU3"
classifiers: list = [
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3 :: Only",
      "Development Status :: 3 - Alpha",
      "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
      "Operating System :: OS Independent",
]
url: str = "https://github.com/dicelab-rhul/pystarworldsturbo"
issues: str = url + "/issues"
dependencies: list = ["wheel", "ipython"]

# End of metadata


setuptools.setup(
      name=name,
      version=version,
      description=description,
      url=url,
      issues=issues,
      author=author,
      author_email=author_email,
      license=license,
      packages=[p for p in setuptools.find_packages() if "test" not in p],
      include_package_data=True,
      install_requires=dependencies,
      classifiers=classifiers
)

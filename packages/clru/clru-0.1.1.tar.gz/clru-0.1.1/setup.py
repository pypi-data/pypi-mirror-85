#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os
import sys
import multiprocessing
from multiprocessing.pool import ThreadPool
from setuptools.command.build_ext import build_ext
from Cython.Distutils import build_ext as cython_build_ext, Extension as CythonExtension
from Cython.Build import cythonize

from setuptools import setup, find_packages

cmd_class = {}
setup_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(setup_dir, "README.rst")) as readme_file:
    readme = readme_file.read()

with open(os.path.join(setup_dir, "CHANGELOG.rst")) as history_file:
    history = history_file.read()

with open(os.path.join(setup_dir, "clru", "VERSION"), "r",) as vf:
    version = vf.read().strip()


def parse_requirements_txt(filename="requirements.txt"):
    with open(os.path.join(setup_dir, filename)) as requirements_file:
        requirements = requirements_file.readlines()
        # remove all the requirements that are comments
        requirements = [line for line in requirements if not line.startswith("#")]
        # remove inline comments
        requirements = [line.split("#", 1)[0] if "#" in line else line for line in requirements]
        # remove empty lines
        requirements = list(filter(None, requirements))
        # remove whitespaces
        requirements = [line.strip().replace(" ", "") for line in requirements]
        return requirements


def solve_transitive_dependencies(cython_extensions):
    """ Solves the dependencies based on the information of its dependencies.

    If file A depends on B, and B depends on C, then A also depends on C.

    :type cython_extensions: list(dict)
    :param cython_extensions: all the information of the extensions to create
        to cythonize the files. Each dict has the following keys:

        - name: the extension"s full package name
        - sources: a list with the python or cython file
        - depends: a list of dependencies. It can be the path to the PXD file
            or another name on the list. When possible we should add the
            referneces to this dict, so it can add the dependencies tree
            correctly
        - kwargs: a dict with the extra kwargs to use when building the
            Cython extension

    :rtype: list(:class:`.Extension`)
    :returns: all the extensions used to cythonize the files
    """
    # create a map with all the names of the extensions
    cython_extensions_map = {extension["name"]: extension for extension in cython_extensions}

    for extension in cython_extensions:
        extension["finished"] = False

    changed = True
    while changed:
        changed = False
        for extension in cython_extensions:
            finished = True
            final_dependencies = set()
            if extension["finished"]:
                # the dependencies are final
                continue

            for dependency in extension["depends"]:
                cython_dependency = cython_extensions_map.get(dependency, None)
                if cython_dependency is None:
                    # in this case is must reference a file
                    final_dependencies.add(dependency)
                    continue
                if not cython_dependency["finished"]:
                    finished = False
                    break

                final_dependencies.update(cython_dependency["depends"])

            if finished:
                # make sure that it is finished and all the dependencies
                # have been replaced for the corresponding files
                not_cython_files = [
                    filename
                    for filename in final_dependencies
                    if os.path.splitext(filename)[1] not in (".pxd", ".pyx", ".c", ".h")
                ]
                if not_cython_files:
                    # fmt: off
                    raise Exception(
                        "Extension %s was finished but a dependency isn't a cython file: %s" % (
                            extension["name"],
                            not_cython_files
                        )
                    )
                    # fmt: on

                extension["depends"] = list(final_dependencies)
                extension["finished"] = True
                changed = True

    # if all the values have been changed make sure that
    # all the extension are finished
    not_finished = [extension for extension in cython_extensions if not extension["finished"]]
    if not_finished:
        raise Exception("At least one extension hasn't finish: %s" % not_finished)

    extension_modules = [
        CythonExtension(
            extension["name"], extension["sources"], depends=extension["depends"], **extension.get("kwargs", {})
        )
        for extension in cython_extensions
    ]
    return extension_modules


# maps all the information of the files that should be cythonized and it"s
# dependencies. Check :meth:`.solve_transitive_dependencies` to get more information
# about the values on the dict. The depends should only include the cimported
# dependencies
cython_extensions = [
    {
        "name": "clru.lrucache.cylrucache",
        "sources": ["clru/lrucache/cylrucache.pyx"],
        "depends": ["clru/lrucache/cylrucache.pxd"],
        "kwargs": {"extra_compile_args": ["-O3"]},
    },
    {
        "name": "clru.cuckoocache.cycuckoocache",
        "sources": ["clru/cuckoocache/cycuckoocache.pyx"],
        "depends": ["clru/cuckoocache/cycuckoocache.pxd"],
        "kwargs": {"extra_compile_args": ["-O3"]},
    },
]
extension_modules = solve_transitive_dependencies(cython_extensions)
include_dirs = os.environ.get("CYTHON_INCLUDE_DIRS", ".").split(":")

force_cython = "--force-cython" in sys.argv
if force_cython:
    del sys.argv[sys.argv.index("--force-cython")]

parallel = None
if "-j" in sys.argv:
    jobpos = sys.argv.index("-j")
    if len(sys.argv) > jobpos:
        # check if the user specified the number of parallel jobs
        # or if we should use the number of CPU
        try:
            parallel = int(sys.argv[jobpos + 1])
            del sys.argv[jobpos : jobpos + 2]
        except ValueError as e:
            parallel = multiprocessing.cpu_count()
            del sys.argv[jobpos]

        if parallel == 1:
            parallel = None

if "--no-cython" in sys.argv:
    del sys.argv[sys.argv.index("--no-cython")]
else:
    # check if Cython is already installed then we don"t have to do
    # anything special
    ext_modules = cythonize(extension_modules, include_path=include_dirs, nthreads=parallel, force=force_cython)
    cmd_class = {"build_ext": cython_build_ext}

    # use a coustom builder when doing a cythonization
    if parallel is not None:

        class parallel_build_ext(build_ext):
            def build_extensions(self):
                # First, sanity-check the "extensions" list
                self.check_extensions_list(self.extensions)

                for ext in self.extensions:
                    ext.sources = self.cython_sources(ext.sources, ext)

                pool = ThreadPool(parallel)
                pool.map(self.build_extension, self.extensions, chunksize=1)
                pool.close()
                pool.join()

        cmd_class["build_ext"] = parallel_build_ext


setup(
    name="clru",
    description="Cython LRU Structures",
    version=version,
    author="Claudio Freire",
    author_email="klaussfreire@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Operating System :: OS Independent",
    ],
    install_requires=parse_requirements_txt(),
    extras_require={
        "dev": parse_requirements_txt("requirements-dev.txt"),
        "dev-strict": [req.replace(">=", "==") for req in parse_requirements_txt("requirements-dev.txt")],
    },
    license="LGPLv3",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    package_data={"": ["*.pxd", "*.pyx"], "clru": ["VERSION"]},
    packages=find_packages(include=["clru", "clru.*"]),
    test_suite="tests",
    tests_require=["pytest"],
    ext_modules=ext_modules,
    cmdclass=cmd_class,
    url="https://github.com/klaussfreire/clru",
    zip_safe=False,
)

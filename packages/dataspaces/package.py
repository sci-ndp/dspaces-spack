# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dataspaces(CMakePackage):
    """DataSpaces v2 based on margo, also called dspaces"""

    homepage = "wwww.dataspaces.org"
    url = ""
    git = "https://github.com/sci-ndp/dspaces.git"

    maintainers = ['pradsubedi', 'pdavis', 'bozhang-hpc']

    version('master', branch='master', submodules=True)
    version('netcdf', branch='netcdf', submodules=True)

    variant('pybind', default=True, description='build Python bindings')
    variant('examples', default=True, description='build dspaces examples')

    depends_on('mpi')
    depends_on('py-numpy', when='+pybind')
    depends_on('python@3.6:', when='+pybind')
    depends_on('py-mpi4py', when='+pybind')
    depends_on('swig', when='+pybind')
    depends_on('cmake', type="build")
    depends_on('mochi-margo')
    depends_on('pkgconfig', type="build")
    depends_on('libtool', type="build")
    depends_on('lz4')
    depends_on('curl')

    extends('python')

    def cmake_args(self):
        """Populate cmake arguments for Dspaces."""
        extra_args = ['-DCMAKE_C_COMPILER=%s' % self.spec['mpi'].mpicc]
        extra_args.extend(['-DCMAKE_CXX_COMPILER=%s' % self.spec['mpi'].mpicxx])
        extra_args.extend(['-DENABLE_TESTS=ON'])
        extra_args.extend(['-DENABLE_EXAMPLES=ON'])
        return extra_args

    # To enable this package add it to the LD_LIBRARY_PATH
    def setup_run_environment(self, env):
        dataspaces_home = self.spec["dataspaces"].prefix
        env.prepend_path("LD_LIBRARY_PATH", dataspaces_home.lib)

    # To enable this package add it to the LD_LIBRARY_PATH
    def setup_dependent_run_environment(self, env, dependent_spec):
        dataspaces_home = self.spec["dataspaces"].prefix
        env.prepend_path("LD_LIBRARY_PATH", dataspaces_home.lib)

# ESMF application makefile fragment
#
# Use the following ESMF_ variables to compile and link
# your ESMF application against this ESMF build.
#
# !!! VERY IMPORTANT: If the location of this ESMF build is   !!!
# !!! changed, e.g. libesmf.a is copied to another directory, !!!
# !!! this file - esmf.mk - must be edited to adjust to the   !!!
# !!! correct new path                                        !!!
#
# Please see end of file for options used on this ESMF build
#

#----------------------------------------------
ESMF_VERSION_STRING=8.0.1
ESMF_VERSION_STRING_GIT=
#----------------------------------------------

ESMF_VERSION_MAJOR=8
ESMF_VERSION_MINOR=0
ESMF_VERSION_REVISION=1
ESMF_VERSION_PATCHLEVEL=1
ESMF_VERSION_PUBLIC='T'
ESMF_VERSION_BETASNAPSHOT='F'


ESMF_APPSDIR=/Users/travis/.pyenv/versions/esmf/esmf/bin/binO/Darwin.gfortran.64.mpiuni.default
ESMF_LIBSDIR=/Users/travis/.pyenv/versions/esmf/esmf/lib/libO/Darwin.gfortran.64.mpiuni.default


ESMF_F90COMPILER=gfortran
ESMF_F90LINKER=gfortran

ESMF_F90COMPILEOPTS=-fallow-argument-mismatch -fallow-invalid-boz -O   -m64 -mcmodel=small -ffree-line-length-none
ESMF_F90COMPILEPATHS=-I/Users/travis/.pyenv/versions/esmf/esmf/mod/modO/Darwin.gfortran.64.mpiuni.default -I/Users/travis/.pyenv/versions/esmf/esmf/include 
ESMF_F90COMPILECPPFLAGS=-DESMF_NO_INTEGER_1_BYTE -DESMF_NO_INTEGER_2_BYTE -DESMF_LAPACK=1 -DESMF_LAPACK_INTERNAL=1 -DESMF_MOAB=1 -DESMF_NO_ACC_SOFTWARE_STACK=1 -DESMF_YAMLCPP=1 -DESMF_YAML=1 -DESMF_NO_PTHREADS -DESMF_NO_OPENMP -DESMF_NO_OPENACC -DESMF_BOPT_O -DESMF_TESTCOMPTUNNEL -DSx86_64_small=1 -DESMF_OS_Darwin=1 -DESMF_COMM=mpiuni -DESMF_DIR=/Users/travis/.conan/data/esmf/8.0.1/CHM/stable/build/7fceccb19c4e6815ff372faca0f38ef1bec0915f -DESMF_MPIUNI
ESMF_F90COMPILEFREECPP=
ESMF_F90COMPILEFREENOCPP=-ffree-form
ESMF_F90COMPILEFIXCPP=-cpp -ffixed-form
ESMF_F90COMPILEFIXNOCPP=

ESMF_F90LINKOPTS=   -m64 -mcmodel=small
ESMF_F90LINKPATHS=-L/Users/travis/.pyenv/versions/esmf/esmf/lib/libO/Darwin.gfortran.64.mpiuni.default  -L./
ESMF_F90ESMFLINKPATHS=-L/Users/travis/.pyenv/versions/esmf/esmf/lib/libO/Darwin.gfortran.64.mpiuni.default
ESMF_F90LINKRPATHS=
ESMF_F90ESMFLINKRPATHS=-L/Users/travis/.pyenv/versions/esmf/esmf/lib/libO/Darwin.gfortran.64.mpiuni.default
ESMF_F90LINKLIBS= -lstdc++ -lc++
ESMF_F90ESMFLINKLIBS=-lesmf  -lstdc++ -lc++

ESMF_CXXCOMPILER=g++
ESMF_CXXLINKER=g++

ESMF_CXXCOMPILEOPTS=-std=c++11 -O -DNDEBUG  -DESMF_LOWERCASE_SINGLEUNDERSCORE -m64 -mcmodel=small
ESMF_CXXCOMPILEPATHS= -I/Users/travis/.pyenv/versions/esmf/esmf/include   -I/Users/travis/.pyenv/versions/esmf/esmf/src/Infrastructure/stubs/mpiuni -I/Users/travis/.pyenv/versions/esmf/esmf/src/prologue/yaml-cpp/include
ESMF_CXXCOMPILECPPFLAGS=-DESMF_NO_INTEGER_1_BYTE -DESMF_NO_INTEGER_2_BYTE -DESMF_LAPACK=1 -DESMF_LAPACK_INTERNAL=1 -DESMF_MOAB=1 -DESMF_NO_ACC_SOFTWARE_STACK=1 -DESMF_YAMLCPP=1 -DESMF_YAML=1 -DESMF_NO_PTHREADS -DESMF_NO_OPENMP -DESMF_NO_OPENACC -DESMF_BOPT_O -DESMF_TESTCOMPTUNNEL -DSx86_64_small=1 -DESMF_OS_Darwin=1 -DESMF_COMM=mpiuni -DESMF_DIR=/Users/travis/.conan/data/esmf/8.0.1/CHM/stable/build/7fceccb19c4e6815ff372faca0f38ef1bec0915f -D__SDIR__='' -DESMF_CXXSTD=11 -DESMF_MPIUNI

ESMF_CXXLINKOPTS=  -m64 -mcmodel=small
ESMF_CXXLINKPATHS=-L/Users/travis/.pyenv/versions/esmf/esmf/lib/libO/Darwin.gfortran.64.mpiuni.default  -L/usr/local/Cellar/gcc/10.2.0/lib/gcc/10/gcc/x86_64-apple-darwin18/10.2.0/../../../
ESMF_CXXESMFLINKPATHS=-L/Users/travis/.pyenv/versions/esmf/esmf/lib/libO/Darwin.gfortran.64.mpiuni.default
ESMF_CXXLINKRPATHS=
ESMF_CXXESMFLINKRPATHS=-L/Users/travis/.pyenv/versions/esmf/esmf/lib/libO/Darwin.gfortran.64.mpiuni.default
ESMF_CXXLINKLIBS= -lgfortran
ESMF_CXXESMFLINKLIBS=-lesmf  -lgfortran

ESMF_SO_F90COMPILEOPTS=
ESMF_SO_F90LINKOPTS=
ESMF_SO_F90LINKOPTSEXE=
ESMF_SO_CXXCOMPILEOPTS=
ESMF_SO_CXXLINKOPTS=
ESMF_SO_CXXLINKOPTSEXE=

ESMF_OPENMP_F90COMPILEOPTS=
ESMF_OPENMP_F90LINKOPTS=
ESMF_OPENMP_CXXCOMPILEOPTS=
ESMF_OPENMP_CXXLINKOPTS=

ESMF_OPENACC_F90COMPILEOPTS=
ESMF_OPENACC_F90LINKOPTS=
ESMF_OPENACC_CXXCOMPILEOPTS=
ESMF_OPENACC_CXXLINKOPTS=

# ESMF Tracing compile/link options
ESMF_TRACE_LDPRELOAD=/Users/travis/.pyenv/versions/esmf/esmf/lib/libO/Darwin.gfortran.64.mpiuni.default/libesmftrace_preload.dylib
ESMF_TRACE_STATICLINKOPTS=-static -Wl,--wrap=c_esmftrace_notify_wrappers -Wl,--wrap=c_esmftrace_isinitialized -Wl,--wrap=write -Wl,--wrap=writev -Wl,--wrap=pwrite -Wl,--wrap=read -Wl,--wrap=open -Wl,--wrap=MPI_Allgather -Wl,--wrap=MPI_Allgatherv -Wl,--wrap=MPI_Allreduce -Wl,--wrap=MPI_Alltoall -Wl,--wrap=MPI_Alltoallv -Wl,--wrap=MPI_Alltoallw -Wl,--wrap=MPI_Barrier -Wl,--wrap=MPI_Bcast -Wl,--wrap=MPI_Gather -Wl,--wrap=MPI_Gatherv -Wl,--wrap=MPI_Recv -Wl,--wrap=MPI_Reduce -Wl,--wrap=MPI_Scatter -Wl,--wrap=MPI_Send -Wl,--wrap=MPI_Sendrecv -Wl,--wrap=MPI_Wait -Wl,--wrap=MPI_Waitall -Wl,--wrap=MPI_Waitany -Wl,--wrap=MPI_Waitsome -Wl,--wrap=mpi_allgather_ -Wl,--wrap=mpi_allgather__ -Wl,--wrap=mpi_allgatherv_ -Wl,--wrap=mpi_allgatherv__ -Wl,--wrap=mpi_allreduce_ -Wl,--wrap=mpi_allreduce__ -Wl,--wrap=mpi_alltoall_ -Wl,--wrap=mpi_alltoall__ -Wl,--wrap=mpi_alltoallv_ -Wl,--wrap=mpi_alltoallv__ -Wl,--wrap=mpi_alltoallw_ -Wl,--wrap=mpi_alltoallw__ -Wl,--wrap=mpi_barrier_ -Wl,--wrap=mpi_barrier__ -Wl,--wrap=mpi_bcast_ -Wl,--wrap=mpi_bcast__ -Wl,--wrap=mpi_exscan_ -Wl,--wrap=mpi_exscan__ -Wl,--wrap=mpi_gather_ -Wl,--wrap=mpi_gather__ -Wl,--wrap=mpi_gatherv_ -Wl,--wrap=mpi_gatherv__ -Wl,--wrap=mpi_recv_ -Wl,--wrap=mpi_recv__ -Wl,--wrap=mpi_reduce_ -Wl,--wrap=mpi_reduce__ -Wl,--wrap=mpi_reduce_scatter_ -Wl,--wrap=mpi_reduce_scatter__ -Wl,--wrap=mpi_scatter_ -Wl,--wrap=mpi_scatter__ -Wl,--wrap=mpi_scatterv_ -Wl,--wrap=mpi_scatterv__ -Wl,--wrap=mpi_scan_ -Wl,--wrap=mpi_scan__ -Wl,--wrap=mpi_send_ -Wl,--wrap=mpi_send__ -Wl,--wrap=mpi_wait_ -Wl,--wrap=mpi_wait__ -Wl,--wrap=mpi_waitall_ -Wl,--wrap=mpi_waitall__ -Wl,--wrap=mpi_waitany_ -Wl,--wrap=mpi_waitany__
ESMF_TRACE_STATICLINKLIBS=-lesmftrace_static

# Internal ESMF variables, do NOT depend on these!

ESMF_INTERNAL_DIR=/Users/travis/.pyenv/versions/esmf/esmf/

#
# !!! The following options were used on this ESMF build !!!
#
# ESMF_DIR: /Users/travis/.conan/data/esmf/8.0.1/CHM/stable/build/7fceccb19c4e6815ff372faca0f38ef1bec0915f
# ESMF_OS: Darwin
# ESMF_MACHINE: x86_64
# ESMF_ABI: 64
# ESMF_COMPILER: gfortran
# ESMF_BOPT: O
# ESMF_COMM: mpiuni
# ESMF_SITE: default
# ESMF_PTHREADS: OFF
# ESMF_OPENMP: OFF
# ESMF_OPENACC: OFF
# ESMF_ARRAY_LITE: FALSE
# ESMF_NO_INTEGER_1_BYTE: TRUE
# ESMF_NO_INTEGER_2_BYTE: TRUE
# ESMF_FORTRANSYMBOLS: default
# ESMF_MAPPER_BUILD: OFF
# ESMF_AUTO_LIB_BUILD: ON
# ESMF_DEFER_LIB_BUILD: ON
# ESMF_SHARED_LIB_BUILD: ON
# 
# ESMF environment variables pointing to 3rd party software:
# ESMF_MOAB:              internal
# ESMF_LAPACK:            internal
# ESMF_ACC_SOFTWARE_STACK:            none
# ESMF_YAMLCPP:           internal

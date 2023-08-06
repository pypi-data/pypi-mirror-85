#!/bin/sh
# Script to preload ESMF dynamic trace library
env LD_PRELOAD="$LD_PRELOAD /Users/travis/.conan/data/esmf/8.1.0_beta_snapshot_36/CHM/stable/package/7fceccb19c4e6815ff372faca0f38ef1bec0915f/lib/libO/Darwin.gfortran.64.mpiuni.default/libesmftrace_preload.dylib" $*

#!/usr/bin/env python3
## vi: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
## ---------------------------------------------------------------------
##
## Copyright (C) 2019 by the adcc authors
##
## This file is part of adcc.
##
## adcc is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## adcc is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with adcc. If not, see <http://www.gnu.org/licenses/>.
##
## ---------------------------------------------------------------------

# TODO This should be the place for global, program-wise modifiable configuration
#      where defaults are read in from a file
#
# Ideas:
#    - number of threads
#    - maximal memory
#    - tensor block size
#    - libvmm or libxm or stuff
#    - "verbosity"

# This should replace the memory_pool and the thread_pool thingies, which should
# be lazily generated from this data on first need allowing the user to modify
# this configuration at one place
#
#
# Offer a way to read psi4 / pyscf configuration data into this automatically.

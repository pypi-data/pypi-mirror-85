#!/usr/bin/env python3
## vi: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
## ---------------------------------------------------------------------
##
## Copyright (C) 2020 by the adcc authors
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
import numpy as np


def project_amplitude(cvs, full):
    """
    Project CVS amplitude to a full amplitude
    """
    assert "s" in full.blocks

    n_c, n_v = cvs["s"].shape
    n_c_a = n_c // 2
    # n_v_a = n_v // 2

    n_of_a = full["s"].shape[0] // 2

    # singles
    cvs_s_arr = cvs["s"].to_ndarray()
    cvs_s_arr_a = cvs_s_arr[:n_c_a, :]
    cvs_s_arr_b = cvs_s_arr[n_c_a:, :]

    full_s_arr = np.zeros(full["s"].shape)
    full_s_arr[:n_c_a, :] = cvs_s_arr_a
    full_s_arr[n_of_a:n_of_a + n_c_a, :] = cvs_s_arr_b
    full["s"].set_from_ndarray(full_s_arr, 1e-12)

    if "d" in full.blocks:
        n_o = cvs["d"].shape[0]
        n_o_a = n_o // 2
        # n_of_a = n_c_a + n_o_a

        # doubles
        cvs_d_arr = cvs["d"].to_ndarray()
        cvs_d_arr_aa = cvs_d_arr[:n_o_a, :n_c_a, :, :]
        cvs_d_arr_ab = cvs_d_arr[:n_o_a, n_c_a:, :, :]
        cvs_d_arr_ba = cvs_d_arr[n_o_a:, :n_c_a, :, :]
        cvs_d_arr_bb = cvs_d_arr[n_o_a:, n_c_a:, :, :]

        full_d_arr = np.zeros(full["d"].shape)
        full_d_arr[n_c_a:n_of_a, 0:n_c_a, :, :] =  cvs_d_arr_aa
        full_d_arr[0:n_c_a, n_c_a:n_of_a, :, :] = -cvs_d_arr_aa.transpose((1,0,2,3))
        #
        full_d_arr[n_c_a:n_of_a, n_of_a:n_of_a + n_c_a, :, :] = cvs_d_arr_ab
        full_d_arr[n_of_a:n_of_a + n_c_a, n_c_a:n_of_a, :, :] = -cvs_d_arr_ab.transpose((1,0,2,3))
        #
        full_d_arr[n_of_a + n_c_a:, 0:n_c_a, :, :] = cvs_d_arr_ba
        full_d_arr[0:n_c_a, n_of_a + n_c_a:, :, :] = -cvs_d_arr_ba.transpose((1,0,2,3))
        #
        full_d_arr[n_of_a + n_c_a:, n_of_a:n_of_a + n_c_a, :, :] = cvs_d_arr_bb
        full_d_arr[n_of_a:n_of_a + n_c_a, n_of_a + n_c_a:, :, :] = -cvs_d_arr_bb.transpose((1,0,2,3))

        full["d"].set_from_ndarray(full_d_arr, 1e-12)

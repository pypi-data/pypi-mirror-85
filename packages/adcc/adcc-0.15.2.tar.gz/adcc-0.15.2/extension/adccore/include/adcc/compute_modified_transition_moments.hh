//
// Copyright (C) 2019 by the adcc authors
//
// This file is part of adcc.
//
// adcc is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published
// by the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// adcc is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with adcc. If not, see <http://www.gnu.org/licenses/>.
//

#pragma once

#include "AmplitudeVector.hh"
#include "LazyMp.hh"
#include "OneParticleOperator.hh"

namespace adcc {
/**
 *  \addtogroup Properties
 */
///@{

/** Compute the modified transition moments (MTM)
 *
 * \param method                The ADC method to use
 * \param ground_state_ptr      The MP ground state to build upon
 * \param op_ptr                The operator for which the MTM
 *                              should be computed
 *
 */
std::shared_ptr<AmplitudeVector> compute_modified_transition_moments(
      std::string method, std::shared_ptr<const LazyMp> ground_state_ptr,
      std::shared_ptr<OneParticleOperator> op_ptr);

///@}
}  // namespace adcc

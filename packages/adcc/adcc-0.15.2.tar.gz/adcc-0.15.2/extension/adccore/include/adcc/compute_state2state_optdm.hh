//
// Copyright (C) 2018 by the adcc authors
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
#include "AdcIntermediates.hh"
#include "AmplitudeVector.hh"
#include "LazyMp.hh"
#include "OneParticleOperator.hh"

namespace adcc {
/**
 *  \addtogroup Properties
 */
///@{

/** Compute the excited state to excited state one-particle
 * transition-density matrix (optdm) at the ADC level of theory
 * given by the method_ptr.
 *
 * \param method                The ADC method to use
 * \param ground_state_ptr      The MP ground state to build upon
 * \param excitation_amplitude_from  The excitation amplitude, given as a std::vector of
 *                                   blocks (singles, doubles, ...) from which the
 *                                   electronic transition starts
 * \param excitation_amplitude_to    The excitation amplitude, given as a std::vector of
 *                                   blocks (singles, doubles, ...) where the
 *                                   electronic transition ends.
 * \param intermediates_ptr     Adc intermediates to reuse during property calculation
 */
std::shared_ptr<OneParticleOperator> compute_state2state_optdm(
      std::string method, std::shared_ptr<const LazyMp> ground_state_ptr,
      const AmplitudeVector& excitation_amplitude_from,
      const AmplitudeVector& excitation_amplitude_to,
      std::shared_ptr<AdcIntermediates> intermediates_ptr);

///@}
}  // namespace adcc

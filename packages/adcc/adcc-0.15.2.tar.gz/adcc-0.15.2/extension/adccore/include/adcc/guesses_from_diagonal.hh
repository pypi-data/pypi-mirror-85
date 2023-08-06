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
#include "guess_zero.hh"

namespace adcc {
/**
 *  \addtogroup AdcGuess
 */
///@{

/** Obtain guesses by inspecting a block of the diagonal of the passed ADC matrix.
 *  The symmetry of the returned vectors is already set-up properly. Note that
 *  this routine may return fewer vectors than requested in case the requested
 *  number could not be found.
 *
 *  matrix     AdcMatrix for which guesses are to be constructed
 *  kind       AdcGuessKind object describing the kind of guesses to be constructed
 *  block      The block of the diagonal to investigate. May be "s" (singles) or
 *             "d" (doubles).
 *  n_guesses  The number of guesses to look for.
 *  degeneracy_tolerance  Tolerance for two entries of the diagonal to be considered
 *                        degenerate, i.e. identical.
 */
std::vector<AmplitudeVector> guesses_from_diagonal(const AdcMatrix& matrix,
                                                   const AdcGuessKind& kind,
                                                   std::string block, size_t n_guesses,
                                                   scalar_type degeneracy_tolerance);
///@}
}  // namespace adcc

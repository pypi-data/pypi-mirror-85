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
#include "AdcMatrix.hh"
#include "AmplitudeVector.hh"
#include "Symmetry.hh"
#include <string>

namespace adcc {
/**
 *  \defgroup AdcGuess ADC guess setup
 */
///@{

/** Struct, which collects information about the kind of guess vectors to be constructed.
 *
 *  \note
 *  The information is collected in the sense of "what the guess vectors should
 *  look like" as opposed to "what excitations are computed with such vectors".
 *  The reasoning is that the latter also depends on the reference, which, however,
 *  does not influence the way the guess algorithms need to find the guess vectors.
 *
 *  To make the collected quantities more relatable, here are common profiles:
 *  - Singlet RHF reference
 *      - for computing singlet excited states:
 *          spin_change == 0 and spin_block_symmetrisation == "symmetric"
 *      - for computing triplet excited states:
 *          spin change == 0 and spin_block_symmetrisation == "antisymmetric"
 *  - UHF reference
 *      - for computing any kind of excited state:
 *          spin_change == 0 and spin_symmetrisation == "none"
 *      - for spin-flip states:
 *          spin_change == -1 and spin_symmetrisation == "none"
 **/
struct AdcGuessKind {
  /** String describing the irreducable representation to consider */
  std::string irrep;

  /** The spin change to enforce in an excitation. Typical values are 0 and -1. */
  float spin_change;

  /** Twice the value of spin_change as an integer */
  int spin_change_twice;

  /** Symmetrisation to enforce between equivalent spin blocks, which all yield
   *  the desired spin_change. E.g. if spin_change == 0, then both the alpha->alpha
   *  and beta->beta blocks of the singles part of the excitation vector achieve
   *  this spin change. The symmetry specified with this parameter will then be
   *  imposed between the a-a and b-b blocks.
   *  Valid values are "none", "symmetric" and "antisymmetric",
   *  where "none" enforces no symmetry.
   */
  std::string spin_block_symmetrisation;

  AdcGuessKind(std::string irrep_, float spin_change_,
               std::string spin_block_symmetrisation_);

  AdcGuessKind()
        : irrep("A"),
          spin_change(0.0f),
          spin_change_twice(0),
          spin_block_symmetrisation("none") {}
};

/** Return the symmetries for setting up guess vectors. The first entry is the singles
 *  symmetry the second the doubles symmetry and so on. */
std::vector<std::shared_ptr<Symmetry>> guess_symmetries(const AdcMatrix& matrix,
                                                        const AdcGuessKind& kind);

/** Return an AmplitudeVector object filled with zeros, but where the symmetry
 *  has been properly set up to meet the requirements of the AdcGuessKind object
 */
AmplitudeVector guess_zero(const AdcMatrix& matrix, const AdcGuessKind& kind);

///@}
}  // namespace adcc


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
#include <string>

namespace adcc {
/**
 *  \addtogroup Tensor
 */
///@{

/** A class managing the indices involved in a contraction. */
struct ContractionIndices {
  /** The indices on the first input tensor */
  std::string first;

  /** The indices on the second input tensor */
  std::string second;

  /** The indices on the output tensor */
  std::string result;

  /** The indices over which the contraction is performed */
  std::string contraction;

  /** Trace indices (Indices which repeat in a single tensor) */
  std::string trace;

  /** All indices (contracted or free) which are involved
   *  in this contraction in alphabetical order. */
  std::string all;

  /** Return the indices into the axes of first and second
   *  which are contracted by c
   *
   *  \throws invalid_argument   If c is in result
   *  */
  std::pair<size_t, size_t> contracted_tensor_axes(const char& c) const;

  /** Returns whether the passed index is contracted over */
  bool is_contraction_index(const char& c) const;

  /** Returns whether the passed index is part of the result */
  bool is_result_index(const char& c) const;

  ContractionIndices(const std::string& contraction);
};

///@}
}  // namespace adcc

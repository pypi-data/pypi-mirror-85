""" Constraint module. """

#  ISC License
#
#  Copyright (c) 2020, Paul Wilhelm <anfrage@paulwilhelm.de>
#
#  Permission to use, copy, modify, and/or distribute this software for any
#  purpose with or without fee is hereby granted, provided that the above
#  copyright notice and this permission notice appear in all copies.
#
#  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from magneticalc.Debug import Debug
from magneticalc.Metric import metric_norm
from magneticalc.Theme import Theme


class Constraint:
    """ Constraint class. """

    # Norm IDs
    Norm_ID_List = {
        "X"             : 0,
        "Y"             : 1,
        "Z"             : 2,
        "Radius XY"     : 3,
        "Radius XZ"     : 4,
        "Radius YZ"     : 5,
        "Radius"        : 6,
        "Angle XY"      : 7,
        "Angle XZ"      : 8,
        "Angle YZ"      : 9,
    }

    # Comparison IDs
    Comparison_ID_List = {
        "In Range"      : 0
    }

    def __init__(self, norm_id: str, comparison_id: str, _min: float, _max: float, permeability: float):
        """
        Initializes the constraint.

        @param norm_id: Norm ID
        @param comparison_id: Comparison ID
        @param _min: Minimum value
        @param _max: Maximum value
        @param permeability: Relative permeability µ_r
        """
        if norm_id not in self.Norm_ID_List:
            Debug(self, "Invalid norm ID", color=Theme.WarningColor, force=True)
            return

        if comparison_id not in self.Comparison_ID_List:
            Debug(self, "Invalid comparison ID", color=Theme.WarningColor, force=True)
            return

        self._norm_id = norm_id
        self._comparison_id = comparison_id

        self._min = _min
        self._max = _max

        self.permeability = permeability

    def evaluate(self, point) -> bool:
        """
        Evaluate this constraint at some point.

        @param point: Point (3D vector)
        """
        norm = metric_norm(self._norm_id, point)

        # Perform comparison
        if self._comparison_id == "In Range":
            return self._min <= norm <= self._max
        else:
            # Invalid comparison ID
            return False

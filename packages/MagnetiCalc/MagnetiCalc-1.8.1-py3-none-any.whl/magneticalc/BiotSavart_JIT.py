""" BiotSavart_JIT module. """

#  ISC License
#
#  Copyright (c) 2020, Paul Wilhelm, M. Sc. <anfrage@paulwilhelm.de>
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

import numpy as np
from numba import jit, prange
from PyQt5.QtCore import QThread
from magneticalc.Constants import Constants
from magneticalc.Debug import Debug
from magneticalc.Theme import Theme


class BiotSavart_JIT:
    """
    Implements the Biot-Savart law for calculating the magnetic flux density.
    """

    def __init__(
            self,
            _type,
            progress_callback,
            distance_limit,
            length_scale,
            dc,
            current_elements,
            sampling_volume_points
    ):
        """
        Populates class attributes.

        @param _type: Field type (0: A-Field; 1: B-Field)
        @param progress_callback: Progress callback
        @param distance_limit: Distance limit (mitigating divisions by zero)
        @param length_scale: Length scale (m)
        @param dc: Wire current (A)
        @param current_elements: List of current elements (list of 3D vector pairs: (element center, element direction))
        @param sampling_volume_points: List of sampling volume points
        """
        self._type = _type
        self._progress_callback = progress_callback
        self._distance_limit = distance_limit
        self._length_scale = length_scale
        self._dc = dc
        self._current_elements = current_elements
        self._sampling_volume_points = sampling_volume_points

        self.total_limited = 0

    @staticmethod
    @jit(nopython=True, parallel=True)
    def worker(_type, distance_limit, length_scale, current_elements, sampling_volume_point):
        """
        Either calculates the magnetic flux density (B-Field) at some sampling volume point using the Biot-Savart law,
        or calculates the magnetic vector potential (A-Field).

        @param _type: Field type (0: A-Field; 1: B-Field)
        @param distance_limit: Distance limit (mitigating divisions by zero)
        @param length_scale: Length scale (m)
        @param current_elements: Ordered list of current elements (3D vector pairs: (element center, element direction))
        @param sampling_volume_point: Sampling volume point (3D vector)
        @return: (Total number of limited points, vector)
        """
        total_limited = 0
        vector = np.zeros(3)

        for j in prange(len(current_elements)):
            element_center = current_elements[j][0]
            element_direction = current_elements[j][1]

            vector_distance = (sampling_volume_point - element_center) * length_scale

            # Calculate distance (mitigating divisions by zero)
            scalar_distance = np.sqrt(vector_distance[0] ** 2 + vector_distance[1] ** 2 + vector_distance[2] ** 2)
            if scalar_distance < distance_limit:
                scalar_distance = distance_limit
                total_limited += 1

            if _type == 0:
                # Calculate A-Field (vector potential)
                vector += element_direction * length_scale / scalar_distance
            elif _type == 1:
                # Calculate B-Field (flux density)
                vector += np.cross(element_direction * length_scale, vector_distance) / (scalar_distance ** 3)

        return total_limited, vector

    def get_vectors(self):
        """
        Calculates the magnetic flux density at every point of the sampling volume.

        @return: (Total number of limited points, field) if successful, None if interrupted
        """
        Debug(self, ".get_vectors()", color=Theme.PrimaryColor)

        total_limited = 0
        vectors = []

        # Fetch resulting vectors
        for i in range(len(self._sampling_volume_points)):

            tup = BiotSavart_JIT.worker(
                self._type,
                self._distance_limit,
                self._length_scale,
                self._current_elements,
                self._sampling_volume_points[i]
            )

            total_limited += tup[0]
            vectors.append(tup[1])

            # Signal progress update, handle interrupt (every 16 iterations to keep overhead low)
            if i & 0xf == 0:
                self._progress_callback(100 * (i + 1) / len(self._sampling_volume_points))

                if QThread.currentThread().isInterruptionRequested():
                    Debug(self, ": Interruption requested, exiting now", color=Theme.PrimaryColor)
                    return None

        if self._type == 0 or self._type == 1:
            # Field is A-Field or B-Field
            vectors = np.array(vectors) * self._dc * Constants.k

        return total_limited, vectors

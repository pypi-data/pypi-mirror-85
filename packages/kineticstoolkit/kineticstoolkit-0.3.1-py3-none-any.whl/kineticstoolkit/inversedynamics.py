#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Félix Chénier

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Provide functions to calculate inverse dynamics.

Warning
-------
This module is currently experimental and its API and behaviour could be
modified in the future.

"""

__author__ = "Félix Chénier"
__copyright__ = "Copyright (C) 2020 Félix Chénier"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"


import kineticstoolkit.filters
from kineticstoolkit.decorators import unstable

import numpy as np
from typing import Dict, List
from kineticstoolkit import TimeSeries


listing = []  # type: List[str]


@unstable(listing)
def get_anthropometrics(segment_name: str,
                        total_mass: float) -> Dict[str, float]:
    """
    Get anthropometric values for a given segment name.

    Warning
    -------
    This method is experimental and its signature and behaviour could change
    in the future.


    For the moment, only this table is available:

    D. A. Winter, Biomechanics and Motor Control of Human Movement,
    4th ed. University of Waterloo, Waterloo, Ontario, Canada,
    John Wiley & Sons, 2009.

    Parameters
    ----------
    segment_name
        The name of the segment, either:

        - 'Hand' (wrist axis to knuckle II of middle finger)
        - 'Forearm' (elbow axis to ulnar styloid)
        - 'UpperArm' (glenohumeral axis to elbow axis)
        - 'ForearmHand' (elbow axis to ulnar styloid)
        - 'TotalArm' (glenohumeral joint to ulnar styloid)
        - 'Foot' (lateral malleolus to head metatarsal II)
        - 'Leg' (femoral condyles to medial malleolus)
        - 'Thigh' (greater trochanter to femoral condyles)
        - 'FootLeg' (fomeral condyles to medial malleolus)
        - 'TotalLeg' (greater trochanter to medial malleolus)
        - 'TrunkHeadNeck' (greater trochanter to glenohumeral joint)
        - 'HeadArmsTrunk' (greater trochanter to glenohumeral joint)

    total_mass
        The total mass of the person, in kg.

    Returns
    -------
    Dict[str, float]
        A dict with the following keys:

        - 'Mass' : Mass of the segment, in kg.
        - 'COMProximalRatio' : Distance between the segment's center of
          mass and the proximal joint, as a ratio of the distance between
          both joints.
        - 'COMDistalRatio' : Distance between the segment's center of mass
          and the distal joint, as a ratio of the distance between
          both joints.
        - 'GyrationCOMRatio': Radius of gyration around the segment's center
          of mass, as a ratio of the distance between both joints.
        - 'GyrationProximalRatio': Radius of gyration around the segment's
           proximal joint, as a ratio of the distance between both joints.
        - 'GyrationDistalRatio': Radius of gyration around the segment's
           distal joint, as a ratio of the distance between both joints.

    """
    table = dict()
    table['Hand'] = [0.006, 0.506, 0.494, 0.297, 0.587, 0.577]
    table['Forearm'] = [0.016, 0.430, 0.570, 0.303, 0.526, 0.647]
    table['UpperArm'] = [0.028, 0.436, 0.564, 0.322, 0.542, 0.645]
    table['ForearmHand'] = [0.022, 0.682, 0.318, 0.468, 0.827, 0.565]
    table['TotalArm'] = [0.050, 0.530, 0.470, 0.368, 0.645, 0.596]
    table['Foot'] = [0.0145, 0.50, 0.50, 0.475, 0.690, 0.690]
    table['Leg'] = [0.0465, 0.433, 0.567, 0.302, 0.528, 0.643]
    table['Thigh'] = [0.100, 0.433, 0.567, 0.323, 0.540, 0.653]
    table['FootLeg'] = [0.061, 0.606, 0.394, 0.416, 0.735, 0.572]
    table['TotalLeg'] = [0.161, 0.447, 0.553, 0.326, 0.560, 0.650]
    table['TrunkHeadNeck'] = [0.578, 0.66, 0.34, 0.503, 0.830, 0.607]
    table['HeadArmsTrunk'] = [0.678, 0.626, 0.374, 0.496, 0.798, 0.621]

    out = dict()
    try:
        out['Mass'] = table[segment_name][0] * total_mass
        out['COMProximalRatio'] = table[segment_name][1]
        out['COMDistalRatio'] = table[segment_name][2]
        out['GyrationCOMRatio'] = table[segment_name][3]
        out['GyrationProximalRatio'] = table[segment_name][4]
        out['GyrationDistalRatio'] = table[segment_name][5]
        return out
    except KeyError:
        raise ValueError(f'The segment "{segment_name}" is not available.')


@unstable(listing)
def calculate_proximal_wrench(
        ts: TimeSeries, inertial_constants: Dict[str, float]) -> TimeSeries:
    """
    Calculate the proximal wrench based on a TimeSeries.

    Warning
    -------
    This method is experimental and has not been strongly validated yet.


    This function is based on R. Dumas, R. Aissaoui, and J. A. De Guise,
    "A 3D generic inverse dynamic method using wrench notation and quaternion
    algebra,” Comput Meth Biomech Biomed Eng, vol. 7, no. 3, pp. 159–166, 2004.

    Parameters
    ----------
    ts
        A TimeSeries with the following data keys:

        - ProximalJointPosition (Nx4)
        - DistalJointPosition (Nx4)
        - ForceApplicationPosition (Nx4)
        - DistalForces (Nx4)
        - DistalMoments (Nx4)

    inertial_constants
        A dict that contains the following keys:

        - Mass': Mass of the segment, in kg.
        - COMProximalRatio': Distance between the segment's center
          of mass and the proximal joint, as a ratio of the
          distance between both joints.
        - 'GyrationCOMRatio': Radius of gyration around the segment's
          center of mass, as a ratio of the distance between
          both joints.

        This dict may be generated using the get_anthropometrics function.

    Returns
    -------
    TimeSeries
        A copy of the input timeseries plus these extra data keys:

        - 'ProximalForces' (Nx4)
        - 'ProximalMoments' (Nx4)
    """
    ts = ts.copy()

    n_frames = ts.time.shape[0]

    ts.data['ProximalToDistalJointDistance'] = (
        ts.data['DistalJointPosition'] -
        ts.data['ProximalJointPosition'])

    ts.data['RadiusOfGyration'] = (
        inertial_constants['GyrationCOMRatio'] *
        ts.data['ProximalToDistalJointDistance'])

    # Center of mass position and acceleration
    ts.data['CenterOfMassPosition'] = (
        inertial_constants['COMProximalRatio'] *
        ts.data['ProximalToDistalJointDistance'] +
        ts.data['ProximalJointPosition'])

    ts_com = ts.get_subset('CenterOfMassPosition')
    ts_acc = kineticstoolkit.filters.savgol(
        ts_com, window_length=21, poly_order=2, deriv=2)
    ts.data['CenterOfMassAcceleration'] = ts_acc.data['CenterOfMassPosition']

    # Rotation angle, velocity and acceleration
    segment_angle_x = np.arctan2(
        ts.data['ProximalToDistalJointDistance'][:, 2],
        ts.data['ProximalToDistalJointDistance'][:, 1])
    segment_angle_y = np.arctan2(
        ts.data['ProximalToDistalJointDistance'][:, 2],
        ts.data['ProximalToDistalJointDistance'][:, 0])
    segment_angle_z = np.arctan2(
        ts.data['ProximalToDistalJointDistance'][:, 1],
        ts.data['ProximalToDistalJointDistance'][:, 0])
    ts.data['Angle'] = np.concatenate((
        segment_angle_x[:, np.newaxis],
        segment_angle_y[:, np.newaxis],
        segment_angle_z[:, np.newaxis]), axis=1)

    ts_angle = ts.get_subset('Angle')
    ts_angvel = kineticstoolkit.filters.savgol(
        ts_angle, window_length=21, poly_order=2, deriv=1)
    ts_angacc = kineticstoolkit.filters.savgol(
        ts_angle, window_length=21, poly_order=2, deriv=2)
    ts.data['AngularVelocity'] = ts_angvel.data['Angle']
    ts.data['AngularAcceleration'] = ts_angacc.data['Angle']

    # Forces line of the wrench equation (16)
    a_i = ts.data['CenterOfMassAcceleration'][:, 0:3]
    g = np.array([0, -9.81, 0])
    F_i_minus_1 = ts.data['DistalForces'][:, 0:3]

    # Moments line of the wrench equation (16)
    c_i = (ts.data['CenterOfMassPosition'][:, 0:3] -
           ts.data['ProximalJointPosition'][:, 0:3])
    d_i = (ts.data['ForceApplicationPosition'] -
           ts.data['ProximalJointPosition'])[:, 0:3]

    segment_mass = inertial_constants['Mass']
    I_i_temp = segment_mass * ts.data['RadiusOfGyration'][:, 0:3] ** 2
    # Diagonalize I_i:
    I_i = np.zeros((n_frames, 3, 3))
    I_i[:, 0, 0] = I_i_temp[:, 0]
    I_i[:, 1, 1] = I_i_temp[:, 1]
    I_i[:, 2, 2] = I_i_temp[:, 2]

    alpha_i = ts.data['AngularAcceleration']
    omega_i = ts.data['AngularVelocity']

    M_i_minus_1 = ts.data['DistalMoments'][:, 0:3]

    # Calculation of the proximal wrench
    proximal_wrench = np.zeros((n_frames, 6, 1))
    for i_frame in range(n_frames):

        skew_symmetric_c_i = np.array([
            [0, -c_i[i_frame, 2], c_i[i_frame, 1]],
            [c_i[i_frame, 2], 0, -c_i[i_frame, 0]],
            [-c_i[i_frame, 1], c_i[i_frame, 0], 0]])

        skew_symmetric_d_i = np.array([
            [0, -d_i[i_frame, 2], d_i[i_frame, 1]],
            [d_i[i_frame, 2], 0, -d_i[i_frame, 0]],
            [-d_i[i_frame, 1], d_i[i_frame, 0], 0]])

        matrix_1 = np.block(
            [[segment_mass * np.eye(3), np.zeros((3, 3))],
             [segment_mass * skew_symmetric_c_i, I_i[i_frame]]])

        matrix_2 = np.block([a_i[i_frame] - g, alpha_i[i_frame]])
        matrix_2 = matrix_2[:, np.newaxis]  # Convert 1d to column vector

        matrix_3 = np.block([
            np.zeros(3),
            np.cross(omega_i[i_frame], I_i[i_frame] @ omega_i[i_frame])])
        matrix_3 = matrix_3[:, np.newaxis]  # Convert 1d to column vector

        matrix_4 = np.block([
            [np.eye(3), np.zeros((3, 3))],
            [skew_symmetric_d_i, np.eye(3)]])

        matrix_5 = np.block([F_i_minus_1[i_frame], M_i_minus_1[i_frame]])
        matrix_5 = matrix_5[:, np.newaxis]  # Convert 1d to column vector

        proximal_wrench[i_frame] = (
            matrix_1 @ matrix_2 + matrix_3 + matrix_4 @ matrix_5)

    # Initialize to a series of vectors of length 4
    ts.data['ProximalForces'] = np.zeros((n_frames, 4))
    ts.data['ProximalMoments'] = np.zeros((n_frames, 4))
    # Assign the 3 first components of the vectors
    ts.data['ProximalForces'][:, 0:3] = proximal_wrench[:, 0:3, 0]
    ts.data['ProximalMoments'][:, 0:3] = proximal_wrench[:, 3:6, 0]

    return ts


def __dir__():
    return listing

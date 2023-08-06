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
Provide functions to process kinetic data from instrumented wheelchair wheels.
"""

__author__ = "Félix Chénier"
__copyright__ = "Copyright (C) 2020 Félix Chénier"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"


import kineticstoolkit.filters as filters
import kineticstoolkit.cycles as cycles
from kineticstoolkit import TimeSeries
from kineticstoolkit.decorators import stable, unstable, private, dead

import numpy as np
from numpy import sin, cos, pi
import pandas as pd
import warnings
import struct  # to unpack binary data from SmartWheels' txt files
from typing import Union, Optional, List


listing = []  # type: List[str]


@stable(listing)
def read_file(filename: str, /, file_format: str = '') -> TimeSeries:
    """
    Read a file containing pushrim kinetics data.

    Parameters
    ----------
    filename
        Name of the file to open
    file_format
        Format of the file. Can be either:

        - 'smartwheel' (SmartWheel CSV file)
        - 'smartwheeltxt' (SmartWheel SD-Card TXT file)
        - 'racingwheel' (will change)

    """
    if file_format == '':
        warnings.warn("file_format will need to be explicitely specified in "
                      "future versions. Now using 'smartwheel'.",
                      FutureWarning)
        file_format = 'smartwheel'

    if file_format == 'smartwheel':

        dataframe = pd.read_csv(filename, delimiter=None, header=None)
        if dataframe.shape[1] == 1:  # Retry with ; as separator
            dataframe = pd.read_csv(filename, delimiter=';', header=None)

        data = dataframe.to_numpy()
        index = data[:, 1]
        time = np.arange(0, len(index)) / 240
        channels = data[:, 6:12]
        forces = data[:, 18:21]
        moments = data[:, 21:24]
        angle_deg = data[:, 3]
        angle_rad = np.unwrap(np.deg2rad(angle_deg))

        ts = TimeSeries(time=time)

        ts.data['Index'] = index
        ts.data['Channels'] = channels
        ts.data['Forces'] = np.block([[forces, np.zeros((len(index), 1))]])
        ts.data['Moments'] = np.block([[moments, np.zeros((len(index), 1))]])
        ts.data['Angle'] = angle_rad

        ts.add_data_info('Channels', 'Unit', 'raw')
        ts.add_data_info('Forces', 'Unit', 'N')
        ts.add_data_info('Moments', 'Unit', 'Nm')
        ts.add_data_info('Angle', 'Unit', 'rad')

    elif file_format == 'racingwheel':

        dataframe = pd.read_csv(filename, delimiter=',')
        data = dataframe.to_numpy()
        time = data[:, 0]
        channels = data[:, 1:7]
        battery = data[:, 8]

        ts = TimeSeries(time=time)

        ts.data['Channels'] = channels
        ts.add_data_info('Channels', 'Unit', 'raw')

        ts.data['Battery'] = battery
        ts.add_data_info('Battery', 'Unit', 'raw')

    elif file_format == 'smartwheeltxt':

        data = {'ch1': [], 'ch2': [], 'ch3': [],
                'ch4': [], 'ch5': [], 'ch6': [], 'angle_ticks': []}

        length = 0
        with open(filename, 'rb') as fid:

            while True:
                try:
                    _ = fid.read(2)
                    data['ch1'].append(struct.unpack('h', fid.read(2))[0])
                    data['ch2'].append(struct.unpack('h', fid.read(2))[0])
                    data['ch3'].append(struct.unpack('h', fid.read(2))[0])
                    data['ch4'].append(struct.unpack('h', fid.read(2))[0])
                    data['ch5'].append(struct.unpack('h', fid.read(2))[0])
                    data['ch6'].append(struct.unpack('h', fid.read(2))[0])
                    data['angle_ticks'].append(
                        struct.unpack('i', fid.read(4))[0])
                    _ = fid.read(8)
                    length += 1
                except Exception:
                    break

        ch1 = np.array(data['ch1'][1:length])  # Remove 1st sample to be
        ch2 = np.array(data['ch2'][1:length])  # consistent with CSV file
        ch3 = np.array(data['ch3'][1:length])
        ch4 = np.array(data['ch4'][1:length])
        ch5 = np.array(data['ch5'][1:length])
        ch6 = np.array(data['ch6'][1:length])
        angle_ticks = np.array(data['angle_ticks'][1:length])

        # Keep only 12 least significant bytes
        ch1 = np.mod(ch1, 2 ** 12)
        ch2 = np.mod(ch2, 2 ** 12)
        ch3 = np.mod(ch3, 2 ** 12)
        ch4 = np.mod(ch4, 2 ** 12)
        ch5 = np.mod(ch5, 2 ** 12)
        ch6 = np.mod(ch6, 2 ** 12)

        # Convert angle in radian
        angle = angle_ticks / 4096 * 2 * np.pi

        ts = TimeSeries(
            time=np.linspace(0, (length - 1) / 240, length - 1))
        ts.data['Channels'] = np.concatenate(
            [ch1[:, np.newaxis],
             ch2[:, np.newaxis],
             ch3[:, np.newaxis],
             ch4[:, np.newaxis],
             ch5[:, np.newaxis],
             ch6[:, np.newaxis]], axis=1)
        ts.data['Angle'] = angle

        ts.add_data_info('Channels', 'Unit', 'raw')
        ts.add_data_info('Angle', 'Unit', 'rad')

    else:
        raise ValueError('Unknown file format.')

    return ts


@unstable(listing)
def find_recovery_indices(Mz: np.ndarray, /) -> np.ndarray:
    """
    Find recovery indices based on a vector of propulsion moments.

    This function analyzes the Mz moments to find which data correspond to
    pushes and which data correspond to recoveries. The method is very
    conservative on what could be considered as a recovery, so that every
    index returned by this function is almost certain to correspond to a
    recovery. This function is used by `pushrimkinetics.remove_sinusoids`
    to identify the instants with no hand contact. It should not be used to
    isolate the push and recovery phases (use `ktk.cycles.detect_cycles()`
    instead).

    Parameters
    ----------
    Mz
        Array that contains the propulsion moments in Nm.

    Returns
    -------
    np.ndarray
        Array of bools where each True represents recovery.

    See Also
    --------
    ktk.cycles.detect_cycles

    """
    Mz = Mz.copy()

    threshold = 2.24  # (Nm): max tolerance for the remaining values.

    while np.nanmax(Mz) - np.nanmin(Mz) > threshold:

        # Remove 1% of data that are the farthest to the median:

        # Sort data
        index_to_remove = np.argsort(np.abs(Mz - np.nanmedian(Mz)))
        sorted_Mz = Mz[index_to_remove]
        index_to_remove = index_to_remove[~np.isnan(sorted_Mz)]

        # Remove the 1% upper.
        index_to_remove = index_to_remove[
                int(0.99*len(index_to_remove))-1:]

        # Assign nan to these data
        Mz[index_to_remove] = np.nan

    index = ~np.isnan(Mz)

    return index


@stable(listing)
def remove_offsets(
        kinetics: TimeSeries,
        baseline_kinetics: Optional[TimeSeries] = None
        ) -> TimeSeries:
    """
    Remove dynamic offsets in forces and moments.

    Parameters
    ----------
    kinetics
        TimeSeries that contains at least Forces, Moments and Angle data.
    baseline_kinetics
        Optional. TimeSeries that contains at least Forces and Moments data.
        This TimeSeries contains a baseline trial, where the wheelchair must be
        pushed by an operator and where no external force must be applied on
        the pushrims. If no baseline is provided, the baseline is calculated
        based on a detection of recoveries in the supplied kinetics
        TimeSeries.

    Returns
    -------
    TimeSeries
        A copy of the input TimeSeries, where sinusoids are removed from
        Forces and Moments data.

    References
    ----------
    F. Chénier, R. Aissaoui, C. Gauthier, and D. H. Gagnon,
    "Wheelchair pushrim kinetics measurement: A method to cancel
    inaccuracies due to pushrim weight and wheel camber," Medical
    Engineering and Physics, vol. 40, pp. 75--86, 2017.

    """
    kinetics = kinetics.copy()

    if baseline_kinetics is None:
        # Create baseline kinetics.
        recovery_index = find_recovery_indices(kinetics.data['Moments'][:, 2])
        f_ofs = np.hstack((kinetics.data['Forces'][recovery_index, 0:3],
                           kinetics.data['Moments'][recovery_index, 0:3]))
        theta_baseline = kinetics.data['Angle'][recovery_index]

    else:
        # Use baseline kinetics.
        f_ofs = np.hstack((baseline_kinetics.data['Forces'][:, 0:3],
                           baseline_kinetics.data['Moments'][:, 0:3]))
        theta_baseline = baseline_kinetics.data['Angle'][:]

    # Do the regression
    theta_baseline = theta_baseline[:, np.newaxis]
    q = np.hstack((
            np.sin(theta_baseline),
            np.cos(theta_baseline),
            np.ones((len(theta_baseline), 1))
            ))
    A = np.linalg.lstsq(q, f_ofs, rcond=None)
    A = A[0]

    # Apply the regression to forces and moments
    theta = kinetics.data['Angle']
    theta = theta[:, np.newaxis]

    f = np.hstack((kinetics.data['Forces'][:, 0:3],
                   kinetics.data['Moments'][:, 0:3]))

    q = np.hstack((
            np.sin(theta),
            np.cos(theta),
            np.ones((len(theta), 1))
            ))

    f = f - q @ A

    # Make the output timeseries
    kinetics.data['Forces'][:, 0:3] = f[:, 0:3]
    kinetics.data['Moments'][:, 0:3] = f[:, 3:6]

    return kinetics


@stable(listing)
def calculate_forces_and_moments(
        kinetics: TimeSeries, /,
        gains: Union[np.ndarray, str],
        offsets: np.ndarray = np.zeros((6)), *,
        transducer: str = 'force_cell',
        reference_frame: str = 'wheel') -> TimeSeries:
    """
    Calculate pushrim forces and moments based on raw channel values.

    For standard force cells (with each channel being a raw value
    corresponding to Fx, Fy, Fz, Mx, My, Mz, respectively), calculates
    the forces and moments using a sensitivity matrix (gains) and an
    offset vector (offsets):

    ``[Fx, Fy, Fz, Mx, My, Mz] = gains @ channels + offsets``

    For SmartWheel, calculates the forces and moments using a gain
    vector (gains) and an offset vector (offsets).

    Parameters
    ----------
    kinetics
        Input TimeSeries that must contain a 'Channels' key in its data dict.
    gains
        6x6 gain matrix (force_cell) or gain vector of length 6 (smartwheel).
    offsets
        Optional. Offset vector of length 6.
    transducer
        Optional. 'force_cell' or 'smartwheel'.
    reference_frame
        Optional. 'wheel' or 'hub'. 'wheel' to report the forces and moments
        into the local wheel's reference frame; 'hub' to compensate for the
        wheel rotation and match the reference frame used by the SmartWheel:
        x anteroposterior, y in the wheel plane, upward for non-camberred
        wheels, and z perpendicular to the wheel plane, outward.

    Returns
    -------
    TimeSeries
        A copy of the input TimeSeries, with the added 'Forces'
        and 'Moments' data keys.

    Note
    ----
    Some calibration matrices are provided as examples in the
    ``pushrimkinetics.CALIBRATION_MATRICES`` dictionary. This dictionary can
    be used directly using dict unpacking. For example::

        ktk.pushrimkinetics.calculate_force_and_moments(
            kinetics,
            **ktk.pushrimkinetics.CALIBRATION_MATRICES['SmartWheel_123'],
            reference_frame='level'
        )

    """
    # Check if this is the old form and call this deprecated form.
    if isinstance(gains, str):
        warnings.warn("This old signature won't be supported in future.",
                      FutureWarning)
        return _old_calculate_forces_and_moments(kinetics, gains)

    # Calculate the forces and moments and add to the output
    if transducer == 'smartwheel':

        # Calculate the rotation angle to apply to the calculated kinetics
        if reference_frame == 'wheel':
            theta = 0
        elif reference_frame == 'hub':
            theta = kinetics.data['Angle']
        else:
            raise ValueError("reference_frame must be 'wheel' or 'hub'")

        # Extract channels and angle
        ch = kinetics.data['Channels'] - 2048

        # Calculate the forces and moments
        Fx = gains[0] * (
            ch[:, 0] * sin(theta) +
            ch[:, 2] * sin(theta + 2 * pi / 3) +
            ch[:, 4] * sin(theta + 4 * pi / 3)) + offsets[0]

        Fy = gains[1] * (
            ch[:, 0] * cos(theta) +
            ch[:, 2] * cos(theta + 2 * pi / 3) +
            ch[:, 4] * cos(theta + 4 * pi / 3)) + offsets[1]

        Fz = gains[2] * (ch[:, 1] + ch[:, 3] + ch[:, 5]) + offsets[2]

        Mx = gains[3] * (
            ch[:, 1] * sin(theta) +
            ch[:, 3] * sin(theta + 2 * pi / 3) +
            ch[:, 5] * sin(theta + 4 * pi / 3)) + offsets[3]

        My = gains[4] * (
            ch[:, 1] * cos(theta) +
            ch[:, 3] * cos(theta + 2 * pi / 3) +
            ch[:, 5] * cos(theta + 4 * pi / 3)) + offsets[4]

        Mz = gains[5] * (ch[:, 0] + ch[:, 2] + ch[:, 4]) + offsets[5]
        forces_moments = np.block([Fx[:, np.newaxis],
                                   Fy[:, np.newaxis],
                                   Fz[:, np.newaxis],
                                   Mx[:, np.newaxis],
                                   My[:, np.newaxis],
                                   Mz[:, np.newaxis]])

    elif transducer == 'force_cell':

        # Calculate the rotation angle to apply to the calculated kinetics
        if reference_frame == 'wheel':
            theta = 0
        elif reference_frame == 'hub':
            raise NotImplementedError("hub reference_frame not implemented yet"
                                      "for force_cell transducers.")
        else:
            raise ValueError("reference_frame must be 'wheel' or 'hub'")

        n_frames = kinetics.data['Channels'].shape[0]

        forces_moments = np.empty((n_frames, 6))
        for i_frame in range(n_frames):
            forces_moments[i_frame] = (gains @
                                       kinetics.data['Channels'][i_frame] +
                                       offsets)

    # Format these data in the output timeseries
    kinetics = kinetics.copy()

    kinetics.data['Forces'] = np.concatenate(
        [forces_moments[:, 0:3], np.zeros((forces_moments.shape[0], 1))],
        axis=1)
    kinetics.add_data_info('Forces', 'Unit', 'N')

    kinetics.data['Moments'] = np.concatenate(
        [forces_moments[:, 3:6], np.zeros((forces_moments.shape[0], 1))],
        axis=1)
    kinetics.add_data_info('Moments', 'Unit', 'Nm')

    return(kinetics)


@stable(listing)
def calculate_velocity(tsin: TimeSeries, /) -> TimeSeries:
    """
    Calculate velocity based on wheel angle.

    The velocity is calculated by deriving the angle using a 2nd order
    Savitzky-Golay filter of length 21. This filter has been experimentally
    validated to maximize the signal-to-noise ratio for a SmartWheel recording
    at 240 Hz. This function may change signature in the future to include
    other filtering options. To manually get the velocity using a custom
    filter, please see the ``ktk.filters`` module.

    Parameters
    ----------
    tsin
        TimeSeries that contains at least the data key 'Angle'.

    Returns
    -------
    TimeSeries
        	A copy of the TimeSeries with the added data key 'Velocity'.

    See Also
    --------
    ktk.filters.butter : Butterworth filter for TimeSeries
    ktk.filters.savgol : Savitsky-golay filter for TimeSeries
    ktk.filters.deriv : Derivative filter for TimeSeries

    """
    tsangle = TimeSeries()
    tsangle.time = tsin.time
    tsangle.data['Angle'] = tsin.data['Angle']
    tsvelocity = filters.savgol(tsangle, window_length=21,
                                    poly_order=2, deriv=1)
    tsout = tsin.copy()
    tsout.data['Velocity'] = tsvelocity.data['Angle']
    tsout.add_data_info('Velocity', 'Unit',
                        tsout.data_info['Angle']['Unit'] + '/s')
    return tsout


@stable(listing)
def calculate_power(tsin: TimeSeries, /) -> TimeSeries:
    """
    Calculate power based on wheel velocity and moment.

    Parameters
    ----------
    tsin
        TimeSeries that contains at least the data keys 'Velocity' and
        'Moments'. The units must be consistent (e.g., rad/s and Nm)

    Returns
    -------
    TimeSeries
        A copy of the TimeSeries with the added data key 'Power'.

    """
    tsout = tsin.copy()
    tsout.data['Power'] = (tsout.data['Velocity'] *
              tsout.data['Moments'][:,2])
    tsout.add_data_info('Power', 'Unit', 'W')
    return tsout


#--- Deprecated functions ---#
@private(listing)
def _old_calculate_forces_and_moments(
        kinetics: TimeSeries, calibration_id: str, /) -> TimeSeries:
    """
    Calculate pushrim forces and moments based on raw channel values.

    Deprecated since October 2020.

    Parameters
    ----------
    kinetics
        Input TimeSeries that must contain a 'Channels' key in its data dict.
    calibration_id
        Calibration identifier, resulting from factory or custom calibration.
        Available values are:

        - 'PATHOKIN-93':  PATHOKIN 24" SmartWheel, Serial #93
        - 'PATHOKIN-94':  PATHOKIN 24" SmartWheel, Serial #94
        - 'LIO-123':      LIO 24" SmartWheel, Serial #123
        - 'LIO-124':      LIO 24" SmartWheel, Serial #124
        - 'LIO-125':      LIO 24" SmartWheel, Serial #125
        - 'LIO-126':      LIO 26" SmartWheel, Serial #126
        - 'S18-126':      PATHOKIN Summer 2018, Serial 126 - 26"
        - 'S18-179':      PATHOKIN Summer 2018, Serial 179 - 25"
        - 'S18-180':      PATHOKIN Summer 2018, Serial 180 - 25"
        - 'S18-181':      PATHOKIN Summer 2018, Serial 181 - 26"
        - 'S18-Racing-Prototype1': Racing wheel prototype
        - 'W20-Racing-Prototype1': Racing wheel proto with calibration matrix

    Returns
    -------
    TimeSeries
		A copy of the input TimeSeries, with the added 'Forces'
		and 'Moments' data keys.

    """

    # Get the gains and offsets based on calibration id
    if calibration_id == 'PATHOKIN-93':
        forcecell = 'smartwheel'
        gains = [-0.1080, 0.1080, 0.0930, 0.0222, -0.0222, 0.0234999]
        offsets = [0.0, 10.0, 0.0, 0.0, 0.0, 0.0]

    elif calibration_id == 'PATHOKIN-94':
        forcecell = 'smartwheel'
        gains = [-0.1070, 0.1070, 0.0960, 0.0222, -0.0222, 0.0230]
        offsets = [0.0, 10.0, 0.0, 0.0, 0.0, 0.0]

    elif calibration_id == 'LIO-123':
        forcecell = 'smartwheel'
        gains = [-0.106, 0.106, 0.094, 0.022, -0.022, 0.0234999]
        offsets = [0.0, 10.0, 0.0, 0.0, 0.0, 0.0]

    elif calibration_id == 'LIO-124':
        forcecell = 'smartwheel'
        gains = [-0.106, 0.106, 0.0949999, 0.0215, -0.0215, 0.0225]
        offsets = [0.0, 10.0, 0.0, 0.0, 0.0, 0.0]

    elif calibration_id == 'LIO-125':
        forcecell = 'smartwheel'
        gains = [-0.104, 0.104, 0.0979999, 0.0215, -0.0215, 0.0225]
        offsets = [0.0, 10.0, 0.0, 0.0, 0.0, 0.0]

    elif calibration_id == 'LIO-126':
        forcecell = 'smartwheel'
        gains = [-0.1059999, 0.1059999, 0.086, 0.021, -0.021, 0.023]
        offsets = [0.0, 10.0, 0.0, 0.0, 0.0, 0.0]

    elif calibration_id == 'S18-126':
        forcecell = 'smartwheel'
        gains = [-0.1083, 0.1109, 0.0898, 0.0211, -0.0194, 0.0214]
        offsets = [0.0, 10.0, 0.0, 0.0, 0.0, 0.0]

    elif calibration_id == 'S18-179':
        forcecell = 'smartwheel'
        gains = [-0.1399, 0.1091, 0.0892, 0.0240, -0.0222, 0.0241]
        offsets = [0.0, 10.0, 0.0, 0.0, 0.0, 0.0]

    elif calibration_id == 'S18-180':
        forcecell = 'smartwheel'
        gains = [-0.1069, 0.1091, 0.0932, 0.0240, -0.0226, 0.0238]
        offsets = [0.0, 10.0, 0.0, 0.0, 0.0, 0.0]

    elif calibration_id == 'S18-181':
        forcecell = 'smartwheel'
        gains = [-0.1152, 0.1095, 0.0791, 0.0229, -0.0197, 0.0220]
        offsets = [0.0, 10.0, 0.0, 0.0, 0.0, 0.0]

    elif calibration_id == 'S18-Racing-Prototype1':
        forcecell = 'forcecell'
        gains = [-0.0314, -0.0300, 0.0576, 0.0037, 0.0019, -0.0019]
        offsets = [-111.3874, -63.3298, -8.6596, 1.8089, 1.5761, -0.8869]

    elif calibration_id == 'S20-Racing-Prototype1':
        forcecell = 'matrix'
        # Gains from calibration matrix
        board_gains = np.array([-2., -2., -2., -2., -4., -4.])
        adc_gains = (2.**15) / 10
        gains = (np.array([
            [201.027, 1.387, 2.077, -3.852, -1.837, -1.519],
            [-0.840, 201.396, 2.119, 0.083, -6.877, 4.482],
            [-1.935, -1.643, 402.286, 1.687, 0.897, -23.616],
            [0.213, 0.122, 0.120, 25.190, -0.013, 0.147],
            [-0.072, 0.286, 0.076, 0.012, 25.430, 0.146],
            [0.016, -0.015, 0.046, -0.099, -0.076, 25.206]]) /
            adc_gains / board_gains)
        # Offsets from home calibration (S18-Racing-Prototype1)
        offsets = [-111.3874, -63.3298, -8.6596, 1.8089, 1.5761, -0.8869]

    else:
        raise ValueError('This calibration ID is not available.')

    gains = np.array(gains)
    offsets = np.array(offsets)

    # Calculate the forces and moments and add to the output
    if forcecell == 'smartwheel':

        # Extract channels and angle
        ch = kinetics.data['Channels'] - 2048
        theta = kinetics.data['Angle']

        # Calculate the forces and moments
        Fx = gains[0] * (
            ch[:, 0] * sin(theta) +
            ch[:, 2] * sin(theta + 2 * pi / 3) +
            ch[:, 4] * sin(theta + 4 * pi / 3)) + offsets[0]

        Fy = gains[1] * (
            ch[:, 0] * cos(theta) +
            ch[:, 2] * cos(theta + 2 * pi / 3) +
            ch[:, 4] * cos(theta + 4 * pi / 3)) + offsets[1]

        Fz = gains[2] * (ch[:, 1] + ch[:, 3] + ch[:, 5]) + offsets[2]

        Mx = gains[3] * (
            ch[:, 1] * sin(theta) +
            ch[:, 3] * sin(theta + 2 * pi / 3) +
            ch[:, 5] * sin(theta + 4 * pi / 3)) + offsets[3]

        My = gains[4] * (
            ch[:, 1] * cos(theta) +
            ch[:, 3] * cos(theta + 2 * pi / 3) +
            ch[:, 5] * cos(theta + 4 * pi / 3)) + offsets[4]

        Mz = gains[5] * (ch[:, 0] + ch[:, 2] + ch[:, 4]) + offsets[5]
        forces_moments = np.block([Fx[:, np.newaxis],
                                   Fy[:, np.newaxis],
                                   Fz[:, np.newaxis],
                                   Mx[:, np.newaxis],
                                   My[:, np.newaxis],
                                   Mz[:, np.newaxis]])

    elif forcecell == 'forcecell':

        forces_moments = gains * kinetics.data['Channels'] + offsets

    elif forcecell == 'matrix':

        n_frames = kinetics.data['Channels'].shape[0]

        forces_moments = np.empty((n_frames, 6))
        for i_frame in range(n_frames):
            forces_moments[i_frame] = (gains @
                                       kinetics.data['Channels'][i_frame] +
                                       offsets)

    # Format these data in the output timeseries
    kinetics = kinetics.copy()

    kinetics.data['Forces'] = np.concatenate(
        [forces_moments[:, 0:3], np.zeros((forces_moments.shape[0], 1))],
        axis=1)
    kinetics.add_data_info('Forces', 'Unit', 'N')

    kinetics.data['Moments'] = np.concatenate(
        [forces_moments[:, 3:6], np.zeros((forces_moments.shape[0], 1))],
        axis=1)
    kinetics.add_data_info('Moments', 'Unit', 'Nm')

    return(kinetics)


@dead(listing)
def detect_pushes(
        tsin: TimeSeries, /, *,
        push_threshold: float = 5.0,
        recovery_threshold: float = 2.0,
        min_push_time: float = 0.1,
        min_push_force: float = 30.0) -> TimeSeries:
    """
    Detect pushes and recoveries automatically.

    Deprecated since October 2020. Please use ktk.cycles.detect_cycles instead.

    Parameters
    ----------
    tsin
        Input TimeSeries that must contain a 'Forces' key in its data dict.
    push_threshold
        Optional. The total force over which a push phase is triggered, in
        newton.
    recovery_threshold
        Optional. The total force under which a recovery phase is triggered,
        in newton.
    min_push_time
        Optional. The minimum time required for a push time, in seconds.
        Detected pushes that last less than this minimum time are removed from
        the push analysis.
    min_recovery_time
        Optional. The minimum time required for a recovery time, in seconds.
        Detected recoveries that last less than this minimum time are removed
        from the push analysis.
    min_push_force
        Optional. The minimum total push force in N under which the detected
        push is discarded. For example, if the user puts their hands on the
        pushrim before starting propelling, this may be detected as a push.
        Using a minimum push force removes these misdetected pushes.

    Returns
    -------
    TimeSeries
        A copy of tsin with the following added events:
        - 'push'
        - 'recovery'

    """
    # Calculate the total force
    f_tot = np.sqrt(np.sum(tsin.data['Forces']**2, axis=1))
    ts_force = TimeSeries(time=tsin.time, data={'Ftot': f_tot})
    ts_force.events = tsin.events

    # Smooth the total force to avoid detecting pushes on glitches
    ts_force = filters.smooth(ts_force, 11)

    # Remove the median if it existed
    ts_force.data['Ftot'] = \
            ts_force.data['Ftot'] - np.median(ts_force.data['Ftot'])

    # Find the pushes
    ts_force = cycles.detect_cycles(
        ts_force, 'Ftot',
        event_name1='push',
        event_name2='recovery',
        threshold1=push_threshold,
        threshold2=recovery_threshold,
        min_duration1=min_push_time,
        min_peak_height1=min_push_force)

    # Form the output timeseries
    tsout = tsin.copy()
    tsout.events = ts_force.events

    return tsout


@dead(listing)
def remove_sinusoids(
        kinetics: TimeSeries,
        baseline_kinetics: Optional[TimeSeries] = None
        ) -> TimeSeries:
    """
    Deprecated since October 2020. Please use
    ktk.pushrimkinetics.remove_offsets instead.
    """
    return remove_offsets(kinetics, baseline_kinetics)


#--- Some calibration matrices ---#
CALIBRATION_MATRICES = {}
CALIBRATION_MATRICES['SmartWheel_93'] = {
    'gains': np.array([-0.1080, 0.1080, 0.0930, 0.0222, -0.0222, 0.0234999]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
    }
CALIBRATION_MATRICES['SmartWheel_94'] = {
    'gains': np.array([-0.1070, 0.1070, 0.0960, 0.0222, -0.0222, 0.0230]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
    }
CALIBRATION_MATRICES['SmartWheel_123'] = {
    'gains': np.array([-0.106, 0.106, 0.094, 0.022, -0.022, 0.0234999]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
    }
CALIBRATION_MATRICES['SmartWheel_124'] = {
    'gains': np.array([-0.106, 0.106, 0.0949999, 0.0215, -0.0215, 0.0225]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
    }
CALIBRATION_MATRICES['SmartWheel_125'] = {
    'gains': np.array([-0.104, 0.104, 0.0979999, 0.0215, -0.0215, 0.0225]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
    }
CALIBRATION_MATRICES['SmartWheel_126'] = {
    'gains': np.array([-0.1059999, 0.1059999, 0.086, 0.021, -0.021, 0.023]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
    }
CALIBRATION_MATRICES['SmartWheel_126_S18'] = {
    'gains': np.array([-0.1083, 0.1109, 0.0898, 0.0211, -0.0194, 0.0214]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
    }
CALIBRATION_MATRICES['SmartWheel_179_S18'] = {
    'gains': np.array([-0.1399, 0.1091, 0.0892, 0.0240, -0.0222, 0.0241]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
    }
CALIBRATION_MATRICES['SmartWheel_180_S18'] = {
    'gains': np.array([-0.1069, 0.1091, 0.0932, 0.0240, -0.0226, 0.0238]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
    }
CALIBRATION_MATRICES['SmartWheel_181_S18'] = {
    'gains': np.array([-0.1152, 0.1095, 0.0791, 0.0229, -0.0197, 0.0220]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
    }
CALIBRATION_MATRICES['MSA_Racing_1'] = {
    'gains': (np.array([
        [201.027, 1.387, 2.077, -3.852, -1.837, -1.519],
        [-0.840, 201.396, 2.119, 0.083, -6.877, 4.482],
        [-1.935, -1.643, 402.286, 1.687, 0.897, -23.616],
        [0.213, 0.122, 0.120, 25.190, -0.013, 0.147],
        [-0.072, 0.286, 0.076, 0.012, 25.430, 0.146],
        [0.016, -0.015, 0.046, -0.099, -0.076, 25.206]])  # Cell calibration
        / (2.**15) / 10  # ADC gains
        / np.array([-2., -2., -2., -2., -4., -4.])  # Board gains
        ),
    'offsets': [-111.3874, -63.3298, -8.6596, 1.8089, 1.5761, -0.8869],
    'transducer': 'force_cell',
    }


def __dir__():
    return listing

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

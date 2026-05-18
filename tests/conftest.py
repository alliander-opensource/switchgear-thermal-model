# SPDX-FileCopyrightText: Contributors to the Switchgear Thermal Model project
#
# SPDX-License-Identifier: MPL-2.0

import numpy as np
import pytest

from switchgear_thermal_model.schemas import InputProfile
from switchgear_thermal_model.switchgear import Switchgear


def datetime_array_seconds(start_time, dt_seconds):
    """Helper function to provide a datetime array with a given length."""
    return start_time + np.arange(100) * np.timedelta64(dt_seconds, "s")


@pytest.fixture
def static_load_array():
    """Fixture to provide a static load array for testing."""
    return np.full((1, 100), 3150)[0]


@pytest.fixture
def static_zero_load_array():
    """Fixture to provide a static zero load array for testing."""
    return np.full((1, 100), 0)[0]


@pytest.fixture
def cyclic_load_array():
    """Fixture to provide a sinusoidal load profile with 2 full periods per 100 samples (i.e. ~ 1 day)."""
    return 2150 + 2000 * np.sin(np.linspace(0, 4 * np.pi, 100))


@pytest.fixture
def start_time():
    """Fixture to provide a start time for testing."""
    return np.datetime64("2024-01-01T00:00")


@pytest.fixture
def datetime_array_15_minutes(start_time):
    """Fixture to provide a datetime array for testing."""
    return datetime_array_seconds(start_time, 60 * 15)


@pytest.fixture
def datetime_array_minute(start_time):
    """Fixture to provide a datetime array for testing."""
    return datetime_array_seconds(start_time, 60)


@pytest.fixture
def datetime_array_30_seconds(start_time):
    """Fixture to provide a datetime array for testing."""
    return datetime_array_seconds(start_time, 30)


@pytest.fixture
def datetime_array_10_seconds(start_time):
    """Fixture to provide a datetime array for testing."""
    return datetime_array_seconds(start_time, 10)


@pytest.fixture
def basic_switchgear():
    """Fixture to provide a basic switchgear for testing."""
    return Switchgear(rated_current=3150, measured_temperature_rise=75, temp_rise_exp=1.8, thermal_time_constant=90)


@pytest.fixture
def basic_amb_temp_array():
    """Fixture to provide a basic ambient temperature array for testing."""
    return np.full((1, 100), 20)[0]


@pytest.fixture
def varying_amb_temp_array():
    """Fixture to provide a varying ambient temperature array for testing."""
    return np.linspace(10, 30, 100)


@pytest.fixture
def basic_input_profile(datetime_array_minute, basic_amb_temp_array, static_load_array):
    """Fixture to provide a basic input profile for testing."""
    return InputProfile(
        datetime_index=datetime_array_minute,
        ambient_temperature_profile=basic_amb_temp_array,
        load_profile=static_load_array,
    )


@pytest.fixture
def basic_zero_load_input_profile(datetime_array_minute, basic_amb_temp_array, static_zero_load_array):
    """Fixture to provide a basic input profile with zero load for testing."""
    return InputProfile(
        datetime_index=datetime_array_minute,
        ambient_temperature_profile=basic_amb_temp_array,
        load_profile=static_zero_load_array,
    )


@pytest.fixture
def cyclic_load_input_profile(datetime_array_15_minutes, basic_amb_temp_array, cyclic_load_array):
    """Fixture to provide a periodic load input profile for testing."""
    return InputProfile(
        datetime_index=datetime_array_15_minutes,
        ambient_temperature_profile=basic_amb_temp_array,
        load_profile=cyclic_load_array,
    )


@pytest.fixture
def varying_amb_temp_input_profile(datetime_array_minute, varying_amb_temp_array, static_load_array):
    """Fixture to provide an input profile with a varying ambient temperature for testing."""
    return InputProfile(
        datetime_index=datetime_array_minute,
        ambient_temperature_profile=varying_amb_temp_array,
        load_profile=static_load_array,
    )

# SPDX-FileCopyrightText: Contributors to the Switchgear Thermal Model project
#
# SPDX-License-Identifier: MPL-2.0

import numpy as np
import pandas as pd
import pytest

from switchgear_thermal_model.schemas import InputProfile
from switchgear_thermal_model.switchgear import Switchgear
from switchgear_thermal_model.thermal_model import switchgear_temp

# Define some basic input parameters to pass to basic tests:


def test_for_expected_modelled_max_temperature(
    cyclic_load_input_profile: InputProfile, basic_switchgear: Switchgear
) -> None:
    """This integration test, tests if we get the expected temperature based on SGTM-version 1.1.2."""
    result = switchgear_temp(cyclic_load_input_profile, basic_switchgear)
    assert result.max() == pytest.approx(125.197, rel=1e-3)


def test_that_output_is_same_length_as_amb_temp_input(
    basic_input_profile: InputProfile, basic_switchgear: Switchgear
) -> None:
    """Test that the output is the same length as the input ambient temperature profile.

    NOTE: It seems to me that in the final implementation, this should be different, as it should depend on
    either dt or on the resolution of the load profile.
    """
    # Call the function
    result = switchgear_temp(basic_input_profile, basic_switchgear)

    # Assert the result is as expected
    assert len(result) == len(basic_input_profile.ambient_temperature_profile)


def test_that_output_temperature_behaves_appropriately_given_constant_amb_temp_and_reasonable_specs(
    basic_switchgear: Switchgear,
    basic_input_profile: InputProfile,
    basic_zero_load_input_profile: InputProfile,
    cyclic_load_input_profile: InputProfile,
) -> None:
    """Test that the output temperature is well-behaved.

    i.e. never drops below a (constant) ambient temperature and starts at ambient temperature.
    NOTE: This test relies on constant ambient temperature.
    """
    # Call the function
    for input_profile in [basic_input_profile, basic_zero_load_input_profile, cyclic_load_input_profile]:
        result = switchgear_temp(input_profile, basic_switchgear)

        # Assert the result is as expected
        assert result.iloc[0] == input_profile.ambient_temperature_profile[0]  # Initial temperature matches ambient
        assert np.min(result) >= np.max(
            input_profile.ambient_temperature_profile
        )  # CB temperature never drops below ambient


@pytest.mark.parametrize(
    "switchgear",
    [
        Switchgear(
            rated_current=3150,
            measured_temperature_rise=75,
            temp_rise_exp=50.0,
            thermal_time_constant=90,
        ),
        Switchgear(
            rated_current=3150,
            measured_temperature_rise=1000,
            temp_rise_exp=1.8,
            thermal_time_constant=90,
        ),
        Switchgear(
            rated_current=31500,
            measured_temperature_rise=75,
            temp_rise_exp=0.001,
            thermal_time_constant=900,
        ),
    ],
)
def test_that_output_never_exceeds_asymptote(switchgear: Switchgear, basic_input_profile: InputProfile) -> None:
    """Test that the output temperature is well-behaved, as bounded from by the asymptote.

    NOTE: This test relies on both a constant ambient temperature AND a constant load.
    The asymptote should be the temperature that a switchgear will EVENTUALLY reach
    given constant load and temperature.
    NOTE: it is assumed that initial switchgear temperature is greater than or equal to
    ambient temperature. This is such an edge case that no test was written.
    """
    asymptote_temp = switchgear.measured_temperature_rise * (
        (np.max(basic_input_profile.load_profile) / switchgear.rated_current) ** switchgear.temp_rise_exp
    ) + np.max(basic_input_profile.ambient_temperature_profile)

    result = switchgear_temp(basic_input_profile, switchgear)

    assert np.max(result) < asymptote_temp


def test_that_output_returns_series_with_datetime_index(
    basic_switchgear: Switchgear, basic_input_profile: InputProfile
) -> None:
    """Test that the output is a pandas Series with the correct datetime index."""
    result = switchgear_temp(basic_input_profile, basic_switchgear)

    assert isinstance(result, pd.Series)

    np.testing.assert_array_equal(result.index.values, basic_input_profile.datetime_index)


def test_that_initial_temperature_equals_first_ambient_temperature(
    basic_switchgear: Switchgear, varying_amb_temp_input_profile: InputProfile
) -> None:
    """Test that the initial modeled temperature equals the first ambient temperature value."""
    result = switchgear_temp(varying_amb_temp_input_profile, basic_switchgear)

    assert result.iloc[0] == varying_amb_temp_input_profile.ambient_temperature_profile[0]


def test_second_timestep_temperature_is_between_initial_and_asymptote(
    basic_switchgear: Switchgear, basic_input_profile: InputProfile
) -> None:
    """Test that the second timestep temperature is between the initial temperature and the asymptote."""
    result = switchgear_temp(basic_input_profile, basic_switchgear).array
    asymptote_temp = result[-1]  # Assuming the last value is close to the asymptote

    assert result[1] > result[0]  # Temperature should increase from initial to second timestep
    assert result[1] < asymptote_temp  # Temperature should be below asymptote at second timestep

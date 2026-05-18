# SPDX-FileCopyrightText: Contributors to the Switchgear Thermal Model project
#
# SPDX-License-Identifier: MPL-2.0

from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd
import pytest
from pandas import DatetimeIndex

from switchgear_thermal_model.schemas.input_profile import InputProfile


@pytest.mark.parametrize(
    "datetime_index, load_profile, ambient_temperature_profile",
    [
        (
            pd.date_range("2021-01-01 00:00:00", periods=3),
            [1, 2, 3],
            [1, 2, 3],
        ),
        (
            pd.date_range("2021-01-01 00:00:00", periods=3),
            np.array([1, 2, 3]),
            [1, 2, 3],
        ),
        (
            pd.date_range("2021-01-01 00:00:00", periods=3),
            pd.Series([1, 2, 3]),
            [1, 2, 3],
        ),
        (
            pd.date_range("2021-01-01 00:00:00", periods=3),
            pd.Series([1, 2, 3], index=pd.date_range("2021-01-01 00:00:00", periods=3)),
            [1, 2, 3],
        ),
        (
            np.array([datetime(2021, 1, 1, 0, 0, 0), datetime(2021, 1, 1, 0, 15, 0), datetime(2021, 1, 1, 0, 30, 0)]),
            [1, 2, 3],
            [1, 2, 3],
        ),
    ],
)
def test_input_profile_with_valid_inputs(
    datetime_index: DatetimeIndex, load_profile: list, ambient_temperature_profile: list
):
    """Test that InputProfile can be created from various valid input formats."""
    input_profile = InputProfile.create(
        datetime_index=datetime_index,
        load_profile=load_profile,
        ambient_temperature_profile=ambient_temperature_profile,
    )
    assert input_profile is not None


@pytest.mark.parametrize(
    "load_profile",
    [
        np.array([1, -2, 3]),
        np.array([1, 2, -3]),
    ],
)
def test_input_profile_rejects_negative_load_values(load_profile: np.ndarray):
    """Test that InputProfile rejects negative values in load_profile."""
    datetime_index = pd.date_range("2021-01-01 00:00:00", periods=3)
    ambient_temperature_profile = [1, 2, 3]

    with pytest.raises(ValueError, match="The load profile must not contain negative values"):
        InputProfile.create(
            datetime_index=datetime_index,
            load_profile=load_profile,
            ambient_temperature_profile=ambient_temperature_profile,
        )


def test_input_profile_rejects_mismatched_ambient_temperature_length():
    """Test that InputProfile rejects ambient_temperature_profile with mismatched length."""
    datetime_index = pd.date_range("2021-01-01 00:00:00", periods=3)
    load_profile = [1, 2, 3]
    ambient_temperature_profile = [1, 2]

    with pytest.raises(ValueError, match="The length of the profiles and index should be the same"):
        InputProfile.create(
            datetime_index=datetime_index,
            load_profile=load_profile,
            ambient_temperature_profile=ambient_temperature_profile,
        )


def test_input_profile_rejects_mismatched_load_profile_length():
    """Test that InputProfile rejects load_profile with mismatched length."""
    datetime_index = pd.date_range("2021-01-01 00:00:00", periods=3)
    load_profile = [1, 2]
    ambient_temperature_profile = [1, 2, 3]

    with pytest.raises(ValueError, match="The length of the profiles and index should be the same"):
        InputProfile.create(
            datetime_index=datetime_index,
            load_profile=load_profile,
            ambient_temperature_profile=ambient_temperature_profile,
        )


def test_input_profile_rejects_unsorted_datetime_index():
    """Test that InputProfile rejects unsorted datetime indices."""
    datetime_index = pd.to_datetime(["2021-01-01 00:00:00", "2021-01-01 00:15:00", "2021-01-01 00:05:00"])
    load_profile = [1, 2, 3]
    ambient_temperature_profile = [1, 2, 3]

    with pytest.raises(ValueError, match="The datetime index should be sorted."):
        InputProfile.create(
            datetime_index=datetime_index,
            load_profile=load_profile,
            ambient_temperature_profile=ambient_temperature_profile,
        )


@pytest.mark.parametrize(
    "datetime_index",
    [
        np.array(["a", "b", "c"]),
        {"a": 1, "b": 3, "c": 3},
    ],
)
def test_input_profile_rejects_invalid_datetime_format(datetime_index: Any):
    """Test that InputProfile rejects invalid datetime formats."""
    load_profile = [1, 2, 3]
    ambient_temperature_profile = [1, 2, 3]

    with pytest.raises(ValueError):
        InputProfile.create(
            datetime_index=datetime_index,
            load_profile=load_profile,
            ambient_temperature_profile=ambient_temperature_profile,
        )


def test_input_profile_rejects_dict_datetime_format():
    """Test that InputProfile rejects datetime conversion from dict."""
    datetime_index = {"a": 1, "b": 3, "c": 3}
    load_profile = [1, 2, 3]
    ambient_temperature_profile = [1, 2, 3]

    with pytest.raises(ValueError, match="Could not convert object to NumPy datetime"):
        InputProfile.create(
            datetime_index=datetime_index,
            load_profile=load_profile,
            ambient_temperature_profile=ambient_temperature_profile,
        )


def test_input_profile_rejects_multidimensional_load_profile():
    """Test that InputProfile rejects multidimensional load_profile arrays."""
    datetime_index = np.array(
        ["2021-01-01 00:00:00", "2021-01-01 00:15:00", "2021-01-01 00:25:00"], dtype="datetime64[s]"
    )
    load_profile = [[2, 4, 5], [2, 4, 5]]

    with pytest.raises(ValueError):
        InputProfile.create(
            datetime_index=datetime_index,
            load_profile=load_profile,
            ambient_temperature_profile=[2, 3, 4],
        )


def test_input_profile_rejects_multidimensional_ambient_temperature():
    """Test that InputProfile rejects multidimensional ambient_temperature_profile."""
    datetime_index = np.array(
        ["2021-01-01 00:00:00", "2021-01-01 00:15:00", "2021-01-01 00:25:00"], dtype="datetime64[s]"
    )
    load_profile = (2, 4, 5)
    ambient_temperature_profile = pd.DataFrame([2, 3, 4], [2, 3, 4])

    with pytest.raises(ValueError, match="array must be one-dimensional"):
        InputProfile.create(
            datetime_index=datetime_index,
            load_profile=load_profile,
            ambient_temperature_profile=ambient_temperature_profile,
        )


def test_input_profile_rejects_multidimensional_datetime_index():
    """Test that InputProfile rejects multidimensional datetime index arrays."""
    datetime_index = [
        np.array(["2021-01-01 00:00:00", "2021-01-01 00:15:00", "2021-01-01 00:25:00"], dtype="datetime64[s]"),
        np.array(["2021-01-01 00:00:00", "2021-01-01 00:15:00", "2021-01-01 00:25:00"], dtype="datetime64[s]"),
    ]
    load_profile = [1, 2, 3]
    ambient_temperature_profile = [1, 2, 3]

    with pytest.raises(ValueError, match="The datetime_index array must be one-dimensional."):
        InputProfile.create(
            datetime_index=datetime_index,
            load_profile=load_profile,
            ambient_temperature_profile=ambient_temperature_profile,
        )


def test_input_profile_rejects_integer_datetime_without_unit():
    """Test that InputProfile rejects integer datetime values without unit specification."""
    datetime_index = [1, 2, 3]  # unixtimes without unit
    load_profile = [1, 2, 3]
    ambient_temperature_profile = [1, 2, 3]

    with pytest.raises(ValueError, match="Converting an integer to a NumPy datetime requires a specified unit"):
        InputProfile.create(
            datetime_index=datetime_index,
            load_profile=load_profile,
            ambient_temperature_profile=ambient_temperature_profile,
        )


def test_that_the_length_of_input_data_is_correct():
    """Test that the length of the input data is correct."""
    datetime_index = pd.date_range("2021-01-01 00:00:00", periods=3)
    load_profile = [1, 2, 3]
    ambient_temperature_profile = [1, 2, 3]
    switchgear_input = InputProfile.create(
        datetime_index=datetime_index,
        load_profile=load_profile,
        ambient_temperature_profile=ambient_temperature_profile,
    )
    assert len(switchgear_input) == 3


def test_input_profile_from_dataframe():
    """Test that the InputProfile can be created from a DataFrame."""
    data = {
        "datetime_index": pd.date_range("2021-01-01 00:00:00", periods=3),
        "load_profile": [1, 2, 3],
        "ambient_temperature_profile": [10, 20, 30],
    }
    df = pd.DataFrame(data)
    input_profile = InputProfile.from_dataframe(df)

    assert len(input_profile) == 3
    assert np.array_equal(input_profile.load_profile, data["load_profile"])
    assert np.array_equal(input_profile.ambient_temperature_profile, data["ambient_temperature_profile"])
    assert np.array_equal(input_profile.datetime_index, data["datetime_index"])


def test_from_dataframe_missing_columns():
    """Test that a ValueError is raised when the DataFrame is missing required columns."""
    # Create a dataframe missing one of the required columns
    df_missing_columns = pd.DataFrame(
        {
            "datetime_index": ["2025-04-17T00:00:00", "2025-04-17T01:00:00"],
            "load_profile": [0.8, 0.9],
            # 'ambient_temperature_profile' is missing
        }
    )

    with pytest.raises(
        ValueError, match="The dataframe is missing the following required columns: ambient_temperature_profile"
    ):
        InputProfile.from_dataframe(df_missing_columns)


def test_load_profile_array_property():
    """Test the load_profile_array property."""
    length = 100
    input_profile = InputProfile(
        datetime_index=pd.date_range("2021-01-01 00:00:00", periods=length).to_numpy(),
        ambient_temperature_profile=np.full((1, length), 20)[0],
        load_profile=np.full((1, length), 50)[0],
    )
    assert np.array_equal(input_profile.load_profile, input_profile.load_profile)


def test_ambient_temperature_is_constant_property(varying_amb_temp_input_profile, basic_input_profile):
    """Test the ambient_temperature_is_constant property."""
    assert basic_input_profile.ambient_temperature_is_constant
    assert not varying_amb_temp_input_profile.ambient_temperature_is_constant

# SPDX-FileCopyrightText: Contributors to the Transformer Thermal Model project
# SPDX-FileCopyrightText: Contributors to the Switchgear Thermal Model project
#
# SPDX-License-Identifier: MPL-2.0
#
# Modified from the Transformer Thermal Model project for use in the Switchgear Model project.
import logging
from collections.abc import Collection
from datetime import datetime
from typing import Self

import numpy as np
import pandas as pd
from pydantic import BaseModel, ConfigDict, model_validator

logger = logging.getLogger(__name__)

_NEGATIVE_LOAD_PROFILE_ERROR_MESSAGE = "The load profile must not contain negative values"


class InputProfile(BaseModel):
    """Class containing the temperature and load profiles for the switchgear thermal model `Model()`.

    This class is also capable of converting the results to a single dataframe with the timestamp as the index for
    convenience.

    This class is a simplified version of the transformer_thermal_model input_profile class (TTM 0.2.1).

    Attributes:
        datetime_index: A 1d array with the datetime index for the profiles.
        load_profile: A 1d array with the load profile for the switchgear.
        ambient_temperature_profile: A 1d array with the ambient temperature profile for the switchgear.

    """

    datetime_index: np.typing.NDArray[np.datetime64]
    load_profile: np.typing.NDArray[np.float64]
    ambient_temperature_profile: np.typing.NDArray[np.float64]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="after")
    def _check_datetime_index_is_sorted(self) -> Self:
        """Check if the datetime index is sorted."""
        if not np.all(self.datetime_index[:-1] <= self.datetime_index[1:]):
            raise ValueError("The datetime index should be sorted.")
        return self

    @model_validator(mode="after")
    def _check_arrays_are_one_dimensional(self) -> Self:
        """Check if the arrays are one-dimensional."""
        if self.datetime_index.ndim != 1:
            raise ValueError("The datetime_index array must be one-dimensional.")
        if self.ambient_temperature_profile.ndim != 1:
            raise ValueError("The ambient_temperature_profile array must be one-dimensional.")
        if self.load_profile.ndim != 1:
            raise ValueError("The load_profile array must be one-dimensional.")
        return self

    @model_validator(mode="after")
    def _check_same_length_of_profiles(self) -> Self:
        """Check if the length of the profiles is the same."""
        if len(self.datetime_index) != len(self.ambient_temperature_profile):
            raise ValueError(
                f"The length of the profiles and index should be the same. Index length: {len(self.datetime_index)}, "
                f"ambient temperature profile length: {len(self.ambient_temperature_profile)}"
            )
        if len(self.datetime_index) != len(self.load_profile):
            raise ValueError(
                f"The length of the profiles and index should be the same. Index length: {len(self.datetime_index)}, "
                f"load profile length: {len(self.load_profile)}"
            )
        return self

    @model_validator(mode="after")
    def _check_load_profile_not_negative(self) -> Self:
        """Check if the load profile contains negative values."""
        if np.min(self.load_profile_array) < 0:
            raise ValueError(_NEGATIVE_LOAD_PROFILE_ERROR_MESSAGE)
        return self

    @classmethod
    def create(
        cls,
        datetime_index: Collection[datetime],
        load_profile: Collection[float],
        ambient_temperature_profile: Collection[float],
    ) -> Self:
        """Create an InputProfile.

        Args:
            datetime_index: The datetime index for the profiles.
            load_profile: The load profile for the switchgear.
            ambient_temperature_profile: The ambient temperature profile for the switchgear.

        Returns:
            An InputProfile object.

        Example: Creating an InputProfile from collections.
            ```python
            >>> from datetime import datetime
            >>> from switchgear_thermal_model.schemas import InputProfile

            >>> datetime_index = [
            ...     datetime(2023, 1, 1, 0, 0),
            ...     datetime(2023, 1, 1, 1, 0),
            ...     datetime(2023, 1, 1, 2, 0),
            ... ]
            >>> load_profile = [0.8, 0.9, 1.0]
            >>> ambient_temperature_profile = [25.0, 24.5, 24.0]
            >>> input_profile = InputProfile.create(
            ...     datetime_index=datetime_index,
            ...     load_profile=load_profile,
            ...     ambient_temperature_profile=ambient_temperature_profile,
            ... )
            >>> input_profile
            InputProfile(datetime_index=array(['2023-01-01T00:00:00.000000',
            '2023-01-01T01:00:00.000000', '2023-01-01T02:00:00.000000'],
            dtype='datetime64[us]'), ambient_temperature_profile=array([25. , 24.5, 24. ]),
            load_profile=array([0.8, 0.9, 1. ]))

            ```

        Example: Directly creating an InputProfile object using numpy arrays.
            ```python
            >>> import numpy as np
            >>> from datetime import datetime
            >>> from switchgear_thermal_model.schemas import InputProfile

            >>> input_profile = InputProfile(
            ...     datetime_index=np.array(
            ...         [
            ...             datetime(2023, 1, 1, 0, 0),
            ...             datetime(2023, 1, 1, 1, 0),
            ...             datetime(2023, 1, 1, 2, 0)
            ...         ],
            ...         dtype=np.datetime64,
            ...     ),
            ...     load_profile=np.array([0.8, 0.9, 1.0], dtype=float),
            ...     ambient_temperature_profile=np.array([25.0, 24.5, 24.0], dtype=float)
            ... )
            >>> input_profile
            InputProfile(datetime_index=array(['2023-01-01T00:00:00.000000',
            '2023-01-01T01:00:00.000000', '2023-01-01T02:00:00.000000'],
            dtype='datetime64[us]'), ambient_temperature_profile=array([25. , 24.5, 24. ]),
            load_profile=array([0.8, 0.9, 1. ]))

            ```
        """
        return cls(
            datetime_index=np.array(datetime_index, dtype=np.datetime64),
            load_profile=np.array(load_profile, dtype=float),
            ambient_temperature_profile=np.array(ambient_temperature_profile, dtype=float),
        )

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> Self:
        """Create an InputProfile from a dataframe."""
        required_columns = {"datetime_index", "load_profile", "ambient_temperature_profile"}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"The dataframe is missing the following required columns: {', '.join(missing_columns)}")

        return cls(
            datetime_index=df["datetime_index"].to_numpy(),
            load_profile=df["load_profile"].to_numpy(),
            ambient_temperature_profile=df["ambient_temperature_profile"].to_numpy(),
        )

    @property
    def load_profile_array(self) -> np.typing.NDArray[np.float64]:
        """Return the single load profile for the switchgear."""
        return self.load_profile

    @property
    def dt(self) -> np.ndarray:
        """The time step between the data points in minutes, with zero for the first element.

        Returns:
            np.ndarray[np.timedelta64]: The time step between the data points in minutes.

        """
        return np.diff(self.datetime_index, prepend=self.datetime_index[0]).astype("timedelta64[m]").astype(float)

    @property
    def ambient_temperature_is_constant(self) -> bool:
        """Check if the ambient temperature profile is constant up to a tolerance of 1e-6."""
        tolerance = 1e-6
        return self.ambient_temperature_profile.max() - self.ambient_temperature_profile.min() <= tolerance

    def __len__(self) -> int:
        """Return the length of the datetime index."""
        return len(self.datetime_index)

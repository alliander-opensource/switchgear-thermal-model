# SPDX-FileCopyrightText: Contributors to the Switchgear Thermal Model project
#
# SPDX-License-Identifier: MPL-2.0

import numpy as np
import pandas as pd

from switchgear_thermal_model.schemas.input_profile import InputProfile
from switchgear_thermal_model.switchgear import Switchgear


def switchgear_temp(data: InputProfile, switchgear: Switchgear) -> pd.Series:
    """Simulate the temperature profile of a circuit breaker component.

    This function simulates the temperature profile of the most critical thermal
    point of a certain circuit breaker for a specific ambient temperature
    profile, load profile and circuit breaker specifications. Since the
    switchgears still follow a minimal thermal model, the solution for any
    component in the switchgears can be modeled similarly. Hence, the thermal
    profile can be modeled for a circuit breaker, or disconnector. It just
    depends on the provided specifications. In particular, the measured
    temperature rise.

    Args:
        data (InputProfile): input profile containing the ambient temperature
            profile and load profile, coupled to a datetime index.
        switchgear (Switchgear): Switchgear object containing the rated current,
            measured temperature rise, temperature rise exponent, and thermal time
            constant.

    Returns:
        np.ndarray
            array of modeled temperatures for the circuit breaker at each timestep
            in the ambient temperature profile
    """
    initial_temperature = data.ambient_temperature_profile[0]
    modeled_temperature = np.zeros(len(data.ambient_temperature_profile))

    modeled_temperature[0] = initial_temperature
    normalised_load = data.load_profile / switchgear.rated_current
    temperature_asymptote = (
        switchgear.measured_temperature_rise * (normalised_load**switchgear.temp_rise_exp)
        + data.ambient_temperature_profile
    )
    exponent = 1 - np.exp(-data.dt / switchgear.thermal_time_constant)

    for i in range(1, len(data.ambient_temperature_profile)):
        new_temperature = (temperature_asymptote[i] - modeled_temperature[i - 1]) * exponent[i] + modeled_temperature[
            i - 1
        ]

        modeled_temperature[i] = new_temperature

    return pd.Series(modeled_temperature, index=data.datetime_index)

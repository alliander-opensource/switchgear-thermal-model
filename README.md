<!--
SPDX-FileCopyrightText: Contributors to the Switchgear Thermal Model project

SPDX-License-Identifier: MPL-2.0
-->

# Switchgear thermal model

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Alliander_switchgear-thermal-model&metric=alert_status&token=530fe96da4abf015e0ecfe4dc2a52aab09ea9029)](https://sonarcloud.io/summary/new_code?id=Alliander_switchgear-thermal-model)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Alliander_switchgear-thermal-model&metric=code_smells&token=530fe96da4abf015e0ecfe4dc2a52aab09ea9029)](https://sonarcloud.io/summary/new_code?id=Alliander_switchgear-thermal-model)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Alliander_switchgear-thermal-model&metric=sqale_rating&token=530fe96da4abf015e0ecfe4dc2a52aab09ea9029)](https://sonarcloud.io/summary/new_code?id=Alliander_switchgear-thermal-model)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Alliander_switchgear-thermal-model&metric=coverage&token=530fe96da4abf015e0ecfe4dc2a52aab09ea9029)](https://sonarcloud.io/summary/new_code?id=Alliander_switchgear-thermal-model)

thermal model which can simulate the temperature of the switchgear, based on
the switchgear specifications, ambient temperature and load profiles.

## Quick start

One can install the switchgear thermal model from PyPI by running

```bash
pip install switchgear-thermal-model
```

### Simple Example

The model uses an `InputProfile`, which is a combination of a datetime index,
load profile, and ambient temperature profile as input for the model.
A quick start can be made using the following code snippet:

```python
import numpy as np

from switchgear_thermal_model.schemas.input_profile import InputProfile
from switchgear_thermal_model.switchgear import Switchgear
from switchgear_thermal_model.thermal_model import switchgear_temp

# Set up the InputProfile
start_time = np.datetime64("2024-01-01T00:00")
dt_minutes = 15
datetime_array = start_time + np.arange(96) * np.timedelta64(dt_minutes, "m")
load_array = np.full((1, 96), 2000)[0]
amb_temp_array = np.full((1, 96), 20)[0]

input_profile = InputProfile(
    datetime_index=datetime_array,
    ambient_temperature_profile=amb_temp_array,
    load_profile=load_array,
)

# Set up a switchgear with specifications
switchgear = Switchgear(
    rated_current=3150,
    measured_temperature_rise=75,
    temp_rise_exp=1.8,
    thermal_time_constant=90
)

# run the model
result = switchgear_temp(input_profile, switchgear)
```

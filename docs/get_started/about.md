<!--
SPDX-FileCopyrightText: Contributors to the Switchgear Thermal Model project

SPDX-License-Identifier: MPL-2.0
-->

# Installation and overview

## Install from PyPI

The Switchgear Thermal Model can be installed directly from PyPI using `pip`:

``` bash
pip install switchgear-thermal-model
```

## Code structure

This package is organized into the following modules:

- `switchgear_thermal_model.thermal_model`: the core of the package, containing
the thermal model used to simulate conductor temperature profiles;
- `switchgear_thermal_model.switchgear`: defines the switchgear class and its
associated thermal and electrical parameters;
- `switchgear_thermal_model.schemas`: contains the data schema, defining the
model input interface.

## Example of switchgear modeling

This example demonstrates how the conductor temperature in switchgear is
calculated.

The required information is:

1. The load: For example the load [A] during a week.
2. The ambient temperature: The temperature during the same period as the load.
3. The switchgear specifications: The required specifications are:
    - the nominal load [A]
    - the measured nominal temperature rise
    - Two thermal parameters: the exponent S and time constant $\tau$

Now we will calculate switchgear
temperatures using `switchgear_thermal_model.thermal_model` and some arbitrary
ambient temperature and loads.

```Python
import pandas as pd

from switchgear_thermal_model.schemas.input_profile import InputProfile
from switchgear_thermal_model.switchgear import Switchgear
from switchgear_thermal_model.thermal_model import switchgear_temp

# In this example the model is used to calculate the switchgear temperature
# based on a load and ambient profile with a period of one week. Any duration
# can be chosen preferably with timestamps with an interval of 15 minute or
# lower. Larger timesteps will result in incorrect results but it *is* possible
# to calculate with them.
one_week = 4*24*7
datetime_index = pd.date_range("2020-01-01", periods=one_week, freq="15min")

# For the load (in A) and ambient temperature (in degrees C) arbitrary constants
# profiles are chosen. It is also possible to use a realistic profile.
nominal_load = 100
load_points = pd.Series([nominal_load] * one_week, index=datetime_index)
ambient_temp = 21
temperature_points = pd.Series([ambient_temp] * one_week, index=datetime_index)

# Create an input object with the profiles
profile_input = InputProfile.create(
   datetime_index = datetime_index,
   load_profile = load_points,
   ambient_temperature_profile = temperature_points
)

# Initialize a switchgear object
basic_switchgear = Switchgear(
    rated_current=100, 
    measured_temperature_rise=75,
    temp_rise_exp=1.8,
    thermal_time_constant=90
)

# Simulate the conductor temperature
result = switchgear_temp(profile_input, basic_switchgear)
```

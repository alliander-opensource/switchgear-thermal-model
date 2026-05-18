<!--
SPDX-FileCopyrightText: Contributors to the Switchgear Thermal Model project

SPDX-License-Identifier: MPL-2.0
-->

# Model input

The Switchgear Thermal model requires the following three inputs:

1. Thermal specifications of the switchgear
2. Electrical Load profile
3. Ambient temperature profile

Together, these inputs allow the model to simulate the time-dependent conductor
temperature of the switchgear under realistic operating conditions.

## Relevant thermal specifications

To define a switchgear object, four thermal parameters must be specified. These
parameters describe both the steady-state and dynamic thermal behaviour of the
switchgear.

### 1. Nominal load

The nominal load is the maximum allowable continuous current through the
switchgear as specified by the Original Equipment Manufacturer (OEM). This value
is defined under reference conditions, typically a constant load and an ambient
temperature of 40 $^{\circ}$ C.

The nominal load can usually be obtained from the switchgear type plate, the
Factory Acceptance Test (FAT) report, or the single-line diagram of the
substation. It must be specified in ampere and is a required input parameter; no
default or fallback value is available.

### 2. Measured temperature rise

During a temperature rise test, the OEM measures the maximum increase in
conductor temperature above ambient temperature under nominal load conditions.
This temperature rise, expressed in kelvin, represents the steady-state
conductor temperature increase at 100 % load.

The value is typically reported in the FAT documentation or obtained from
laboratory measurements. If the measured temperature rise is not available, a
conservative fallback value can be used, equal to the temperature limit minus 40
$^{\circ}$C. This reflects the requirement that the conductor temperature must
remain below its temperature limit during the temperature rise test in order to
pass the FAT.

### 3. Thermal exponent

The thermal exponent is a dimensionless parameter that describes the
relationship between the load level and the resulting temperature rise of the
switchgear. It governs how conductor temperature scales under overloading or
underloading conditions.

Switchgear-specific values for this exponent are often not provided by the OEM
and can only be determined through laboratory testing at multiple load factors.
In the absence of asset-specific data, IEC 62271‑306 recommends using a value
typically in the range of 1.6 to 2.0.

### 4. Thermal time constant

The thermal time constant $ \tau $, expressed in minutes, characterizes the
dynamic thermal response of the switchgear. It determines the exponential rate
at which the conductor temperature approaches its steady-state value under
constant conditions.

After five times the thermal time constant, the conductor temperature has
reached about 99.3 % of its final temperature rise. A switchgear-specific time
constant can be derived from a detailed heating curve obtained during a
temperature rise test. If such data is unavailable, it must be determined
through laboratory experiments.

The thermal time constant is strongly influenced by the insulating and cooling
medium used in the switchgear and an important parameter for the conductor
temperature simulation under dynamic conditions.

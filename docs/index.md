<!--
SPDX-FileCopyrightText: Contributors to the Switchgear Thermal Model project

SPDX-License-Identifier: MPL-2.0
-->

# Welcome to Switchgear Thermal Model

Switchgear Thermal Model is a library for modeling the conductor temperature
of switchgear based on thermal specifications, load profiles and an ambient
temperature conditions. The model is based on calculation principles described
in IEC 62271-306. The results of the model should be considered indicative:
further validation and refinement of the model are required. Contributions to
improve, validate, and extend the model are welcome.

## Features

The Switchgear Thermal Model is designed to simulate temperature behavior in
switchgear. In summary, it provides the following features:

* Creation of a switchgear model based on specified thermal parameters;
* Simulation of conductor temperature using static or dynamic load profiles and
ambient temperature profiles;

## Who is using the Switchgear Thermal Model?

The Switchgear Thermal Model is intended for engineers, analysts, and
researchers who want to better understand and quantify the development of
conductor temperatures in switchgear under varying operating conditions.

Since conductor temperature ultimately determines the maximum allowable current
and power that can be transported through switchgear, the model enables a
temperature-driven approach to loadability assessment. Instead of relying on
static current limits, the model can be used to determine asset- and
profile-specific ampacities based on thermal limits, ambient conditions, and
actual load profiles.

This makes the model particularly suitable for applications such as dynamic
loadability analysis, asset utilization studies, and scenario analyses in power
system planning and operation.

## Model validation

The Switchgear Thermal Model (SGTM) is based on IEC 62271-1 and
IEC 62271-306, which define the thermal behaviour of high-voltage
switchgears.

Validation of the model has primarily been performed using laboratory
measurements under controlled conditions. At this stage, no field
validation has been conducted.

The results of the laboratory tests show good agreement with measurements,
with small deviations (typically within a few Kelvin), which are acceptable
for the intended application.

It should be noted that most validation has been carried out using static
load profiles. Model performance under cyclic or highly dynamic conditions
has not yet been fully validated and requires further investigation.

The model has mainly been developed and tested for medium-voltage
applications (10 kV and 20 kV). However, the underlying methodology is in
principle applicable to switchgear systems with rated voltages ≥ 1 kV,
provided that IEC 62271-306 is applied appropriately.

Given the current validation status, the model should be used with
appropriate engineering judgement, especially when applied outside the
validated domain.

## License

This project is licensed under the Mozilla Public License, version 2.0 - see
[LICENSE](https://github.com/alliander/swtichgear-thermal-model/blob/main/LICENSE) for details.

## Licenses third-party libraries

This project includes third-party libraries,
which are licensed under their own respective Open-Source licenses.
SPDX-License-Identifier headers are used to show which license is applicable.

The concerning license files can be found in the
[LICENSES](https://github.com/alliander/switchgear-thermal-model/blob/main/LICENSES) directory.

## Contributing

Please read
[CODE_OF_CONDUCT](https://github.com/alliander/switchgear-thermal-model/blob/main/CODE_OF_CONDUCT.md),
[CONTRIBUTING](https://github.com/alliander/switchgear-thermal-model/blob/main/CONTRIBUTING.md)
and
[PROJECT GOVERNANCE](https://github.com/alliander/switchgear-thermal-model/blob/main/GOVERNANCE.md)
for details on the process for submitting pull requests to us.

## Contact

Please read [SUPPORT](https://github.com/alliander/switchgear-thermal-model/blob/main/SUPPORT.md) for how to
connect and get into contact with the Switchgear Thermal Model project.

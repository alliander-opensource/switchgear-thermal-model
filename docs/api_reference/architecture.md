<!--
SPDX-FileCopyrightText: Contributors to the Switchgear Thermal Model project

SPDX-License-Identifier: MPL-2.0
-->

# The architecture of Switchgear Thermal Model

<!-- markdownlint-disable MD013 -->
## System context diagram

```mermaid
C4Context
    title C1: System Context of the Switchgear Thermal Model

    Person(engineer, "Engineer", "Someone that analyses or reports on the thermal behaviour of switchgear components.")

    Boundary(b0, "Switchgear Thermal Model") {
        System(stm, "Switchgear Thermal Model", "Simulates the temperature profile of a switchgear component<br/> given a load profile, ambient temperature profile and asset specifications.")
    }

    System_Ext(upstream, "Upstream data source", "Provides load profiles and ambient temperature measurements.")

    Rel(engineer, stm, "Models switchgear temperatures using")
    Rel(upstream, stm, "Supplies load and ambient temperature profiles to")

    UpdateLayoutConfig($c4BoundaryInRow="1", $c4ShapeInRow="2")
```

## Container diagram

```mermaid
C4Container
    title C2: Containers of the Switchgear Thermal Model

    Person(engineer, "Engineer", "Someone that analyses or reports on the thermal behaviour of switchgear components.")

    Boundary(b0, "Switchgear Thermal Model") {

        Boundary(b1, "Core") {
            Container(thermal_model, "Thermal Model", "Python module", "Computes the temperature profile of a switchgear component over time.")
            Container(switchgear, "Switchgear", "Python module", "Pydantic data class holding the asset specifications of a switchgear component.")
            Container(input_profile, "Input Profile", "Python module", "Pydantic schema that validates and structures the load and ambient temperature profiles.")
        }

        Boundary(b2, "Docs") {
            Container(docs, "Docs", "HTML module", "Markdown files and notebooks providing usage guidance and API reference documentation.")
        }

        Boundary(b3, "Imported packages") {
            Container_Ext(numpy, "NumPy", "Python package", "Numerical array operations used throughout the thermal calculations.")
            Container_Ext(pydantic, "Pydantic", "Python package", "Schema validation for asset specifications and input profiles.")
            Container_Ext(pandas, "Pandas", "Python package", "Used in input conversion within the InputProfile schema.")
        }
    }

    Rel(engineer, thermal_model, "Calculates switchgear temperature profiles using")
    Rel(engineer, docs, "Understands the model and its inputs via")

    Rel(thermal_model, switchgear, "Reads asset specifications from")
    Rel(thermal_model, input_profile, "Reads validated load and ambient profiles from")
    Rel(thermal_model, numpy, "Performs numerical calculations with")
    Rel(switchgear, pydantic, "Validates asset specifications with")
    Rel(input_profile, pydantic, "Validates input arrays with")
    Rel(input_profile, pandas, "Converts DataFrame input to NumPy arrays with")

    UpdateLayoutConfig($c4BoundaryInRow="2", $c4ShapeInRow="3")
```

## Component diagrams

### Thermal model

```mermaid
C4Component
    title C3: Thermal Model Components

    Person(engineer, "Engineer", "Someone that analyses or reports on the thermal behaviour of switchgear components.")

    Boundary(b0, "Switchgear Thermal Model") {
        System_Boundary(s0, "Thermal Model") {
            Component(switchgear_temp, "switchgear_temp()", "Python function", "Simulates the temperature profile of a switchgear component using<br/> a first-order thermal model. Entry point for thermal calculations.")
            Component(get_time_step, "_get_time_step()", "Python function", "Derives time deltas in minutes from the datetime index of an InputProfile.")
        }

        System_Boundary(s1, "Schemas") {
            Component(switchgear_cls, "Switchgear", "Pydantic model", "Holds asset specifications.")
            Component(input_profile_cls, "InputProfile", "Pydantic model", "Validated load and ambient temperature profiles.")
        }

        Component_Ext(numpy, "NumPy", "Python package", "Numerical array operations.")
    }

    Rel(engineer, switchgear_temp, "Calculates temperature profiles by calling")
    Rel(switchgear_temp, get_time_step, "Derives time deltas via")
    Rel(switchgear_temp, switchgear_cls, "Reads rated current and thermal parameters from")
    Rel(switchgear_temp, input_profile_cls, "Reads load and ambient temperature profiles from")
    Rel(switchgear_temp, numpy, "Performs array-based calculations with")

    UpdateLayoutConfig($c4BoundaryInRow="2", $c4ShapeInRow="2")
```

### Switchgear schema

```mermaid
C4Component
    title C3: Switchgear Schema Components

    Person(engineer, "Engineer", "Someone that analyses or reports on the thermal behaviour of switchgear components.")

    Boundary(b0, "Switchgear Thermal Model") {
        System_Boundary(s0, "Schemas") {
            Component(switchgear_cls, "Switchgear", "Pydantic model", "Holds asset specifications: rated current, measured temperature rise,<br/> temperature rise exponent and thermal time constant.")
        }

        Component_Ext(pydantic, "Pydantic", "Python package", "Schema validation for asset specifications.")
    }

    Rel(engineer, switchgear_cls, "Defines asset specifications with")
    Rel(switchgear_cls, pydantic, "Validates field values with")

    UpdateLayoutConfig($c4BoundaryInRow="1", $c4ShapeInRow="2")
```

### InputProfile schema

```mermaid
C4Component
    title C3: InputProfile Schema Components

    Person(engineer, "Engineer", "Someone that analyses or reports on the thermal behaviour of switchgear components.")

    Boundary(b0, "Switchgear Thermal Model") {
        System_Boundary(s0, "Schemas") {
            Component(input_profile_cls, "InputProfile", "Pydantic model", "Validates and stores the datetime index, load profile and ambient<br/> temperature profile. Enforces array shape and ordering constraints.")
        }

        Component_Ext(pydantic, "Pydantic", "Python package", "Schema validation and model validators.")
        Component_Ext(pandas, "Pandas", "Python package", "Used in input conversion to NumPy arrays.")
        Component_Ext(numpy, "NumPy", "Python package", "Array types used for the stored profiles.")
    }

    Rel(engineer, input_profile_cls, "Constructs validated input profiles with")
    Rel(input_profile_cls, pydantic, "Validates array inputs and ordering with")
    Rel(input_profile_cls, pandas, "Converts DataFrame input to NumPy arrays with")
    Rel(input_profile_cls, numpy, "Stores profiles as typed NumPy arrays with")

    UpdateLayoutConfig($c4BoundaryInRow="1", $c4ShapeInRow="3")
```

<!-- markdownlint-enable MD013 -->
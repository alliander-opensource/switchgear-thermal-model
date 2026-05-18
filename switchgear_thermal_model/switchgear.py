# SPDX-FileCopyrightText: Contributors to the Switchgear Thermal Model project
#
# SPDX-License-Identifier: MPL-2.0

from pydantic import BaseModel, Field


class Switchgear(BaseModel):
    """A switchgear to model the thermal behavior of a switchgear component."""

    rated_current: float = Field(..., description="Rated current of the switchgear in Amperes (A).")
    measured_temperature_rise: float = Field(
        ...,
        description=(
            "Measured temperature rise of the switchgear in Kelvin (K). "
            "How many degrees the switchgear temperature rises above the ambient temperature "
            "when operating its rated current."
        ),
    )
    temp_rise_exp: float = Field(
        ...,
        description=(
            "Temperature rise exponent for the switchgear. Determines how the temperature rise scales with the load. "
            "A value of 1.0 indicates a linear relationship, while values greater than 1.0 indicate a nonlinear "
            "relationship (e.g., quadratic or cubic)."
        ),
    )
    thermal_time_constant: float = Field(
        ...,
        description=(
            "Thermal time constant of the switchgear in minutes (m). "
            "This determines how quickly the switchgear temperature responds to changes in load."
        ),
    )

    def __init__(
        self, rated_current: float, measured_temperature_rise: float, temp_rise_exp: float, thermal_time_constant: float
    ) -> None:
        """Initialize the switchgear with its thermal parameters."""
        super().__init__(
            rated_current=rated_current,
            measured_temperature_rise=measured_temperature_rise,
            temp_rise_exp=temp_rise_exp,
            thermal_time_constant=thermal_time_constant,
        )

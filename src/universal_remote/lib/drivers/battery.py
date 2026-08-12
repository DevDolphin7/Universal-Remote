from universal_remote.lib.drivers.hardware import Hardware


class Battery:
    def __init__(self) -> None:
        """Initializes the Battery with default voltage values and hardware settings."""
        self.full_voltage = 4.2
        self.empty_voltage = 3.0
        self.voltage = 0.0
        self.voltage_threshold = round(
            self.empty_voltage + ((self.full_voltage - self.empty_voltage) / 10), 2
        )

        self._vsys = Hardware.vsys
        self._adc_volt_conversion_factor = 3.3 * 2 / 65535
        self._sample_size = 16

    def read_voltage(self) -> float:
        """Reads the voltage from the battery using the ADC and returns the calculated voltage."""
        raw = self._vsys.read_u16()

        return raw * self._adc_volt_conversion_factor

    def get_voltage(self) -> float:
        """Reads the battery voltage multiple times and returns the average voltage rounded to 2 decimal places."""
        total = 0.0
        self.read_voltage()  # Discard the first reading to allow the ADC to stabilize

        for _ in range(self._sample_size):
            total += self.read_voltage()

        return round(total / self._sample_size, 2)

    def is_low(self) -> bool:
        """Checks if the battery percentage is below a specified threshold."""
        return self.voltage < self.voltage_threshold

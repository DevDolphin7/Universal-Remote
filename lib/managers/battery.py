from machine import ADC
from lib.core.config import VOLTAGE_DIVIDER_PIN


class BatteryManager:
    def __init__(self):
        self._vsys = ADC(VOLTAGE_DIVIDER_PIN)
        self._adc_volt_conversion_factor = 3.3 * 2 / 65535
        self._sample_size = 16

    def read_voltage(self):
        """Reads the voltage from the battery using the ADC and returns the calculated voltage."""
        raw = self._vsys.read_u16()

        return raw * self._adc_volt_conversion_factor

    def get_voltage(self):
        """Reads the battery voltage multiple times and returns the average voltage."""
        total = 0.0
        self.read_voltage()  # Discard the first reading to allow the ADC to stabilize

        for _ in range(self._sample_size):
            total += self.read_voltage()

        return total / self._sample_size

from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.drivers.hardware import Hardware
from universal_remote.lib.core.types import Events


class Power:
    def __init__(self, event_bus: EventBus) -> None:
        self.event_bus = event_bus

        self.state_four = 2.8  # Volts
        self.state_three = 2.55  # Volts
        self.state_two = 2.35  # Volts
        self.state_one = 2.25  # Volts
        self.hysteresis = 0.05  # Volts

        self._vsys = Hardware.vsys
        self._adc_volt_conversion_factor = 3.3 * 2 / 65535
        self._sample_size = 8

        self.set_state()

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

    def set_state(self):
        voltage = self.get_voltage()

        if voltage > self.state_four:
            self.state = 4
        elif voltage > self.state_three:
            self.state = 3
        elif voltage > self.state_two:
            self.state = 2
        elif voltage > self.state_one:
            self.state = 1
        else:
            self.state = 0

    def update_state(self) -> None:
        """Returns an integer indicating the low 1-4 high battery status based on the current voltage."""
        voltage = self.get_voltage()

        if self.state == 4:
            if voltage < self.state_four - self.hysteresis:
                self.state = 3
        elif self.state == 3:
            if voltage < self.state_three - self.hysteresis:
                self.state = 2
        elif self.state == 2:
            if voltage < self.state_two - self.hysteresis:
                self.state = 1
        elif self.state == 1:
            if voltage < self.state_one - self.hysteresis:
                self.state = 0

    def is_low(self) -> bool:
        """Checks if the battery percentage is below a specified threshold."""
        return self.state == 0

    def update(self) -> None:
        old_state = self.state
        if self.state == 0:
            self.set_state()
        else:
            self.update_state()

        if old_state != self.state:
            self.event_bus.publish(Events.BATTERY_LEVEL_CHANGED, self.state)

            if self.is_low():
                self.event_bus.publish(Events.LOW_BATTERY)

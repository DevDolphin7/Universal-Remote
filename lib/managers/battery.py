from time import ticks_ms, ticks_diff
from lib.managers.hardware import Hardware
from lib.core.event_bus import event_bus
from lib.core.types import Events, PowerState


class BatteryManager:
    def __init__(self) -> None:
        """Initializes the BatteryManager with default voltage values and hardware settings."""
        self.full_voltage = 4.2
        self.empty_voltage = 3.0
        self.voltage = 0.0
        self.percentage = 0
        self.status = 0
        self.current_state = PowerState.ACTIVE

        self._vsys = Hardware.vsys
        self._adc_volt_conversion_factor = 3.3 * 2 / 65535
        self._sample_size = 16
        self._last_activity = ticks_ms()
        self._deep_sleep_interval = 120000  # ms
        self._idle_interval = 60000  # ms

        self._event_bus = event_bus
        self._event_bus.subscribe(Events.BUTTON_RELEASED, self._on_activity)

        self.update()

    def _on_activity(self, *args, **kwargs) -> None:
        """Handles activity events to update the battery status."""
        self._last_activity = ticks_ms()
        if self.current_state != PowerState.ACTIVE:
            print("Woken up")
            self.current_state = PowerState.ACTIVE
            self._event_bus.publish(Events.WAKE)

    def update(self) -> None:
        """Updates the battery status by reading the current voltage and calculating the percentage."""
        self.voltage = self.get_voltage()
        self.percentage = self.get_percentage()
        self.status = self.get_status()

        if self.is_low():
            self._event_bus.publish(Events.LOW_BATTERY, self.percentage)

        self.poll()

    def poll(self):
        elapsed = ticks_diff(ticks_ms(), self._last_activity)

        if (
            elapsed > self._deep_sleep_interval
            and self.current_state != PowerState.DEEP_SLEEP
        ):
            self._enter_deep_sleep()

        elif elapsed > self._idle_interval and self.current_state == PowerState.ACTIVE:
            self._enter_idle()

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

    def get_percentage(self) -> int:
        """Calculates the battery percentage based on the current voltage."""
        if self.voltage >= self.full_voltage:
            return 100
        elif self.voltage <= self.empty_voltage:
            return 0
        else:
            percentage = (self.voltage - self.empty_voltage) / (
                self.full_voltage - self.empty_voltage
            )
            return round(percentage * 100)

    def get_status(self) -> int:
        """Returns an integer indicating the battery status based on the current voltage.
        4: Battery is full (>= 75%)
        3: Battery is medium (>= 50% and < 75%)
        2: Battery is low (>= 25% and < 50%)
        1: Battery is very low (< 25%)"""
        percentage = self.get_percentage()

        if percentage >= 75:
            return 4
        elif percentage >= 50:
            return 3
        elif percentage >= 25:
            return 2
        else:
            return 1

    def is_low(self, threshold=10) -> bool:
        """Checks if the battery percentage is below a specified threshold."""
        return self.percentage < threshold

    def _enter_deep_sleep(self):
        print("Entering deep")
        self.current_state = PowerState.DEEP_SLEEP
        self._event_bus.publish(Events.SLEEP_DEEP, PowerState.DEEP_SLEEP)

    def _enter_idle(self):
        print("Entering idle")
        self.current_state = PowerState.IDLE
        self._event_bus.publish(Events.SLEEP_IDLE, PowerState.IDLE)


battery = BatteryManager()

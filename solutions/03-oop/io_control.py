from machine import Pin
from machine import PWM
import time


class Led:
    """
    This class represents a LED with basic functionality. It uses
    the Pin object from the machine module.
    """

    def __init__(self, pin_number):
        """
        Constructor to initialize the LED with the given pin number.
        """
        # Instance variable `self.pin`, unique to each instance
        self.pin = Pin(pin_number, Pin.OUT)

    def on(self):
        """Turn the LED on."""
        self.pin.on()

    def off(self):
        """Turn the LED off."""
        self.pin.off()

    def toggle(self):
        """Toggle the LED state."""
        self.pin.value(not self.pin.value)

    def blink(self, duration=0.5, times=5):
        """Make the LED blink a certain number of times."""
        for _ in range(times):
            self.pin.on()
            time.sleep(duration)
            self.pin.off()
            time.sleep(duration)


class PwmLed(Led):
    """
    This class inherits from the base LED class and extends
    it with Pulse Width Modulation (PWM) functionality.
    """

    def __init__(self, pin_number, frequency=1000):
        # Call the parent class (Led) constructor
        super().__init__(pin_number)
        # Initialize PWM on the LED pin
        self.pwm = PWM(self.pin, freq=frequency)
    
    def set_brightness(self, brightness):
        """Set the LED brightness using PWM (0 to 100%)."""
        duty_cycle = int(brightness / 100 * 1023)  # Duty cycle 0 to 1023
        self.pwm.duty(duty_cycle)

    def on(self, brightness=100):
        """Override the `on` method with a brightness (0 to 100%)."""
        self.set_brightness(brightness)

    def off(self):
        """Override the off method to use 0% duty cycle."""
        self.set_brightness(0)

    def fade_in(self, steps=100, duration=1):
        """Fade in the LED by increasing brightness gradually."""
        step_duration = duration / steps
        for i in range(steps):
            self.set_brightness(i)
            time.sleep(step_duration)

    def fade_out(self, steps=100, duration=1):
        """Fade out the LED by decreasing brightness gradually."""
        step_duration = duration / steps
        for i in range(steps, 0, -1):
            self.set_brightness(i)
            time.sleep(step_duration)


class Button:
    def __init__(self, pin_number):
        self.button = Pin(pin_number, Pin.IN, Pin.PULL_UP)

    def is_pressed(self):
        return not self.button.value()  # Active-low button


# Code inside `if __name__ == "__main__"` will not be executed
# when imported as a module but runs only when executed directly.
if __name__ == "__main__" :
    led = Led(2)
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
    led.blink(times=3)

    # Create a PWM LED object and control brightness
    led = PwmLed(2)
    led.set_brightness(10)  # Set brightness to 20%
    time.sleep(1)
    led.on(50)
    time.sleep(1)
    led.fade_in()
    led.fade_out()
    time.sleep(1)
    led.off()

    btn = Button(27)
    # Turn on LED when button is pressed
    if btn.is_pressed():
        led.on()
    else:
        led.off()

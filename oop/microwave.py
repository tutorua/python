# OOP in Python
# https://www.youtube.com/watch?v=rLyYb7BFgQI

class Microwave:
    def __init__(self, brand: str, model: str, power: str) -> None:
        self.brand = brand
        self.model = model
        self.power = power
        self.turned_on: bool = False

    def __str__(self):
        return f'{self.brand} {self.model} {self.power}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.brand}, {self.model}, {self.power})'
    
    def turn_on(self) -> None:
        """Turn on the microwave."""
        # Check if the microwave is already on
        if self.turn_on:
            print(f'{self.brand} {self.model} is already ON.')
        else:
            self.turn_on = True
            # Simulate turning on the microwave
            # In a real scenario, you would add code to actually turn on the microwave here.
            # For example, you might send a signal to the microwave's control board.
            # This is just a placeholder for demonstration purposes.
            # self.control_board.send_signal('turn_on')
            print(f'{self.brand} {self.model} is now ON.')

    def turn_off(self) -> None:
        """Turn off the microwave."""
        # Check if the microwave is already off
        if not self.turn_on:
            print(f'{self.brand} {self.model} is already OFF.')
        else:
            self.turn_on = False
            # Simulate turning off the microwave
            # In a real scenario, you would add code to actually turn off the microwave here.
            # For example, you might send a signal to the microwave's control board.
            # This is just a placeholder for demonstration purposes.
            # self.control_board.send_signal('turn_off')
            print(f'{self.brand} {self.model} is now OFF.')
    
    def run(self, time: int) -> None:
        """Run the microwave for a specified time."""
        # Check if the microwave is on before running it
        if not self.turn_on:
            print(f'{self.brand} {self.model} is OFF. Please turn it ON first.')
        else:
            # Simulate running the microwave for the specified time
            # In a real scenario, you would add code to actually run the microwave here.
            # For example, you might send a signal to the microwave's control board.
            # This is just a placeholder for demonstration purposes.
            # self.control_board.send_signal('run', time)
            print(f'{self.brand} {self.model} is running for {time} seconds.')


smeg: Microwave = Microwave('Smeg', 'SMEG1', 800)
print(smeg.__str__())
print(smeg.power)
smeg.turn_on()
smeg.turn_on()  # Attempt to turn on again
smeg.run(30)
smeg.turn_off()

bosh: Microwave = Microwave('Bosh', 'BOSCH1', 900)
print(bosh.__str__())
print(bosh.power)
# train_system/track_controller/track_controller.py
from hw_plc import HWPLC

class HWTrackController:
    def __init__(self, track_occupancies, authority):
        """
        Initialize the TrackController with an HWPLC instance
        """
        self.plc = HWPLC(track_occupancies, authority)
        
        # Initialize the PLC to determine the initial states
        self.plc.plc()

    def get_switch_position(self):
        """
        Get the switch position from the PLC
        """
        switch_position = self.plc.switch_positions()
        print("Switch Position:", "Station C" if switch_position else "Station B")
        return switch_position

    def get_crossing_signal(self):
        """
        Get the crossing signal state from the PLC
        """
        crossing_signal = self.plc.crossing_signals()
        print("Crossing Signal:", "Down" if crossing_signal else "Up")
        return crossing_signal

    def get_light_station_b(self):
        """
        Get the light signal state for Station B from the PLC
        """
        self.plc.light_signals()
        light_station_b = "RED" if not self.plc.light_colorB else "GREEN"
        print("Light Station B:", light_station_b)
        return light_station_b

    def get_light_station_c(self):
        """
        Get the light signal state for Station C from the PLC
        """
        self.plc.light_signals()
        light_station_c = "RED" if not self.plc.light_colorC else "GREEN"
        print("Light Station C:", light_station_c)
        return light_station_c
    
# Example usage
"""
if __name__ == "__main__":
    track_occupancies = [False] * 16
    authority = 45

    # Simulate some track occupancies
    track_occupancies[6] = True  # Block 6 is occupied

    controller = HWTrackController(track_occupancies, authority)

    controller.get_switch_position()
    controller.get_crossing_signal()
    controller.get_light_station_b()
    controller.get_light_station_c()
"""
# train_system/track_controller/track_controller.py
from hw_plc import HWPLC

class HWTrackController:
    def __init__(self, track_occupancies, authority):
        self.plc = HWPLC(track_occupancies, authority)
        # Initialize the PLC to determine the initial states
        self.plc.plc()

    def get_switch_position(self):
        switch_position = self.plc.switch_positions()
        print("Switch Position:", "Station C" if switch_position else "Station B")
        return switch_position

    def get_crossing_signal(self):
        crossing_signal = self.plc.crossing_signals()
        print("Crossing Signal:", "Down" if crossing_signal else "Up")
        return crossing_signal

    def get_light_station_b(self):
        self.plc.light_signals()
        light_station_b = "GREEN" if not self.plc.light_colorB else "RED"
        print("Light Station B:", light_station_b)
        return light_station_b

    def get_light_station_c(self):
        self.plc.light_signals()
        light_station_c = "GREEN" if not self.plc.light_colorC else "RED"
        print("Light Station C:", light_station_c)
        return light_station_c
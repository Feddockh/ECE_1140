class HardwareTrackController:
 def __init__(self, new_track_occupancies):
        """
        Initialize the hardware track controllers
        """
        self.track_occupancies = new_track_occupancies
        self.switch = False
        self.light_StationB = False
        self.light_StationC = False
        self.crossing_signal = False
        self.hw_plc()

 
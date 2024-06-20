# train_system/track_controller/hw_plc.py
class HWPLC:
 #INITIALIZE
    def __init__(self, track_occupancies, authority):
        """
        Initialize all variables
        """
        self.authority = authority
        self.track_occupancies = track_occupancies
        self.switch_position = False
        self.light_colorB = False #0 = green, 1 = red
        self.light_colorC = False
        self.crossing_signal = False
        self.plc()
 #PLC
    def plc(self):
        """
        This is a PLC program intended to determine the switch states, Light signals, and crossign signals.
        There are 5 scenarios that this PLC simulates
    Returns:
        switch_position(bool): Bool representing the track switch positions0 = connected to block 6, train will head towards Station B 1 = connected to block 11, train will head towards Station C
        crossing_signal(bool): Bool representing the Crossing State 0 = gate is up, pedestrians can cross1 = gate is down, pedestrians must stop
        light_StationB(bool): Bool representing light signal for the track headed towards StationB 0 = GREEN, 1 = RED
        light_StationC(bool): Bool representing light signal for the track headed towards StationC 0 = GREEN, 1 = RED
    """
        
        self.crossing_signals()
        self.switch_positions()
        self.light_signals()

    def switch_positions(self):
        #Determining switch position
        #Check if both tracks are occupied (ERROR CHECK)
        if((self.track_occupancies[11] or self.track_occupancies[12] or self.track_occupancies[13] 
            or self.track_occupancies[14] or self.track_occupancies[15])and (self.track_occupancies[6] or self.track_occupancies[7] or self.track_occupancies[8] 
            or self.track_occupancies[9] or self.track_occupancies[10])):
            self.emergency_authority(0)
            #print("EMERGENCY WARNING!")
            #print("BOTH TRACKS ARE OCCUPIED")
            #print("ALL TRAINS MUST STOP")

        #Check if path to station B is occupied
        elif (self.track_occupancies[6] or self.track_occupancies[7] or self.track_occupancies[8] 
            or self.track_occupancies[9] or self.track_occupancies[10]):
            self.switch_position = True
            #print("Switch is connected to Block 6.")
            #print("Train is headed towards Station B.")

        #check if path to station C is occupied
        elif(self.track_occupancies[11] or self.track_occupancies[12] or self.track_occupancies[13] 
            or self.track_occupancies[14] or self.track_occupancies[15]):
            self.switch_position = False
            #print("Switch is connected to Block 11.")
            #print("Train is headed towards Station C.")

        return self.switch_position

    def crossing_signals(self):
        #Determing crossing signal / gate
        if (self.track_occupancies[2] or self.track_occupancies[3] or self.track_occupancies[4]):
            self.crossing_signal = True
            #print("Crossing Signal is down. Do Not Cross!")
        else:
            self.crossing_signal = False
           #print("Crossing Signal is up. Pedestrians can now cross the tracks.")
        
        return  self.crossing_signal 

    def emergency_authority(self, authority):
        #emergency authority for if both tracks are zero
        self.authority = authority
        return self.authority

    def light_signals(self):
        if((self.track_occupancies[11] or self.track_occupancies[12] or self.track_occupancies[13] 
            or self.track_occupancies[14] or self.track_occupancies[15])and (self.track_occupancies[6] or self.track_occupancies[7] or self.track_occupancies[8] 
            or self.track_occupancies[9] or self.track_occupancies[10])):
            self.light_colorB = True
            self.light_colorC = True
    
    #Check if path to station B is occupied
        elif (self.track_occupancies[6] or self.track_occupancies[7] or self.track_occupancies[8] 
            or self.track_occupancies[9] or self.track_occupancies[10]):
            self.light_colorB = True
            self.light_colorC = False
            #print("Station C Light is RED")
            #print("Station B light is GREEN")

    #check if path to station C is occupied
        elif(self.track_occupancies[11] or self.track_occupancies[12] or self.track_occupancies[13] 
            or self.track_occupancies[14] or self.track_occupancies[15]):
            self.light_colorB = False
            self.light_colorC = True
           #print("Station C Light is GREEN.")
            #print("Station B light is RED.")

        return self.light_colorB, self.light_colorC

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
        self.light_StationB = False
        self.light_StationC = False
        self.crossing_signal = False
        self.plc()

 #PLC
 def plc(self):
    """
    This is a PLC program intended to determine the switch states, Light signals, and crossign signals.
    There are 5 scenarios that this PLC simulates
            1) Blocks 6-10 are occupied, so the switch must switch to blocks 11-15 and force the train to station C
                light to station C turns green, light to station B turns red. 

            2) Blocks 11 - 15 are occupied, so the switch must switch to blocks 6-10 and force the train to station B. 
                light to station B turns green, light to station C turns red

            3) Both blocks 6-10 and 11-15 are occupied, so light signals must turn
            4) Blocks 2-4 are occupied, crossing gates come down
            5) Blocks 2-4 are unoccupied, crossing gates go up, and pedestrians can cross
    
    Returns:
        switch_position(bool): Bool representing the track switch positions
                        0 = connected to block 6, train will head towards Station B
                        1 = connected to block 11, train will head towards Station C
        crossing_signal(bool): Bool representing the Crossing State 
                        0 = gate is up, pedestrians can cross
                        1 = gate is down, pedestrians must stop
        light_StationB(bool): Bool representing light signal for the track headed towards StationB 0 = GREEN, 1 = RED
        light_StationC(bool): Bool representing light signal for the track headed towards StationC 0 = GREEN, 1 = RED


    """
    #Determining switch position
    #Check if both tracks are occupied (ERROR CHECK)
    if((self.track_occupancies[11] or self.track_occupancies[12] or self.track_occupancies[13] 
        or self.track_occupancies[14] or self.track_occupancies[15])and (self.track_occupancies[6] or self.track_occupancies[7] or self.track_occupancies[8] 
        or self.track_occupancies[9] or self.track_occupancies[10])):
        self.light_StationB = False
        self.light_StationC = False
        self.Authority = 0
        print("EMERGENCY WARNING!")
        print("BOTH TRACKS ARE OCCUPIED")
        print("ALL TRAINS MUST STOP")
        print("STATION B = RED")
        print("STATION C = RED")
    
    #Check if path to station B is occupied
    elif (self.track_occupancies[6] or self.track_occupancies[7] or self.track_occupancies[8] 
        or self.track_occupancies[9] or self.track_occupancies[10]):
        self.switch_position = True
        self.light_StationC = False
        self.light_StationB = True
        print("Switch is connected to Block 6.")
        print("Station C Light is RED")
        print("Station B light is GREEN")
        print("Train is headed towards Station B.")

    #check if path to station C is occupied
    elif(self.track_occupancies[11] or self.track_occupancies[12] or self.track_occupancies[13] 
        or self.track_occupancies[14] or self.track_occupancies[15]):
        self.switch_position = False
        self.light_StationC = True
        self.light_StationB = False
        print("Switch is connected to Block 11.")
        print("Station C Light is GREEN.")
        print("Station B light is RED.")
        print("Train is headed towards Station C.")

    #Determing crossing signal / gate
    if (self.track_occupancies[2] or self.track_occupancies[3] or self.track_occupancies[4]):
        self.crossing_signal = True
        print("Crossing Signal is down. Do Not Cross!")
    else:
        self.crossing_signal = False
        print("Crossing Signal is up. Pedestrians can now cross the tracks.")

    return self.switch_position, self.crossing_signal, self.light_StationB, self.light_StationC, self.authority    

"""
# Test main function
def main():
    """
    #Test Bench
"""

    authority = 55
    #            yard   1      2      3     4       5      6      7      8      9     10      11     12     13     14     15
    blue_line1 = [False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False ]
    print(f"Blue Line Instance 1")

    HWPLC(blue_line1, authority)


if __name__ == "__main__":
    main()
"""
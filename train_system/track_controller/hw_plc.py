# train_system/track_controller/HW_PLC.py
class HWPLC:
    def __init__(self, block_array,authority):
        """
        Initialize Hardware Track Controller. Initializes the block_array (list of bools that are the track occupancies) Calls the check_occupaancies funcrtion
        """
        self.authority = authority
        self.block_array = block_array
        self.occupancy_var = False
        self.stationB_light = False
        self.stationC_light = False
        self.check_occupancies()
        self.close_crossing()
        
    def check_occupancies(self):
        """
        Check and print occupancy status of each block, then call the switch position function to determine if we should switch
        """
        num_blocks = len(self.block_array)
        for i in range(num_blocks):
            if self.block_array[i]:
                self.switch_positions()
        
    def close_crossing(self):
        """
        Check if adjacent blocks are occupied to decide closing the crossing gate.   Prints out whether the gate is closing or not.
        """
        self.occupancy_var = False
        length_array = len(self.block_array)
        for i in range(length_array):
            if (self.block_array[i]) or ( self.block_array[i-1]) or (i < length_array - 1 and self.block_array[i+1]):
                #print(f"Closing Crossing Gate.")
                self.occupancy_var = True
              
            else:
                #print(f"Opening Crossing Gate, Pedestrians Free To Cross.")
                self.occupancy_var = False

        if self.occupancy_var:
            print(f"Closing Crossing Gate.")

        else:
            print(f"Opening Crossign Gate. Pedestrains Can Now Cross Tracks.")

        self.light_signals()

    def light_signals(self):
        """
        In this function, based on occupancies, this function will be used to determine light signals RED = Occupied, stop... GREEN = Unoccupied, GO
        """
        light_color = ""
        if self.occupancy_var:
            light_color = "RED"
        else:
            light_color = "GREEN"
           
        print(f"Track Light Signal:{light_color}")

    def switch_positions(self):
        """
        This is the function for switching the actual switches.
        Going to use the occupancies and check at the switch point if any of block 11 or 6 are occupied
        If both are occupied, all trains will stop. 
        """

        if self.block_array[6] and self.block_array[11]:
            self.emergency_stop()

        elif self.block_array[6] or not self.block_array[11]:
            print(f"Switch from Block 5 to 11 is ON")
            print(f"Traveling to Station C, Authority: {self.authority} miles per hour")

        elif self.block_array[11] or not self.block_array[6]:
            print(f"Switch from Block 5 to 6 is ON")
            print(f"Traveling to Staton B, Authority: {self.authority} miles per hour")
        

        

    def emergency_stop(self):
        """
        E-STOP Function
        Goal:
            set authority to zero and lights to red
        """
        self.authority = 0
        print(f"EMERGENCY STOP! STOPPING ALL TRAINS!")
        

# Test main function
def main():
    """
    Test Bench
    """

    authority = 45
    #            station   1      2      3     4       5      6      7      8      9     10      11     12     13     14     15
    blue_line1 = [False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False ]
    print(f"Blue Line Instance 1")
    plc = HWPLC(blue_line1, authority)

    blue_line2 = [False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False ]
    print(f"Blue Line Instance 2")
    plc2 = HWPLC(blue_line2, authority)

    blue_line3 = [False, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False ]
    print(f"Blue Line Instance 3")
    plc3 = HWPLC(blue_line3, authority)


if __name__ == "__main__":
    main()

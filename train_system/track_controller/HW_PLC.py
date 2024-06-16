# train_system/track_controller/HW_PLC.py
class HWPLC:
    def __init__(self, block_array):
        """
        Initialize Hardware Track Controller. Initializes the block_array (list of bools that are the track occupancies) Calls the check_occupaancies funcrtion
        """
        self.block_array = block_array
        self.occupancy_var = False
        self.check_occupancies()
        self.close_crossing()
    
    def check_occupancies(self):
        """
        Check and print occupancy status of each block

        """
        num_blocks = len(self.block_array)
        for i in range(num_blocks):
            if self.block_array[i]:
                print(f"Block {i} is occupied.")
            else:
                print(f"Block {i} is not occupied.")
        
       

    def close_crossing(self):
        """
        Check if adjacent blocks are occupied to decide closing the crossing gate.   Prints out whether the gate is closing or not.
        """
        occupancy_var = False
        length_array = len(self.block_array)
        for i in range(length_array):
            if (self.block_array[i]) or ( self.block_array[i-1]) or (i < length_array - 1 and self.block_array[i+1]):
                print(f"Closing Crossing Gate.")
                self.occupancy_var = True
              
            else:
                print(f"Opening Crossing Gate, Pedestrians Free To Cross.")
                self.occupancy_var = False
            
        self.light_signals()


    def light_signals(self):
        """
        In this function, based on occupancies, we will determine if it is safe for people to cross
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
        Going to take the 
        """


# Test main function
def main():
    block_array = [True, False, False, False, False]
    plc = HWPLC(block_array)

if __name__ == "__main__":
    main()

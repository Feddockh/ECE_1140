# train_system/track_controller/HW_PLC.py

class HWPLC:
    def __init__(self,block_array):
        """
        Initialize Hardware Track Controller
        """
        self.block_array = block_array
    
    def check_occupancies(self):
        """
        check and print occupancy status of each block

        Returns:
        Prints example Track Occupancy for Now
        """
        num_blocks = len(self.block_array)
        for index in range(num_blocks):
            if self.block_array[index]:
                print(f"Block {index} is occupied.")
            else:
                print(f"Block {index} is not occupied.")



    """
    TEST MAIN
    """
def main():
    block_array = [True, False, True, True, False]
    plc = HWPLC(block_array)
    plc.check_occupancies()
    
    block_array2 = [False, True, True, False, False]
    plc = HWPLC(block_array2)
    plc.check_occupancies()

if __name__ == "__main__":
    main()
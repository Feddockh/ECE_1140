# train_system/track_controller/hwtrack_testbench.py

from hw_trackcontroller import HWTrackController

# Test main function
def main():
    """
    Test Bench
    """
    #Instance 1, where the track to Station C is occupied and we have to head to Station B
      #                  yard   1      2      3     4       5      6      7      8      9     10      11     12     13     14     15
    track_occupancies = [False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, True ]
    print(f"Blue Line Instance 1")
    authority = 45
    instance1 = HWTrackController(track_occupancies, authority)

    instance1.get_switch_position()
    instance1.get_crossing_signal()
    instance1.get_light_station_b()
    instance1.get_light_station_c()
    
   
   

if __name__ == "__main__":
    main()

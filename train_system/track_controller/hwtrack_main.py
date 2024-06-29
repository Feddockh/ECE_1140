# train_system/track_controller/hwtrack_main.py
from hw_trackcontroller import HWTrackController

# Test main function
def main():
    """
    Test Bench
    """
    
    print(f"Blue Line Example 1")
      #                  yard   1      2      3     4       5      6      7      8      9     10      11     12     13     14     15
    track_occupancies = [False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False ]
    authority = 45
    instance1 = HWTrackController(track_occupancies)

    instance1.get_switch_position()
    instance1.get_crossing_signal()
    instance1.get_light_station_b()
    instance1.get_light_station_c()

if __name__ == "__main__":
    main()

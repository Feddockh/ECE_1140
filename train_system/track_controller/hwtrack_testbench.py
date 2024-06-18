# train_system/track_controller/hwtrack_testbench.py

from hw_plc import HWPLC

# Test main function
def main():
    """
    Test Bench
    """

    authority = 55
    #            yard   1      2      3     4       5      6      7      8      9     10      11     12     13     14     15
    blue_line1 = [False, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False ]
    print(f"Blue Line Instance 1")

    PLC = HWPLC(blue_line1, authority)


if __name__ == "__main__":
    main()

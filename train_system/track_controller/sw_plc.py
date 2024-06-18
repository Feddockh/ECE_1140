#train_system/track_controller/sw_plc.py

"""
PLC program used to determine switch, crossing, and light state.
Representing a scenario where one train is going to Station B and
the other is going to Station C in that order. A crossing occurs at block 8.

Returns:
    switch(bool): Bool representing switch position - 0 = connected 
    6 & 1 = connected to 11. 
    crossing(bool): Bool representing crossing state - 0 = up & 1 = down
    light(bool): Bool representing light state - 0 = green & 1 = red
"""

#Determining light status
if (switch == False and track_occupancies[5]):
    light = True
    print("Light is red.")
elif (switch == False and track_occupancies[10]):
    light = True
    print("Light is red.")
else:
    light = False
    print("Light is green.")

#Determining switch position
if (track_occupancies[5] or track_occupancies[6] or track_occupancies[7]
    or track_occupancies[8] or track_occupancies[9]):
    switch = 1
    print("Switch is connected to Block 11.")
else:
    switch = 0
    print("Switch is connected to Block 6.")

#Determing crossing signal
if (track_occupancies[6] or track_occupancies[7] or track_occupancies[8]):
    cross = 1
    print("Crossing Signal is down.")
else:
    cross = 0
    print("Crossing Signal is up.")

#return switch, crossing, light    


"""
Testing code exec
"""
    


        
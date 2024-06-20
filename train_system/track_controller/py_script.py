import serial
from hw_trackcontroller import HWTrackController

def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust this if necessary
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            try:
                # Parse the incoming data
                parts = data.split(',')
                track_occupancies = [bool(int(x)) for x in parts[:-1]]
                authority = int(parts[-1])

                # Run the PLC logic
                controller = HWTrackController(track_occupancies, authority)
                switch_position = controller.get_switch_position()
                crossing_signal = controller.get_crossing_signal()
                light_station_b = controller.get_light_station_b()
                light_station_c = controller.get_light_station_c()

                # Prepare the result as a delimited string
                result = f"{int(switch_position)},{int(crossing_signal)},{light_station_b},{light_station_c}\n"
                ser.write(result.encode('utf-8'))
            except Exception as e:
                ser.write(('Error: ' + str(e) + '\n').encode('utf-8'))

if __name__ == "__main__":
    main()

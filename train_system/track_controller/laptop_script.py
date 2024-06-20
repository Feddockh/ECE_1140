import serial
import time

def main():
    ser = serial.Serial('COM1', 9600)  # Adjust this if necessary

    # Prepare the data to send as a delimited string
    track_occupancies = [False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, True]
    authority = 45
    data_to_send = ','.join(str(int(x)) for x in track_occupancies) + f",{authority}\n"

    ser.write(data_to_send.encode('utf-8'))

    time.sleep(1)  # Wait for the Raspberry Pi to process and send back the result

    if ser.in_waiting > 0:
        result = ser.readline().decode('utf-8').strip()
        try:
            # Parse the incoming data
            parts = result.split(',')
            switch_position = bool(int(parts[0]))
            crossing_signal = bool(int(parts[1]))
            light_station_b = parts[2]
            light_station_c = parts[3]
            print("Switch Position:", "Station C" if switch_position else "Station B")
            print("Crossing Signal:", "Down" if crossing_signal else "Up")
            print("Light Station B:", light_station_b)
            print("Light Station C:", light_station_c)
        except Exception as e:
            print("Error:", result)

if __name__ == "__main__":
    main()

import requests
from datetime import datetime
import time
import serial


def motion_deteted(bool):
    person_entered = bool
    return person_entered


def fetch_forced_status():
    forced_status_response = requests.get('http://192.168.43.181:8000/api/room_monitor/room/power_status/LLT1B/')
    forced_status_json_res = forced_status_response.json()
    is_forced_power_status = forced_status_json_res['is_forced_power_status']
    power_state = forced_status_json_res['power_state']
    return is_forced_power_status, power_state


def fetch_timetable():
    timet_response = requests.get('http://192.168.43.181:8000/api/room_monitor/timetable/LLT1B/')
    timet_json_res = timet_response.json()
    tt_array = []
    for session in timet_json_res:
        tt_array.append(session['start_time'])
        tt_array.append(session['end_time'])
    print (tt_array)
    return tt_array


def get_time_now():
    time_now = datetime.now()
    return time_now.hour


def update_forced_status(is_forced_power_status, power_state):
    API_ENDPOINT = "http://192.168.43.181:8000/api/room_monitor/room/power_status/LLT1B/update/"
    data = {'is_forced_power_status': is_forced_power_status, 'power_state': power_state}
    response = requests.put(url = API_ENDPOINT, data = data)
    # pastebin_url = response.text
    # print("The pastebin URL is: %s"%pastebin_url)


def power_server(is_forced_power_status, power_state, motion, time):
    i = 0
    tt_array = fetch_timetable() # timetable
    # is_forced_power_status, power_state = fetch_forced_status()
    time_now = time
    person_entered = motion
    if len(tt_array) > 0:
        for m in range(int((len(tt_array))/2)):
            if is_forced_power_status == True:
                if power_state == True:
                    print("Forced power on")
                    send_to_arduino(b'1\r\n')
                else:
                    print("Forced power off")
                    send_to_arduino(b'0\r\n')
            elif is_forced_power_status == False:
                if time_now >= tt_array[i] and time_now <= tt_array[i+1]:
                    if person_entered == True:
                        print("Power is on")
                        send_to_arduino(b'1\r\n')
                        update_forced_status(False, True)
                        power_change_listener(is_forced_power_status, power_state, person_entered, time, False)
                    else:
                        print("Power is still off, no motion")
                        send_to_arduino(b'0\r\n')
                        update_forced_status(False, False)
                        power_change_listener(is_forced_power_status, power_state, person_entered, time, False)
                else:
                    print("Power is off")
                    send_to_arduino(b'0\r\n')
            i = i + 2
    elif len(tt_array) == 0:
        if is_forced_power_status == True:
                if power_state == True:
                    print("Forced power on")
                    send_to_arduino(b'1\r\n')
                else:
                    print("Forced power off")
                    send_to_arduino(b'0\r\n')


def power_change_listener(is_forced_power_status, power_state, motion, time_now, spark):
    initial_motion = motion
    initial_status = is_forced_power_status
    initial_state = power_state
    initial_time = time_now
    time_now = get_time_now()
    motion = motion_deteted(True)
    is_forced_power_status, power_state = fetch_forced_status()

    if spark == True:
        update_forced_status(False, False)
        spark = False

    if initial_status != is_forced_power_status or initial_state != power_state or initial_motion != motion or initial_time != time_now:
        power_server(is_forced_power_status, power_state, motion, time_now)
        time.sleep(2)
        print("Maintaining state in if")
        power_change_listener(is_forced_power_status, power_state, motion, time_now, False)
    else:
        time.sleep(2)
        print("Maintaining state in else")
        power_change_listener(is_forced_power_status, power_state, motion, time_now, False)


def send_to_arduino(command):
    arduino_serial_data = serial.Serial('COM4', 9600)
    while True:
        if arduino_serial_data.inWaiting() > 0:
            my_data = arduino_serial_data.readline()
            arduino_serial_data.write(command)
            if my_data == b'0\r\n' or my_data == b'1\r\n' or my_data == b'Start\r\n' or my_data == b'Continue\r\n':
                if my_data == command:
                    print("Recieved !")
                    arduino_serial_data.close()
                    break


def arduino_connection_status():
    arduino_serial_data = serial.Serial('COM4', 9600)
    command = b'Con\r\n'
    i = 0
    while True:
        if arduino_serial_data.inWaiting() > 0:
            my_data = arduino_serial_data.readline()
            arduino_serial_data.write(command) # trigger to make serial available
            if my_data == b'Con\r\n':
                print("Connected !")
                arduino_serial_data.close()
                return True
                break
        elif i == 20:
            print("Connection failed...")
            arduino_serial_data.close()
            return False
            break
        else:
            print("Waiting for connection...")
            time.sleep(1)
            i = i + 1

spark = True
arduino_connection_status()
power_change_listener(False, True, True, 0, spark)


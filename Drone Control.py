from djitellopy import Tello
import time
import json
from paho.mqtt import client as mqtt_client



def move_left():
    tello.takeoff()
    time.sleep(1)
    tello.move_left(20)

def move_right():
    tello.takeoff()
    time.sleep(1)
    tello.move_right(20)

def move_forward():
    tello.takeoff()
    time.sleep(1)
    tello.move_forward(20)

def move_back():
    tello.takeoff()
    time.sleep(1)
    tello.move_back(20)

def move_up():
    tello.takeoff()
    time.sleep(1)
    tello.move_up(20)

def move_down():
    tello.takeoff()
    time.sleep(1)
    tello.move_down(20)

def query_battery():
    battery = tello.get_battery()
    return battery

def query_speed():
    speed = tello.get_speed_x()
    return speed

def query_attitude():
    pitch = tello.get_pitch()
    roll = tello.get_roll()
    yaw = tello.get_yaw()
    result = {"pitch": pitch, 
              "roll": roll,
              "yaw": yaw}
    return json.dumps(result)

def query_height():
    height = tello.get_height()
    return height

def query_temperature():
    temperature = tello.get_temperature()
    return temperature

def rotate_counter_clockwise():
    tello.takeoff()
    time.sleep(1)
    tello.rotate_counter_clockwise(90)
    
def rotate_clockwise():
    tello.takeoff()
    time.sleep(1)
    tello.rotate_clockwise(90)

def emergency():
    tello.is_flying = False
    tello.land()

def flip_left():
    tello.takeoff()
    tello.flip_left()

def flip_right():
    tello.takeoff()
    tello.flip_right()

def flip_forward():
    tello.takeoff()
    tello.flip_forward()

def flip_backward():
    tello.takeoff()
    tello.flip_back()


def check_flight_time():
    flight_time = tello.get_flight_time()
    return flight_time

def set_speed():
    set_speed = tello.set_speed(10)

def check_height():
    current_height = tello.get_height()
    return current_height

def set_direction_downward():
    tello.set_video_direction(tello.CAMERA_DOWNWARD)

def set_direction_forward():
    tello.set_video_direction(tello.CAMERA_FORWARD)


    



broker_address = 'localhost'
port = 1883
client_id = 'python'
topic = 'tello/command'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Connected to EMQX")
        else:
            print("Failed to connect")
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker_address, port)
    return client 

def handle_command(command):
    if command == "Takeoff":
        tello.takeoff()
    elif command == "Land":
        tello.land()
    elif command == "Emergency":
        emergency()
    elif command == "Flip Left":
        flip_left()
    elif command == "Flip Right":
        flip_right()
    elif command == "Flip Forward":
        flip_forward()
    elif command == "Flip Backward":
        flip_backward()
    elif command == "Rotate 90 Degrees Clockwise":
        rotate_clockwise()
    elif command == "Rotate 90 Degrees Anticlockwise":
        rotate_counter_clockwise()
    elif command == "Set Speed To 10cm/s":
        set_speed_to_10 = set_speed()
        print("Set Speed:", set_speed_to_10)
    elif command == "Set Video Direction Downward":
        video_direction = set_direction_downward()
        print("Set Video Direction: ", video_direction)
    elif command == "Set Video Direction Forward":
        video_direction2 = set_direction_forward()
        print("Set Video Direction: ", video_direction2)
    elif command == "Move Forward 20cm":
        move_forward()
    elif command == "Move Back 20cm":
        move_back()
    elif command == "Move Down 20cm":
        move_down()
    elif command == "Move Up 20cm":
        move_up()
    elif command == "Move Right 20cm":
        move_right()
    elif command == "Move Left 20cm":
        move_left()
    elif command == "Check Battery Percentage":
        battery_percentage = query_battery()
        print("Battery percentage:", battery_percentage)
    elif command == "Check Current Speed":
        current_speed = query_speed()
        print("Current speed:", current_speed)
    elif command == "Check Current Temperature":
        current_temperature = query_temperature()
        print("Current temperature:", current_temperature)
    elif command == "Check Current Attitude":
        current_attitude = query_attitude()
        print(current_attitude)
    elif command == "Check Flight Time":
        flight_time = check_flight_time()
        print("Flight time:", flight_time)
    elif command == "Check Height":
        height = check_height()
        print("Current height:", height)
    else:
        print("Unknown Command:", command)

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
        command = msg.payload.decode()
        
        handle_command(command)
    client.subscribe(topic)
    client.on_message = on_message

def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"hello {msg_count}"
        result = client.publish(topic, msg)
        status = result[0]
        if status ==0:
            print(f"Send '{msg}' to topic '{topic}'")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count +=1
        if msg_count > 2:
            break 



if __name__=="__main__":
    tello = Tello()
    tello.connect()
    client = connect_mqtt()
    subscribe(client)
    publish(client)
    print(client)
    client.loop_forever() 



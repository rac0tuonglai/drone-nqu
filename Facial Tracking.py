import cv2
import socket
from flask import Flask, Response, make_response
from flask_cors import CORS


face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_bounding_box(frame, prev_faces):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_gray = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)
    faces = face_classifier.detectMultiScale(resized_gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    
    if len(faces) == 0:
        faces = prev_faces

    scaled_faces = [(int(x*2), int(y*2), int(w*2), int(h*2)) for (x, y, w, h) in faces]
    for (x, y, w, h) in scaled_faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return scaled_faces

app = Flask(__name__)
CORS(app)

def receive_video():
    cap = cv2.VideoCapture('udp://0.0.0.0:11111')
    
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    prev_faces = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        if frame_count % 3 == 0:
            prev_faces = detect_bounding_box(frame, prev_faces)
        else:
            for (x, y, w, h) in prev_faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        frame_count += 1

    cap.release()

def send_command(command, address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(command.encode(), (address, port))

@app.route('/video_feed')
def video_feed():
    return Response(receive_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return make_response("Tello Video Stream with Face Detection. Go to /video_feed to see the stream.")

def main():
    tello_address = '192.168.10.1'
    command_port = 8889

    send_command('command', tello_address, command_port)
    send_command('streamon', tello_address, command_port)

    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()



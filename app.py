from flask import Flask, render_template, Response, request, jsonify
from camera import VideoCamera

app = Flask(__name__)

# Global camera instance (None to start)
camera = None

def get_camera():
    global camera
    if camera is None:
        camera = VideoCamera()
    return camera

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/workout')
def workout():
    return render_template('workout.html')

@app.route('/how-to-use')
def how_to_use():
    return render_template('how_to_use.html')

def gen(camera_instance):
    while True:
        frame = camera_instance.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    cam = get_camera()
    response = Response(gen(cam),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/set_exercise', methods=['POST'])
def set_exercise():
    data = request.get_json()
    exercise_name = data.get('exercise')
    if exercise_name:
        cam = get_camera()
        cam.set_exercise(exercise_name)
        return jsonify(success=True, exercise=cam.get_current_exercise_name())
    return jsonify(success=False), 400

@app.route('/current_exercise')
def current_exercise():
    cam = get_camera()
    return jsonify(exercise=cam.get_current_exercise_name())

@app.route('/reset_counter', methods=['POST'])
def reset_counter():
    cam = get_camera()
    cam.reset_counter()
    return jsonify(success=True)

if __name__ == '__main__':
    # Run slightly specifically to avoid localhost binding issues on some windows setups
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

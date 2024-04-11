import random
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_socketio import SocketIO

hint = ""

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('update_hint')
def handle_update_hint():
    global hint
    socketio.emit('hint_update', hint)


def random_RGB():
   global rgbValues
   rgbValues = [random.randint(0,255) for x in range(3)]
   # Generating the color image
   im = Image.open('static/css/images/rgbPlaceholder.png')
   im = im.convert('RGBA')
   data = np.array(im)
   global color_value
   color_value = str(rgbValues)


   r1, g1, b1 = 248, 225, 101 # rgbPlaceholder's RGB values
   r2, g2, b2, a2 = rgbValues[0], rgbValues[1], rgbValues[2], 255  # The new, RGB random values


   red, green, blue, alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
   mask = (red == r1) & (green == g1) & (blue == b1)
   data[:,:,:4][mask] = [r2, g2, b2, a2]


   im = Image.fromarray(data)
   im.save('static/css/images/rgbColor.png')

def guess_checker():
   global hint
   global correct_answer
   global distance
   distance =  abs(int(rgbValues[0])-int(user_value))

   if user_value == str(rgbValues[0]):
      hint=("CORRECT YEAH!!!")
   elif distance >= 100:
      hint=("The user is 100 or more off for R")
   elif distance >= 50:
      hint=("The user is 50 or more off for R")
   elif distance >= 25:
      hint=("The user is 25 or more off for R")
   elif distance >= 10:
      hint=("The user is 10 or more off for R")
   elif distance < 10:
      hint=("The user is under 10 values off for R")


@app.route('/') 
def home():
    random_RGB() 
    return render_template('home.html', color_value=color_value, hint=hint)


@app.route('/handle_data', methods=['POST'])  
def handle_data():
   global user_value
   formpath = request.form['user_guess']
   user_value = str(formpath) 
   guess_checker()
   return render_template('home.html')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8081)
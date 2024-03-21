import random
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

def random_RGB():
   global rgbValues
   rgbValues = [random.randint(0,255) for x in range(3)]
   # Generating the color image
   im = Image.open('static/css/images/rgbPlaceholder.png')
   im = im.convert('RGBA')
   data = np.array(im)
   global value
   value = str(rgbValues)


   r1, g1, b1 = 248, 225, 101 # rgbPlaceholder's RGB values
   r2, g2, b2, a2 = rgbValues[0], rgbValues[1], rgbValues[2], 255  # The new, RGB random values


   red, green, blue, alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
   mask = (red == r1) & (green == g1) & (blue == b1)
   data[:,:,:4][mask] = [r2, g2, b2, a2]


   im = Image.fromarray(data)
   im.save('static/css/images/rgbColor.png')

def guess_checker():
   global correct_answer
   
   if user_value == str(rgbValues[0]):
      print("--Correct--")
      correct_answer = True
   else:
      print("--Incorrect--")
      correct_answer = False
      #print(float(rgbValues[0]))


@app.route('/') 

def home():
    random_RGB() 
    return render_template('home.html', value=value)


@app.route('/handle_data', methods=['POST'])  

def handle_data():
   global user_value
   formpath = request.form['user_guess']
   user_value = str(formpath)
   #print(user_value) 
   guess_checker()
   return ("Pass")


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=8081)
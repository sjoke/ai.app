
# import the necessary packages
from tensorflow import keras
import numpy as np
from PIL import Image
import os
import io
from flask import request, Flask, send_from_directory, jsonify
from werkzeug.utils import secure_filename

# initialize our Flask application and the Keras model
app = Flask(__name__)
model = None
class_names = None
image_size = 28


def load_model():
    # load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras, but you can
    # substitute in your own networks just as easily)
    global model
    global class_names
    model = keras.models.load_model('model/quickDraw_new.h5')
    model.compile(loss='categorical_crossentropy',
                          optimizer='adam',
                          metrics=['accuracy'])

    # keras's bug, otherwise model.predict in predict function below will throw error
    random_sample = np.zeros((1,image_size, image_size, 1 ))
    model.predict(random_sample)

    with open("model/class_names.txt", "r") as f:
        class_names = f.readlines()


@app.route('/ai/quickdraw/predict', methods=['POST'])
def predict():
    image = request.files["file"].read()
    image = Image.open(io.BytesIO(image))

    # image = Image.open("model/sample/tooth.png")
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = np.expand_dims(image_array, axis=3)

    print(image_array.shape)
    assert len(image_array.shape) == 4

    predictResult = {}
    model_pred = model.predict(image_array)[0]
    predictResult['pred'] = getPred(model_pred)

    return jsonify(predictResult)


def getPred(prediction):
    pred_index = np.argmax(prediction)
    pred_label = class_names[pred_index]
    pred_prob = format(prediction[pred_index].item() * 100, '.2f')
    
    return {
        'label' : pred_label,
        'prob': pred_prob
    }

# static route

@app.route('/webapp', defaults={'path': ''})
@app.route('/webapp/<path:path>')
def serve(path):
    if(path == ""):
        return send_from_directory('webapp/build', 'index.html')
    return send_from_directory('webapp/', path)



# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    load_model()
    app.run(port=5000, debug=True)

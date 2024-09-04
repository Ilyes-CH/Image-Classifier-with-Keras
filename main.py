from flask import Flask, render_template, request, jsonify
from keras import models
from PIL import Image
import numpy as np

# init
app = Flask(__name__)
model = models.load_model("baseline.keras")

# const
PORT: int = 5501

# data_class
class_names = {
    0: 'airplane',
    1: 'automobile',
    2: 'bird',
    3: 'cat',
    4: 'deer',
    5: 'dog',
    6: 'frog',
    7: 'horse',
    8: 'ship',
    9: 'truck',
}

# model prediction function
def predict_image(model, file):
    img = Image.open(file)
    img = img.convert("RGB")
    img = img.resize((32, 32))
    data = np.asarray(img)
    data = data / 255.0
    probability = model.predict(np.array([data]))[0]
    top_prob = probability.max()
    top_pred = class_names[np.argmax(probability)]
    return top_prob, top_pred

# main routes
@app.route('/classifier')
def model_func():
    return render_template("index.html")

@app.route('/uploader', methods=["POST"])
def file_handler_func():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        top_prob, top_pred = predict_image(model, file)
        return jsonify({
            "prediction": top_pred,
            "probability": round(top_prob * 100, 2)
        })

# entry point
if __name__ == "__main__":
    app.run(debug=True, port=PORT)

from taipy.gui import Gui
from keras import models
from PIL import Image
import numpy as np

model = models.load_model("../baseline.keras")

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

def predict_image(model,path_to_img):
    img = Image.open(path_to_img)
    # because our model is trained on RGB images
    img = img.convert("RGB")
    # to match the size of our training imagesW
    img = img.resize((32,32))
    data = np.asarray(img) #tensor
    # print("before",data[0][0])
    # normalize data
    data = data / 255
    # print("after",data[0][0])
    probabilty = model.predict(np.array([data][:1]))
    # print(probabilty)
    top_prob = probabilty.max()
    # to return the value of the hashmap
    top_pred= class_names[np.argmax(probabilty)]
    
    # print(top_pred)
    # print(model.summary())
    # print(path_to_img)
    return top_prob, top_pred

content =""
img_path = "placeholder_image.png"
prob = 0
pred = ""


index = """
<|text-center|
<|{"logo.png"}|image|width=25vw|>

<|{content}|file_selector|extensions=.png|>
select an image from your file system

<|{pred}|> 

<|{img_path}|image|>

<|{prob}|indicator|value={prob}|min=0|max=100|width=25vw|>

>
"""


def on_change(state, name, value):
    if name == "content":
        top_prob, top_pred =  predict_image(model,value)
        state.prob = round(top_prob *100)
        state.pred = "this is a " + top_pred
        state.img_path = value
        print(top_pred)
        
        
        
app = Gui(page=index)

if __name__=="__main__":
    app.run(use_reloader=True)
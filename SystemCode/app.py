import os
from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
from form import PatientInfo
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__, template_folder='Template')

CLASSES = ['actinic keratosis', 'basal cell carcinoma', 'benign keratosis-like lesions', 'dermatofibroma', 'melanocytic nevi', 'melanoma', 'vascular lesions']

#Set secret key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

#set paths to upload folder
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGE_UPLOADS'] = os.path.join(APP_ROOT, 'static')

info_dict = {
"actinic keratosis": "Actinic keratosis is a rough, scaly patch on the skin that develops from years of exposure to the sun. Also known as a solar keratosis, an actinic keratosis enlarges slowly and usually causes no signs or symptoms other than a patch or small spot on your skin. However, if left untreated, it may develop into squamous cell carcinoma which is cancerous. You can reduce your risk of actinic keratosis by minimizing your sun exposure and protecting your skin from ultraviolet rays.",
"basal cell carcinoma": "Basal cell carcinoma is a cancerous type of skin lesion that develops in the basal cell layer located in the lower part of the epidermis. It is the most common type of skin cancer accounting for 80% of all cases. Basal cell carcinoma can look like open sores, red patches, pink growths, shiny bumps, scars or growths with slightly elevated, rolled edges and/or a central indentation. At times, Basal cell carcinoma may ooze, crust, itch or bleed. The lesions commonly arise in sun-exposed areas of the body.",
"benign keratosis-like lesions": "Benign keratosis is a slow and noncancerous type of skin growth that some people develop as they age. They can be left untreated as they are typically harmless. Most people will develop at least one seborrheic keratosis during their lifetime.",
"dermatofibroma": "Dermatofibromas is a small noncancerous and usually harmless skin growth, thus no treatment is required. They can grow anywhere on the body, but are most common on the arms, lower legs, and upper back. Dermatofibromas are seen in adults but are rare in children.",
"melanoma": "Melanoma is the most serious type of skin cancer that develops in the melanocyte cells that produce melanin — the pigment that gives your skin its color. Melanoma can also form in the eyes and, rarely, inside the body, such as in the nose or throat.",
"vascular lesions": "Vascular lesions are relatively common abnormalities of the skin and underlying tissues, more commonly known as birthmarks. While these birthmarks can look similar at times, they each vary in terms of origin and necessary treatment. They may be benign or malignant.",
"melanocytic nevi": "Melanocytic nevi is a benign type of melanocytic tumor that contains nevus cells. Patients with melanocytic nevi are considered to be at a higher risk of melanoma which is cancerous."
}

@app.route('/', methods=['GET','POST'])
def index():
    form = PatientInfo()
    if request.method == 'POST':
        uploaded_file = form.Image.data
        if uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config["IMAGE_UPLOADS"], filename)
            uploaded_file.save(file_path)
            image = tf.keras.preprocessing.image.load_img(file_path, target_size=(75,100))
            image = tf.keras.preprocessing.image.img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image = (image - 155) /53
            classifier = tf.keras.models.load_model("model.h5", compile=False) 
            prediction = classifier.predict([image])[0]
            prediction = np.argmax(prediction) 
            class_name = CLASSES[prediction]
            if class_name == "actinic keratosis":
              info = info_dict["actinic keratosis"]
            elif class_name == "basal cell carcinoma":
              info = info_dict["basal cell carcinoma"]
            elif class_name == "benign keratosis-like lesions":
              info = info_dict["benign keratosis-like lesions"]
            elif class_name == "dermatofibroma":
              info = info_dict["dermatofibroma"]
            elif class_name == "melanoma":
              info = info_dict["melanoma"]
            elif class_name == "vascular lesions":
              info = info_dict["vascular lesions"]
            else:
              info = info_dict["melanocytic nevi"]
            return render_template('result.html', image_path = filename, class_name = class_name, info = info)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug = True)


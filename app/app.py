from flask import Flask, render_template, request
import openai
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = 'your_openai_api_key_here'

# Function to process the crop image and convert it to text (assuming you have an image captioning or description mechanism)
def process_image(image):
    # Placeholder function: Add real image processing logic here (like using an OCR tool or an image captioning model)
    return "The crop seems to have yellowing leaves, possibly due to fungal disease."

# Home route with navigation buttons
@app.route('/')
def home():
    return render_template('index.html')

# Disease Prediction Route
@app.route('/disease', methods=['GET', 'POST'])
def disease_prediction():
    if request.method == 'POST':
        crop_image = request.files['crop_image']

        if crop_image:
            # Save the uploaded image temporarily to process it (optional)
            filename = secure_filename(crop_image.filename)
            image_path = os.path.join('uploads', filename)
            crop_image.save(image_path)

            # Process the image and get a description (for simplicity, we are assuming the description is generated)
            description = process_image(crop_image)

            # Use OpenAI API to generate a disease prediction based on the image description
            response = openai.Completion.create(
                engine="text-davinci-003",  # You can use other models if preferred
                prompt=f"Given the description of a crop: {description}, predict the disease and suggest a solution.",
                max_tokens=150
            )

            prediction = response.choices[0].text.strip()

            return render_template('disease.html', prediction=prediction)

    return render_template('disease.html', prediction=None)

# Yield Prediction Route
@app.route('/yield', methods=['GET', 'POST'])
def yield_prediction():
    if request.method == 'POST':
        crop_type = request.form['crop_type']
        location = request.form['location']

        # Use OpenAI API to generate a yield prediction based on crop type and location
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use a model appropriate for this task
            prompt=f"Predict the yield for {crop_type} crop grown in {location}. Provide an estimate in terms of quantity per acre or hectare.",
            max_tokens=150
        )

        # Extract the prediction from the response
        prediction = response.choices[0].text.strip()

        return render_template('yield.html', prediction=prediction)

    return render_template('yield.html', prediction=None)

if __name__ == '__main__':
    app.run(debug=True)

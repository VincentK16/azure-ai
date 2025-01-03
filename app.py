# filepath: your_flask_app/app.py
from flask import Flask, request, render_template, redirect, url_for, flash
from imageanalysis import analyze_image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'supersecretkey'  # Needed for flashing messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_url = request.form['image_url']
        visual_features = request.form.getlist('visual_features')
        gender_neutral_caption = request.form['gender_neutral_caption'] == 'True'
        model_version = request.form['model_version']

        if image_url:
            try:
                result = analyze_image(image_url, visual_features, gender_neutral_caption, model_version)
                return render_template('index.html', result=result)
            except Exception as e:
                flash(f"An error occurred: {str(e)}")
                return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
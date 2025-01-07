# filepath: your_flask_app/app.py
from flask import Flask, request, render_template, redirect, url_for, flash
from imageanalysis import analyze_image
from faceanalysis import analyze_face, verify_faces, find_similar_faces, generate_face_ids_from_folder, analyze_face_local
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['FACE_ID_FOLDER'] = 'static/face_ids' 
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

@app.route('/face', methods=['GET', 'POST'])
def face():
    if request.method == 'POST':
        image_url = request.form['image_url']

        if image_url:
            try:
                result = analyze_face(image_url)
                return render_template('face.html', result=result)
            except Exception as e:
                flash(f"An error occurred: {str(e)}")
                return redirect(url_for('face'))
    return render_template('face.html')

@app.route('/upload_faces', methods=['GET', 'POST'])
def upload_faces_route():
    if request.method == 'POST':
        if 'images' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('images')
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['FACE_ID_FOLDER'], filename).replace("\\", "/")
                file.save(file_path)
        face_ids = generate_face_ids_from_folder(app.config['FACE_ID_FOLDER'])
        flash('Files successfully uploaded')
        return render_template('upload_faces.html', face_ids=face_ids)
    return render_template('upload_faces.html')

@app.route('/find_similar', methods=['GET', 'POST'])
def find_similar_route():
    if request.method == 'POST':
        image = request.files['image']

        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace("\\", "/")
            image.save(image_path)

            try:
                detection_result = analyze_face_local(image_path)
                print()
                face_id = detection_result['face_ids'][0]
                print("Detection Face ID:", face_id)
                face_list = generate_face_ids_from_folder(app.config['FACE_ID_FOLDER'])
                if not face_list:
                    flash("No face IDs found in the folder.")
                    return redirect(url_for('find_similar_route'))
                similar_faces_result = find_similar_faces(face_id, face_list)
                return render_template('find_similar.html', detection_result=detection_result, similar_faces_result=similar_faces_result)
            except Exception as e:
                flash(f"An error occurred: {str(e)}")
                return redirect(url_for('find_similar_route'))
    return render_template('find_similar.html')

@app.route('/verify_faces', methods=['GET', 'POST'])
def verify_faces_route():
    if request.method == 'POST':
        image1 = request.files['image1']
        image2 = request.files['image2']

        if image1 and image2:
            filename1 = secure_filename(image1.filename)
            filename2 = secure_filename(image2.filename)
            image1_path = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
            image2_path = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
            image1.save(image1_path)
            image2.save(image2_path)

            try:
                result = verify_faces(image1_path, image2_path)
                return render_template('verify_faces.html', result=result)
            except Exception as e:
                flash(f"An error occurred: {str(e)}")
                return redirect(url_for('verify_faces_route'))
    return render_template('verify_faces.html')


if __name__ == '__main__':
    app.run(debug=True)
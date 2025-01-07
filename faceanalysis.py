# filepath: /C:/Users/vincentkok/Documents/OneDrive - Microsoft/Deliveries/AI/AI-3004/Demo/Web App/faceanalysis.py
import os
from dotenv import load_dotenv
from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import (
    FaceDetectionModel,
    FaceRecognitionModel,
    FaceAttributeTypeDetection03,
    FaceAttributeTypeRecognition04,
)

from azure.core.credentials import AzureKeyCredential
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

# Set the values of your face API endpoint and key
endpoint = os.getenv("FACE_ENDPOINT")
key = os.getenv("FACE_KEY")

print(endpoint, key)

if not endpoint or not key:
    raise ValueError("Missing environment variable 'FACE_ENDPOINT' or 'FACE_KEY'")

# Create a Face client
face_client = FaceClient(endpoint, AzureKeyCredential(key))

def analyze_face(image_url):
    # Detect faces in the image
    detected_faces = face_client.detect_from_url(
        url=image_url,
         detection_model='detection_03',
        recognition_model='recognition_04',
        return_face_id=True,
        return_face_landmarks=True,
         return_face_attributes=[
            "blur", "exposure", "glasses", "headPose", "mask", "occlusion", "qualityForRecognition"
        ]
    )

    if not detected_faces:
        raise Exception("No face detected in the image.")

    # Process the results and draw bounding boxes
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(img)

     # Load a font with a larger size
    font_path = "arial.ttf"  # Path to a .ttf font file
    font_size = 20  # Adjust the font size as needed
    font = ImageFont.truetype(font_path, font_size)

    for face in detected_faces:
        bbox = face.face_rectangle
        draw.rectangle([bbox.left, bbox.top, bbox.left + bbox.width, bbox.top + bbox.height], outline="blue", width=3)


        # Label face with face ID using the larger font
        draw.text((bbox.left, bbox.top - 10), face.face_id, fill="red", font=font)
         # Draw facial landmarks
        landmarks = face.face_landmarks.as_dict()
        for landmark, point in landmarks.items():
            draw.ellipse([point['x'] - 2, point['y'] - 2, point['x'] + 2, point['y'] + 2], outline="red", width=2)

    # Save the image with bounding boxes
    output_path = os.path.join("static", "uploads", "face_output.png")
    img.save(output_path)

    # Prepare the result dictionary
    result_dict = {
        "output_image": output_path,
        "faces": detected_faces,
        "landmarks": [face.face_landmarks.as_dict() for face in detected_faces]
    }

    return result_dict

def analyze_face_local(image_path):
    # Detect faces in the image from local file path
    with open(image_path, 'rb') as image:
        detected_faces = face_client.detect(
            image_content=image,
            detection_model='detection_03',
            recognition_model='recognition_04',
            return_face_id=True,
            return_face_attributes=[
                "blur", "exposure", "glasses", "headPose", "mask", "occlusion", "qualityForRecognition"
            ]
        )

    if not detected_faces:
        raise Exception("No face detected in the image.")

    # Process the results and draw bounding boxes
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Load a font with a larger size
    font_path = "arial.ttf"  # Path to a .ttf font file
    font_size = 20  # Adjust the font size as needed
    font = ImageFont.truetype(font_path, font_size)

    for face in detected_faces:
        bbox = face.face_rectangle
        draw.rectangle([bbox.left, bbox.top, bbox.left + bbox.width, bbox.top + bbox.height], outline="blue", width=3)

        # Label face with face ID using the larger font
        draw.text((bbox.left, bbox.top - 10), face.face_id, fill="white", font=font)
        

    # Save the image with bounding boxes
    output_path = os.path.join("static", "uploads", f"output_{os.path.basename(image_path)}").replace("\\", "/")
    img.save(output_path)

    # Prepare the result dictionary
    result_dict = {
        "output_image": output_path,
        "faces": detected_faces,
        "face_ids": [face.face_id for face in detected_faces]
    }

    return result_dict

def find_similar_faces(face_id, face_list):
    # Find similar faces
    similar_faces = face_client.find_similar(
        face_id=face_id,
        face_ids=face_list
    )

    # Prepare the result dictionary
    result_dict = {
        "similar_faces": similar_faces
    }

    return result_dict

def verify_faces(image1_path, image2_path):
    # Detect faces in the first image
    with open(image1_path, 'rb') as image1:
        detected_faces1 = face_client.detect(
            image1,
            detection_model='detection_03',
            recognition_model='recognition_04',
            return_face_id=True
        )

    if not detected_faces1:
        raise Exception("No face detected in the first image.")

    # Detect faces in the second image
    with open(image2_path, 'rb') as image2:
        detected_faces2 = face_client.detect(
            image2,
            detection_model='detection_03',
            recognition_model='recognition_04',
            return_face_id=True
        )

    if not detected_faces2:
        raise Exception("No face detected in the second image.")

    face_id1 = detected_faces1[0].face_id
    face_id2 = detected_faces2[0].face_id

        # Draw bounding boxes around detected faces in the first image
    img1 = Image.open(image1_path)
    draw1 = ImageDraw.Draw(img1)
    for face in detected_faces1:
        bbox = face.face_rectangle
        draw1.rectangle([bbox.left, bbox.top, bbox.left + bbox.width, bbox.top + bbox.height], outline="blue", width=3)
    output_image1_path = os.path.join("static", "uploads", f"output_{os.path.basename(image1_path)}")
    img1.save(output_image1_path)

    # Draw bounding boxes around detected faces in the second image
    img2 = Image.open(image2_path)
    draw2 = ImageDraw.Draw(img2)
    for face in detected_faces2:
        bbox = face.face_rectangle
        draw2.rectangle([bbox.left, bbox.top, bbox.left + bbox.width, bbox.top + bbox.height], outline="blue", width=3)
    output_image2_path = os.path.join("static", "uploads", f"output_{os.path.basename(image2_path)}")
    img2.save(output_image2_path)

    # Verify the faces
    verify_result = face_client.verify_face_to_face(
        face_id1=face_id1,
        face_id2=face_id2
    )

    # Prepare the result dictionary
    result_dict = {
        "face_id1": face_id1,
        "face_id2": face_id2,
        "confidence": verify_result.confidence,
        "is_identical": verify_result.is_identical,
        "output_image1": f"uploads/output_{os.path.basename(image1_path)}".replace("\\", "/"),
        "output_image2": f"uploads/output_{os.path.basename(image2_path)}".replace("\\", "/")
    }

    print (output_image1_path, output_image2_path)

    return result_dict

def generate_face_ids_from_folder(folder_path):
    face_ids = []
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename).replace("\\", "/")
        if os.path.isfile(image_path):
            try:
                detection_result = analyze_face_local(image_path)
                face_ids.extend([face.face_id for face in detection_result["faces"]])
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
    return face_ids

def find_similar_faces(face_id, face_list):
    # Find similar faces
    similar_faces = face_client.find_similar(
        face_id=face_id,
        face_ids=face_list
    )
    print(similar_faces)

    # Prepare the result dictionary
    result_dict = {
        "similar_faces": similar_faces
    }

    return result_dict
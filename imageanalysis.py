# filepath: /C:/Users/vincentkok/Documents/OneDrive - Microsoft/Deliveries/AI/AI-3004/Demo/Web App/imageanalysis.py
import os
from dotenv import load_dotenv
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from PIL import Image, ImageDraw
import requests
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

# Set the values of your computer vision endpoint and computer vision key
endpoint = os.getenv("VISION_ENDPOINT")
key = os.getenv("VISION_KEY")

if not endpoint or not key:
    raise ValueError("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")

# Create an Image Analysis client
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

def analyze_image(image_url, visual_features, gender_neutral_caption, model_version):
    # Convert visual features to the appropriate enum values
    visual_features_enum = [getattr(VisualFeatures, vf) for vf in visual_features]

    # Get a caption for the image. This will be a synchronously (blocking) call.
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=visual_features_enum,
        smart_crops_aspect_ratios=[0.9, 1.33],
        language="en",
        model_version=model_version,
        gender_neutral_caption=gender_neutral_caption
    )

    # Process the results and draw bounding boxes
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(img)

    if result.smart_crops is not None:
        for smart_crop in result.smart_crops.list:
            bbox = smart_crop.bounding_box
            draw.rectangle([bbox.x, bbox.y, bbox.x + bbox.width, bbox.y + bbox.height], outline="red", width=3)

    if result.people is not None:
        for person in result.people.list:
            if person.confidence > 0.9:
                bbox = person.bounding_box
                draw.rectangle([bbox.x, bbox.y, bbox.x + bbox.width, bbox.y + bbox.height], outline="blue", width=3)

    # Save the image with bounding boxes
    output_path = os.path.join("static", "uploads", "output.png")
    img.save(output_path)

    # Prepare the result dictionary
    result_dict = {
        "output_image": output_path,
        "metadata": result.metadata,
        "model_version": result.model_version
    }

    # Add selected visual features to the result dictionary
    if "TAGS" in visual_features:
        result_dict["tags"] = result.tags.list
    if "CAPTION" in visual_features:
        result_dict["caption"] = result.caption
    if "DENSE_CAPTIONS" in visual_features:
        result_dict["dense_captions"] = result.dense_captions.list
    if "READ" in visual_features:
        result_dict["read"] = result.read
    if "SMART_CROPS" in visual_features:
        result_dict["smart_crops"] = result.smart_crops
    if "OBJECTS" in visual_features:
        result_dict["objects"] = result.objects
    if "PEOPLE" in visual_features:
        result_dict["people"] = result.people

    print(result_dict)

    return result_dict
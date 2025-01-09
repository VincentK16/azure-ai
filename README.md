# Azure AI Vision Project

This repository contains code designed to faciliate your experimentation and exploration with the Azure AI Vision service. 

Azure AI services help developers and organizations to rapidly create intelligent, cutting-edge, market-ready, and responsible applications with out-of-the-box and pre-built and customizable APIs and models. Example applications include natural language processing (NLP) for conversations, search, monitoring, translation, speech, vision, and decision-making.

Most Azure AI services are available through REST APIs and client library SDKs in popular development languages. For more information, see each service's documentation.

## Seeing the Wonderful World of AI with Azure AI Vision service
### Azure AI Vision - Image Analaysis
<br>


https://github.com/user-attachments/assets/ad7d4fdd-71a3-4707-aab8-f69c4dda66c4



### Azure AI Vision - Face API
<img width="601" alt="image" src="https://github.com/user-attachments/assets/80c62579-fe5f-445d-b1ec-46c7a5f34ff3" />

## Getting Started

Follow the steps below to set up your environment and start utilizing the features of this repository (📌there's also the base code imageanalysis.py for understanding the SDK methods for Image Analysis):

### Prerequisites

- Python (>= 3.8)
- Visual Studio Code
  
### Installation

1. Clone this repository to your local machine.

```bash
git clone https://github.com/VincentK16/azure-ai-vision.git
```

2. Navigate to the project directory.

```bash
cd azure-ai-vision
```

3. Create a virtual environment.

```bash
python -m venv <name_of_your_env>
```

4. Activate the virtual environment.

- On Windows:

```bash
<name_of_your_env>\Scripts\activate
```

- On macOS/Linux:
```bash
source <name_of_your_env>/bin/activate
```

5. Install project dependencies from the requirements.txt file.

```bash
pip install -r requirements.txt
```

6. Create a .env file in the root directory of your project to store sensitive information such as the Azure OpenAI resource's keys. You can find a sample .env file in the repository called `.env_sample`. Duplicate this file and rename it to `.env`, then fill in the necessary values.

```bash
cp .env_sample .env
```

Now, you're ready to use the secrets stored in your `.env` file securely within your project. Feel free to customize the `.env` file with your other specific secrets and configurations as needed.

**Note: Never share your `.env` file publicly or commit it to version control systems like Git, as it contains sensitive information. The best practice is to use a `.gitignore` file in your repo to avoid commiting the `.env` file.**

7. Run the web app.
   
```bash
python app.py
```

8. Browse to the web app.

```bash
https://127.0.0.1:5000/
```

### Web App Routes
```bash
- Image Analysis: https://127.0.0.1:5000/
- Face Analysis: https://127.0.0.1:5000/face
- Verify Faces: https://127.0.0.1:5000/verify_faces
```


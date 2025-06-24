# 🤖 RT-FaceAuth

A **Real-Time Face Authentication System** built with **Python**, **OpenCV**, and **face_recognition**, using **Cloudinary** for cloud image storage. This project uses webcam video to recognize faces and display related user info with a custom UI overlay.

---

## 🎯 Features

- 🎥 Real-time face detection and recognition using webcam
- 🧠 Face encoding with `face_recognition`
- ☁️ Image upload and retrieval via **Cloudinary**
- 🖼️ UI overlays using `cvzone` and OpenCV
- 📦 Local storage of face encodings with `pickle`
- 🧾 Display of user info and attendance

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Face Recognition**: OpenCV, face_recognition
- **Cloud Storage**: Cloudinary
- **UI Overlay**: cvzone
- **Data Storage**: pickle, local files
- **Virtual Environment**: venv

---

## 📁 Project Structure

![image](https://github.com/user-attachments/assets/c1b70c0e-e822-4cc2-919b-652447ceaa28)


less
Copy
Edit

---

## ☁️ Cloudinary Setup

1. Create a free account at [Cloudinary](https://cloudinary.com)
2. Note your:
   - `cloud_name`
   - `api_key`
   - `api_secret`
3. Create a file named `cloudinary_config.py`:

```python
import cloudinary
import cloudinary.uploader

cloudinary.config(
  cloud_name="your_cloud_name",
  api_key="your_api_key",
  api_secret="your_api_secret"
)

def upload_to_cloudinary(image_path):
    result = cloudinary.uploader.upload(image_path)
    return result['secure_url']
📦 Setup Instructions
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/yourusername/RT-FaceAuth.git
cd RT-FaceAuth
2. Create and activate virtual environment
bash
Copy
Edit
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
3. Install dependencies
bash
Copy
Edit
pip install opencv-python face_recognition cvzone cloudinary numpy
🧠 Encode Faces
Add clear face images to the Images/ folder.

Run:

bash
Copy
Edit
python EncodeGenerator.py
This will:

Encode each face

Save encodings in EncodeFile.p

Upload images to Cloudinary and print URLs

🔍 Run Real-Time Recognition
Start the webcam-based face authentication system:

bash
Copy
Edit
python Main.py
🧑‍💻 Author
Made with ❤️ by Kamlesh Kumar Verma

GitHub: @kamlesh1002

Email: kamlesh1002@gmail.com

📜 License
Licensed under the MIT License

✅ Future Enhancements
Add local CSV/SQLite attendance logs

GUI for adding new users

Multiple camera support

Face registration via UI

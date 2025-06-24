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

python```
🧑‍💻 Author
Made with ❤️ by Kamlesh Kumar Verma

GitHub: [@kamlesh1002](https://github.com/kamalkumarverma)

Email: kamleshverma1002@gmail.com

📜 License
Licensed under the MIT License

✅ Future Enhancements
Add local CSV/SQLite attendance logs

GUI for adding new users

Multiple camera support

Face registration via UI


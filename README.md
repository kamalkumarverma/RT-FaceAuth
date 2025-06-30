# 🤖 RT-FaceAuth

A **Real-Time Face Authentication System** built with **Python**, **OpenCV**, and **face_recognition**, using **Cloudinary** for cloud image storage. This project uses webcam video to recognize faces and display related user info with a custom UI overlay.

---
![image](https://github.com/user-attachments/assets/72ee97ae-9c21-4f63-be3f-3ed19d0586a9)

![image](https://github.com/user-attachments/assets/2bb8550d-c259-4b66-ab0a-2652416c6b53)
![image](https://github.com/user-attachments/assets/8f018f61-13b1-40e0-b191-cf3159b55e5c)
![image](https://github.com/user-attachments/assets/58c1e936-e516-4d82-92a2-cf4034456c15)
![image](https://github.com/user-attachments/assets/4f4e42f0-3004-46fa-aa68-d13a1ae5d2a0)

![image](https://github.com/user-attachments/assets/fce332d1-6111-4685-9b0c-fac2f761d603)

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


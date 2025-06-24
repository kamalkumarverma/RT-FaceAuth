import cv2
import face_recognition
import pickle
import numpy as np
import requests
import cloudinary
import os
import json


# Cloudinary Configuration

cloudinary.config(
    cloud_name="",
    api_key="",
    api_secret="",
    secure=True
)

"""

def download_student_data():
    try:
        response = requests.get("https://res.cloudinary.com/dlzxrsnps/raw/upload/students_data.json")
        response.raise_for_status()
        print(response.json())
        return response.json()
    except Exception as e:
        print("Error downloading student data:", str(e))
        return None

"""

def read_local_student_data():
    try:
        with open("students_data.json", "r") as file:
            data = json.load(file)
            #print(data)  # print full dict in one line
            return data
    except Exception as e:
        print("Error reading students_data.json:", str(e))
        return None




def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        #print(cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR))
        return cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Error downloading image from {url}: {str(e)}")
        return None

def download_cloudinary_images(student_data):
    img_list = []
    student_ids = []
    for student_id, info in student_data.items():
        try:
            img = download_image(info['image_url'])
            if img is not None:
                img_list.append(img)
                student_ids.append(student_id)
                print(f"Downloaded Cloudinary image for student {student_id}")
        except Exception as e:
            print(f"Error downloading Cloudinary image for student {student_id}: {str(e)}")
    return img_list, student_ids



def find_encodings(images_list):
    encode_list = []
    for img in images_list:
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # face recognition use rgb format 
            face_encodings = face_recognition.face_encodings(img)
            if face_encodings:
                encode_list.append(face_encodings[0])
            else:
                print("Warning: No face found in image")
        except Exception as e:
            print("Error encoding face:", str(e))
    return encode_list



def main():
    print("Starting Cloudinary-only encoding process...")
    #student_data = download_student_data()
    student_data = read_local_student_data()
    if not student_data:
        print("No student data found in student_data.json. Exiting...")
        return



    cloud_images, cloud_ids = download_cloudinary_images(student_data)
    #print(cloud_images)
    #print( cloud_ids)
    print(f"Generating face encodings for {len(cloud_images)} Cloudinary images...")
    encode_list_known = find_encodings(cloud_images)
    encode_list_with_ids = [encode_list_known, cloud_ids]

    try:
       with open("EncodeFile.p", 'wb') as file:
           pickle.dump(encode_list_with_ids, file)
           print(f"Encodings saved successfully for {len(encode_list_known)} faces")
    except Exception as e:
       print("Error saving encodings:", str(e))

if __name__ == "__main__":
    main()

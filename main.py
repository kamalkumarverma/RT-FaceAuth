import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import requests
from datetime import datetime
import json
import cloudinary # type: ignore
import cloudinary.uploader # type: ignore
import time 

# Cloudinary Configuration for data 
cloudinary.config(
    cloud_name="",
    api_key="",
    api_secret="",
    secure=True
)

# Download and initialize student data

def read_local_student_data():
    try:
        with open("students_data.json", "r") as file:
            data = json.load(file)
            #print(data)  # print full dict in one line
            return data
    except Exception as e:
        print("Error reading students_data.json:", str(e))
        return None

"""
def initialize_student_data():
    '''Download and initialize student data'''
    try:
        response = requests.get("https://res.cloudinary.com/dlzxrsnps/raw/upload/students_data.json")
        response.raise_for_status()
        #print(response.json())
        return response.json()
        
    except Exception as e:
        print("Error initializing student data:", str(e))
        return {}
"""

def download_student_image(image_url):
    """Download student image from Cloudinary"""
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        return cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
    except Exception as e:
        print("Error downloading student image:", str(e))
        return None

def update_attendance(student_id, student_data):
    """Update attendance record in Cloudinary"""
    try:
        # Update local data
        student_info = student_data[student_id]
        student_info['total_attendance'] += 1
        student_info['last_attendance_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save updated data to file
        with open('students_data.json', 'w') as f:
            json.dump(student_data, f)
        
        # Upload to Cloudinary
        cloudinary.uploader.upload('students_data.json',
                                public_id='students_data',
                                resource_type='raw',
                                overwrite=True)
    except Exception as e:
        print("Error updating attendance:", str(e))

def initialize_camera():
    """Initialize camera with retry logic try 3 time"""
    max_retries = 3
    for i in range(max_retries):
        cap = cv2.VideoCapture(i)  # Try different indices
        if cap.isOpened():
            print(f"Successfully opened camera at index {i}")
            cap.set(3, 640)
            cap.set(4, 480)
            return cap
        cap.release()
    
    # Try the default camera index
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("Successfully opened default camera")
        cap.set(3, 640)
        cap.set(4, 480)
        return cap
    
    print("Failed to initialize any camera")
    return None

def recently_marked(student_info, seconds=50):
    try:
        last_time = datetime.strptime(student_info['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
        return (datetime.now() - last_time).total_seconds() < seconds
    except Exception as e:
        print("Error parsing last_attendance_time:", str(e))
        return False

def main():
    # Initialize student data
    #student_data = initialize_student_data()
    student_data     = read_local_student_data()
    print(student_data)
    if not student_data:
        return
    
    # Load face encodings
    try:
        with open('EncodeFile.p', 'rb') as file:
            encode_list_with_ids = pickle.load(file)
        encode_list_known, student_ids = encode_list_with_ids
        #print("encode data 128*d  face encode data",encode_list_known)
        #print(student_ids)
    except Exception as e:
        print("Error loading face encodings:", str(e))
        return

    
    
    # Initialize camera with retry logic
    cap = initialize_camera()
    if cap is None:
        print("Cannot proceed without camera access")
        return
    
    # Load background and mode images
    img_background = cv2.imread('Resources/background.png')
    if img_background is None:
        print("Error loading background image")
        cap.release()
        return
    
    # Load mode images
    mode_path_list = os.listdir('Resources/Modes')
    img_mode_list = [cv2.imread(os.path.join('Resources/Modes', path)) for path in mode_path_list]

    #print("img_mode_list strated ....")
    #print(img_mode_list)
    #print("img_mode_list ended ....")


    # Attendance system variables
    mode_type = 0
    counter = 0
    current_id = -1
    img_student = None
    
    
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image from camera - retrying...")
            time.sleep(1)  # Wait before retrying
            cap.release()
            cap = initialize_camera()
            if cap is None:
                break
            continue
        
        # Process frame for face recognition
        img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(img_small)
        # encode capture  face in web cam 
        face_encodings = face_recognition.face_encodings(img_small, face_locations)
        
        # Update background display
        img_background[162:162 + 480, 55:55 + 640] = img
        img_background[44:44 + 633, 808:808 + 414] = img_mode_list[mode_type]
        
        if face_locations:
            for encode_face, face_loc in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(encode_list_known, encode_face)
                print("matches : ",matches)
                face_distances = face_recognition.face_distance(encode_list_known, encode_face)
                print("face_distances: ",face_distances)

                match_index = np.argmin(face_distances)
                print("match_index : ",match_index)
                
                if matches[match_index]:
                    # Draw rectangle around detected face
                    y1, x2, y2, x1 = face_loc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    img_background = cvzone.cornerRect(img_background, bbox, rt=0)
                    
                    current_id = student_ids[match_index]
                    if counter == 0:
                        cvzone.putTextRect(img_background, "Loading", (275, 400))
                        cv2.imshow("Face Attendance", img_background)
                        cv2.waitKey(1)
                        counter = 1
                        mode_type = 1
            
            if counter != 0:
                if counter == 1:
                    # Get student info
                    student_info = student_data.get(current_id, {})
                    print("Recognized student:", student_info)
                    
                    # Download student image
                    if 'image_url' in student_info:
                        img_student = download_student_image(student_info['image_url'])
                    
                    # Check attendance time
                    try:
                        last_time = datetime.strptime(student_info['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                        seconds_elapsed = (datetime.now() - last_time).total_seconds()
                        
                        if seconds_elapsed > 30:
                            update_attendance(current_id, student_data)
                        else:
                            mode_type = 3
                            counter = 0
                            img_background[44:44 + 633, 808:808 + 414] = img_mode_list[mode_type]
                    except Exception as e:
                        print("Error processing attendance time:", str(e))
                
                if mode_type != 3:
                    if 10 < counter < 20:
                        mode_type = 2
                    
                    img_background[44:44 + 633, 808:808 + 414] = img_mode_list[mode_type]
                    
                    if counter <= 10:
                        # Display student info
                        cv2.putText(img_background, str(student_info.get('total_attendance', 0)), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(img_background, str(student_info.get('major', '')), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(img_background, str(current_id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(img_background, str(student_info.get('standing', '')), (910, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(img_background, str(student_info.get('year', '')), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(img_background, str(student_info.get('starting_year', '')), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        
                        # Display student name centered
                        name = student_info.get('name', '')
                        (w, h), _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(img_background, name, (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                        
                        # Display student image if available
                        if img_student is not None:
                            img_student_resized = cv2.resize(img_student, (216, 216))
                            img_background[175:175 + 216, 909:909 + 216] = img_student_resized
                    
                    counter += 1
                    
                    if counter >= 20:
                        counter = 0
                        mode_type = 0
                        img_student = None
                        img_background[44:44 + 633, 808:808 + 414] = img_mode_list[mode_type]
        else:
            mode_type = 0
            counter = 0
        
        # Display the result
        cv2.imshow("Face Attendance", img_background)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    main()

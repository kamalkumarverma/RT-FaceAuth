import cloudinary
import cloudinary.uploader
import json

# Cloudinary Configuration
cloudinary.config(
    cloud_name="dlzxrsnps",
    api_key="",
    api_secret="",
    secure=True
)

# Student data structure
data = {
    "987645": {
        "name": "kamal Kumar 1234",
        "major": "CSE",
        "starting_year": 2022,
        "total_attendance": 7,
        "standing": "X",
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34",
        "image_url": "https://res.cloudinary.com/dlzxrsnps/image/upload/987645.jpg"
    },
    "321654": {
        "name": "Jai Kumar",
        "major": "Robotics",
        "starting_year": 2025,
        "total_attendance": 7,
        "standing": "A",
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34",
        "image_url": "https://res.cloudinary.com/dlzxrsnps/image/upload/321654.png"
    },
    "852741": {
        "name": "Aadhya Joshi",
        "major": "Economics",
        "starting_year": 2021,
        "total_attendance": 12,
        "standing": "B",
        "year": 1,
        "last_attendance_time": "2022-12-11 00:54:34",
        "image_url": "https://res.cloudinary.com/dlzxrsnps/image/upload/852741.png"
    },
    "963852": {
        "name": "Elon Musk",
        "major": "Physics",
        "starting_year": 2020,
        "total_attendance": 7,
        "standing": "G",
        "year": 2,
        "last_attendance_time": "2022-12-11 00:54:34",
        "image_url": "https://res.cloudinary.com/dlzxrsnps/image/upload/963852.png"
    },
        "123456": {
        "name": "kamal kumar 542",
        "major": "CSE",
        "starting_year": 2022,
        "total_attendance": 0,
        "standing": "M",
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34",
        "image_url": "https://res.cloudinary.com/dlzxrsnps/image/upload/123456.png"
    }
}

def upload_student_images():
    """Upload sample student images to Cloudinary"""
    students = {
        "987645": "Images/987645.jpg",
        "321654": "Images/321654.png",
        "852741": "Images/852741.png",
        "963852": "Images/963852.png",
        "123456": "Images/123456.png",


    }
    
    for student_id, image_path in students.items():
        try:
            result = cloudinary.uploader.upload(image_path, public_id=student_id)
            print(f"Uploaded image for student {student_id}: {result['secure_url']}")
        except Exception as e:
            print(f"Error uploading image for student {student_id}: {str(e)}")

def main():
    # First upload the student images
    upload_student_images()
    
    # Then save and upload the student data JSON
    try:
        with open('students_data.json', 'w') as f:
            json.dump(data, f)
        
        result = cloudinary.uploader.upload('students_data.json',
                                         public_id='students_data',
                                         resource_type='raw')
        print("Student data uploaded successfully:", result['secure_url'])
    except Exception as e:
        print("Error uploading student data:", str(e))

if __name__ == "__main__":
    main()

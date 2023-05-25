import cv2
import time
import os
import requests
from PIL import Image
from six import BytesIO

def take_picture():
    # Create the "pictures" folder if it doesn't exist
    if not os.path.exists("pictures"):
        os.makedirs("pictures")

    # Access the camera
    cap = cv2.VideoCapture(1)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error opening the camera")
        return

    # Create a loop to capture images every 3 seconds
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if ret:
            # Show the captured image
            frame = cv2.convertScaleAbs(frame, alpha=2)

            cv2.imshow("Camera", frame)

            # Delete the previous image
            prev_image_path = os.path.join("pictures", "image.jpg")
            if os.path.exists(prev_image_path):
                os.remove(prev_image_path)

            # Save the image to a file
            filename = os.path.join("pictures", "image.jpg")
            cv2.imwrite(filename, frame)

            # Convert the image to PIL format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame)

            # Convert the PIL image to bytes
            with BytesIO() as stream:
                pil_image.save(stream, format="JPEG")
                stream.seek(0)
                img_for_post = stream.read()

            files = {'file': (f'image.jpg', img_for_post)}

            response = requests.post(
                url="http://10.102.15.193:8000/upload",
                files=files
            )

            # Check the response status
            if response.status_code == 200:
                print("Image uploaded successfully")
            else:
                print("Error uploading image")

            # Wait for 1 second
            time.sleep(1)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()

# Call the function to start capturing images and sending them to the API
take_picture()

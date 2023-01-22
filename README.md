# FaceTrack
An AI Based Facial Attendance System created in 1 day for T-Hunt Hackathon, Manipal University Jaipur.

## Credits for the project:

- **Mr. Abhay Tripathi ([@abhaytr](https://github.com/abhaytr))**:
  - Developed the Whole Backend i.e. made the model trainer and model recognizer using OpenCV standard facial recognizer.
  - Developed the WebSocket Server to receive and send facial data in the form of Base64 Images.
  - Developed the Frontend Script using JavaScript to take camera input from the client browser to get facial data and integrated it with the WebSocket Server by creating endpoints on the server for registration and marking attendance i.e model training from the received data and then student recognition from the received facial data in the form of Base64 images.
  - Developed the SQLite Database on the backend to store registered students data and to mark and store the attendace of each student per day.

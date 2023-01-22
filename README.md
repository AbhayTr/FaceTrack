# FaceTrack
An AI Based Facial Attendance System created in 1 day for T-Hunt Hackathon, Manipal University Jaipur.

## Instructions to deploy and use the Web App
  - Donwload the project and extract the files in any folder.
  - Open Command Prompt/Terminal and navigate to the **"Backend"** folder.
  - In the **"Backend"** folder, run the **"app.py"** file to start the Facial Recognizer AI WebSocket Server by running the following command:
    
    ```bash
    python app.py
    ```
    
  - Then, open a new instance of the Command Prompt/Terminal and navigate to the **"Frontend"** folder.
  - run the following command in the **"Frontend"** directory:
    
    ```bash
    python -m http.server 5000
    ```
    
    Note: here 5000 is the port at which the HTTP Server will run and you could set it to anything you want.

## Credits for the project:

- **Mr. Abhay Tripathi ([@abhaytr](https://github.com/abhaytr))**:
  - Developed the Whole Backend i.e. made the model trainer and model recognizer using OpenCV standard facial recognizer.
  - Developed the WebSocket Server to receive and send facial data in the form of Base64 Images.
  - Developed the SQLite Database on the backend to store registered students data and to mark and store the attendance of each student per day.
  - Developed the Frontend Script using JavaScript to take camera input from the client browser to get facial data and integrated it with the WebSocket Server by creating endpoints on the server for registration and marking attendance i.e model training from the received facial data from the registration page and then student recognition from the received facial data from the mark attendance page in the form of Base64 images.
  - Developed the Frontend UI using HTML and Bootstrap CSS Framework to take Camera Input and User Data from the client browser in the Registration and Mark Attendance Pages.

- **Mr. Nikhil Dixit ([@nikdixit](https://github.com/nikdixit))**:
  - Developed the Home Page of the Frontend using HTML and Bootstrap CSS Framework.
  - Developed the Frontend of Register and Mark Attendance Pages using HTML and Bootstrap CSS Framework.

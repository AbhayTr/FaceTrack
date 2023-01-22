# FaceTrack
An AI Based Facial Attendance System developed in 1 day for the T-Hunt Hackathon, Manipal University Jaipur.

## Prerequisites to deploy and use the Web App
  - **Python** should be installed on the system to run the Backend of the Web App.
  - **Pip** should be installed on the system to install dependencies of the Back End of the Web App.
  - The following packages should be installed by using pip on the system (run the following commands on Command Prompt/Terminal after installing python and pip to install them):
    
    ```bash
    pip install tornado
    pip install opencv-python
    pip install numpy
    pip install Pillow
    ```

## Instructions to deploy and use the Web App
  - Donwload the project and extract the files in any folder.
  - Open Command Prompt/Terminal and navigate to the **"Backend"** folder.
  - In the **"Backend"** folder, run the **"app.py"** file to start the Facial Recognizer AI WebSocket Server by running the following command:
    
    ```bash
    python app.py
    ```
    
  - Then, open a new instance of the Command Prompt/Terminal and navigate to the **"Frontend"** folder.
  - Run the following command in the **"Frontend"** directory to start the Frontend HTTP Server:
    
    ```bash
    python -m http.server 5000
    ```
    
    Note: here 5000 is the port at which the HTTP Server will run and you could set it to anything you want.
  
  - Done! The Web App is now deployed and can be accessed at **"http://localhost:5000"** (replace 5000 with the port which you used in the previous command).
  - In the Web App, first go to the Register page to register yourself in the System.
  - Then, go to the Mark Attendance page to mark your attendance for the day.

## Credits for the Project

- **Mr. Abhay Tripathi ([@abhaytr](https://github.com/abhaytr))**:
  - Developed the complete Backend i.e. made the model trainer and model recognizer using OpenCV standard facial recognizer.
  - Developed the WebSocket Server to receive and send facial data in the form of Base64 Images.
  - Developed the SQLite Database on the backend to store registered students data and to mark and store the attendance of each student per day.
  - Developed the Frontend Script using JavaScript to take camera input from the client browser to get facial data and integrated it with the WebSocket Server by creating endpoints on the server for registration and marking attendance i.e model training from the received facial data from the registration page and then student recognition from the received facial data from the mark attendance page in the form of Base64 images.
  - Developed the Frontend UI using HTML and Bootstrap CSS Framework to take Camera Input and User Data from the client browser in the Registration and Mark Attendance Pages.

- **Mr. Nikhil Dixit ([@nikdixit](https://github.com/nikdixit))**:
  - Developed the Home Page of the Frontend using HTML and Bootstrap CSS Framework.
  - Developed the Frontend of Register and Mark Attendance Pages using HTML and Bootstrap CSS Framework.

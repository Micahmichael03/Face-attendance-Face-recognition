import os.path  # Import os.path module for file and directory operations
import datetime  # Import datetime module to handle date and time
import pickle  # Import pickle module for serializing and deserializing objects
import csv  # Import csv module for CSV file operations

import tkinter as tk  # Import tkinter module for GUI
import cv2  # Import OpenCV module for computer vision tasks
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL for image processing
import face_recognition  # Import face_recognition module for face recognition tasks

import util  # Import custom utility module
# from test import test  # Import test function from test module


class App:
    def __init__(self):
        self.main_window = tk.Tk()  # Create the main window
        self.main_window.geometry("1200x520+350+100")  # Set the size and position of the main window

        # Create and place the login button
        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=200)

        # Create and place the logout button
        self.logout_button_main_window = util.get_button(self.main_window, 'logout', 'red', self.logout)
        self.logout_button_main_window.place(x=750, y=300)

        # Create and place the register new user button
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400) 

        # Create and place the webcam label
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500) # Place the webcam label

        self.add_webcam(self.webcam_label)  # Add webcam to the label

        self.db_dir = './db'  # Set the database directory path
        if not os.path.exists(self.db_dir):  # Check if the database directory exists
            os.mkdir(self.db_dir)  # Create the database directory if it does not exist

        self.log_path = './log.txt'  # Set the log file path
        self.csv_log_path = './log.csv'  # Set the CSV log file path

        # Add header to CSV file if it doesn't exist
        if not os.path.exists(self.csv_log_path):
            with open(self.csv_log_path, 'w', newline='') as csvfile:
                logwriter = csv.writer(csvfile)
                logwriter.writerow(['Name', 'Date', 'Timestamp', 'Action'])  # Write the header

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:  # Check if the webcam capture object is not already created
            self.cap = cv2.VideoCapture(0)  # Create a webcam capture object

        self._label = label  # Set the label to display the webcam feed
        self.process_webcam()  # Start processing the webcam feed

    def process_webcam(self):
        ret, frame = self.cap.read()  # Capture a frame from the webcam

        self.most_recent_capture_arr = frame  # Store the most recent captured frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)  # Convert the frame to RGB
        self.most_recent_capture_pil = Image.fromarray(img_)  # Convert the frame to a PIL image
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)  # Convert the PIL image to an ImageTk object
        self._label.imgtk = imgtk  # Set the ImageTk object to the label
        self._label.configure(image=imgtk)  # Update the label with the new image

        self._label.after(20, self.process_webcam)  # Schedule the next frame capture

    def login(self):
        # Detect all faces in the frame
        face_locations = face_recognition.face_locations(self.most_recent_capture_arr)
        face_encodings = face_recognition.face_encodings(self.most_recent_capture_arr, face_locations)

        # Load all known face encodings from the database
        known_face_encodings = []
        known_face_names = []
        for filename in os.listdir(self.db_dir):
            if filename.endswith(".pickle"):
                name = filename[:-7]  # Remove the '.pickle' extension
                with open(os.path.join(self.db_dir, filename), 'rb') as f:
                    encoding = pickle.load(f)
                    known_face_encodings.append(encoding)
                    known_face_names.append(name)

        # Recognize each face in the frame
        recognized_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "unknown_person"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            recognized_names.append(name)

        # Log the recognized users
        for name in recognized_names:
            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box('Ups...', 'Unknown user detected. Please register new user or try again.')
            else:
                util.msg_box('Welcome back!', 'Welcome, {}.'.format(name))
                with open(self.log_path, 'a') as f:  # Open the log file in append mode
                    f.write('{},{},in\n'.format(name, datetime.datetime.now()))  # Write the login entry to the log file
                with open(self.csv_log_path, 'a', newline='') as csvfile:  # Open the CSV log file in append mode
                    logwriter = csv.writer(csvfile, delimiter=',')
                    # Write the login entry with date and timestamp
                    logwriter.writerow([name, datetime.datetime.now().date(), datetime.datetime.now().time(), 'in'])

    def logout(self):
        # Detect all faces in the frame
        face_locations = face_recognition.face_locations(self.most_recent_capture_arr)
        face_encodings = face_recognition.face_encodings(self.most_recent_capture_arr, face_locations)

        # Load all known face encodings from the database
        known_face_encodings = []
        known_face_names = []
        for filename in os.listdir(self.db_dir):
            if filename.endswith(".pickle"):
                name = filename[:-7]  # Remove the '.pickle' extension
                with open(os.path.join(self.db_dir, filename), 'rb') as f:
                    encoding = pickle.load(f)
                    known_face_encodings.append(encoding)
                    known_face_names.append(name)

        # Recognize each face in the frame
        recognized_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "unknown_person"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            recognized_names.append(name)

        # Log the recognized users
        for name in recognized_names:
            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box('Ups...', 'Unknown user detected. Please register new user or try again.')
            else:
                util.msg_box('Hasta la vista!', 'Goodbye, {}.'.format(name))
                with open(self.log_path, 'a') as f:  # Open the log file in append mode
                    f.write('{},{},out\n'.format(name, datetime.datetime.now()))  # Write the logout entry to the log file
                with open(self.csv_log_path, 'a', newline='') as csvfile:  # Open the CSV log file in append mode
                    logwriter = csv.writer(csvfile, delimiter=',')
                    # Write the logout entry with date and timestamp
                    logwriter.writerow([name, datetime.datetime.now().date(), datetime.datetime.now().time(), 'out'])

    def register_new_user(self):
        # Create a new window for user registration
        self.register_new_user_window = tk.Toplevel(self.main_window)  # Create a new window for user registration
        self.register_new_user_window.geometry("1200x520+370+120")  # Set the size and position of the new window

        # Create and place the accept button
        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        # Create and place the try again button
        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        # Create and place the capture label
        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)  # Add the captured image to the label

        # Create and place the entry text for username
        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        # Create and place the text label for instructions
        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, \ninput username:')
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()  # Destroy the registration window

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)  # Convert the most recent capture to ImageTk
        label.imgtk = imgtk  # Set the ImageTk object to the label
        label.configure(image=imgtk)  # Update the label with the new image

        self.register_new_user_capture = self.most_recent_capture_arr.copy()  # Store the captured frame

    def start(self):
        self.main_window.mainloop()  # Start the main event loop

    def accept_register_new_user(self):
        # Save the captured image to the database
        name = self.entry_text_register_new_user.get(1.0, "end-1c")  # Get the entered username

        # Check if user already exists
        if os.path.exists(os.path.join(self.db_dir, '{}.pickle'.format(name))):
            util.msg_box('Error!', 'User already registered!')
            return

        embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]  # Get face embeddings
        
        # Save the embeddings to a file
        file = open(os.path.join(self.db_dir, '{}.pickle'.format(name)), 'wb')  # Open a file to save embeddings
        pickle.dump(embeddings, file)  # Save the embeddings to the file

        # Save the captured image as PNG
        cv2.imwrite(os.path.join(self.db_dir, '{}.png'.format(name)), self.register_new_user_capture)

        # Show success message
        util.msg_box('Success!', 'User was registered successfully !')  # Show success message
        self.register_new_user_window.destroy()  # Destroy the registration window


if __name__ == "__main__":
    app = App()  # Create an instance of the App class
    app.start()  # Start the application
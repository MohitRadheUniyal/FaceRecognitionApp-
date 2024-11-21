import cv2
import numpy as np
import threading
import subprocess
import sys
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
import os

class FaceRecognitionSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System")
        self.root.geometry("1366x768+0+0")

        # Setup UI
        self.setup_ui()

        # Flag to signal when to stop the face recognition thread
        self.running = True
        self.video_cap = None
        self.face_thread = threading.Thread(target=self.face_rec)
        self.face_thread.daemon = True
        self.face_thread.start()

        # Bind the window close event to clean up OpenCV resources
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        """Setup UI components like header, background, etc."""
        header_bg = Label(self.root, bg="#00264d")
        header_bg.place(x=0, y=0, width=1366, height=130)

        # Logo
        img_path = r"Images\logo.png"
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((130, 130), Image.LANCZOS)
            self.photoimg = ImageTk.PhotoImage(img)
            logo_lbl = Label(self.root, image=self.photoimg, bg="#00264d")
            logo_lbl.place(x=0, y=0, width=130, height=130)
        else:
            messagebox.showerror("Error", "Logo image not found.")

        # Title Label
        title_lbl = Label(
            self.root,
            text="Government Polytechnic Narendra Nagar\nFace Recognition Attendance System",
            font=("Arial", 22, "bold"),
            bg="#00264d", fg="white", anchor="center"
        )
        title_lbl.place(x=160, y=40, width=1000, height=60)

        # Background
        bg_img_path = r"Images\background.jpg"
        if os.path.exists(bg_img_path):
            bg_img = Image.open(bg_img_path)
            bg_img = bg_img.resize((1366, 638), Image.LANCZOS)
            self.bg_photoimg = ImageTk.PhotoImage(bg_img)
            bg_lbl = Label(self.root, image=self.bg_photoimg)
            bg_lbl.place(x=0, y=132, width=1366, height=638)
        else:
            messagebox.showerror("Error", "Background image not found.")

    def draw_boundary(self, img, classifier, scaleFactor, minNeighbors, color, clf):
        """Detect faces and match with the stored classifier."""
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
        cord = []

        for (x, y, w, h) in features:
            id, predict = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int(100 * (1 - predict / 300))

            # Connect to the database
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="attendance_system")
            cursor = conn.cursor()

            if confidence > 50:
                cursor.execute("SELECT name, roll_no, department, year, semester FROM students WHERE id = %s", (id,))
                result = cursor.fetchone()

                if result:
                    name, roll_no, department, year, semester = result
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(img, f"Name: {name}", (x, y - 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.putText(img, f"Roll No: {roll_no}", (x, y - 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.putText(img, f"Department: {department}", (x, y - 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.putText(img, f"Year: {year}", (x, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.putText(img, f"Semester: {semester}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                    # Mark attendance if recognized
                    self.mark_attendance(name, roll_no, department, year, semester)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(img, "Unknown Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 3)

            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(img, "Unknown Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 3)

            cursor.close()
            conn.close()  # Close the connection after each iteration
            cord = [x, y, w, h]
        return cord

    def recognize(self, img, clf, faceCascade):
        """Perform face recognition on the image."""
        cord = self.draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), clf)
        return img
    
    def mark_attendance(self, name, roll_no, department, year, semester):
        """Mark attendance in the CSV file."""
        with open("attendance.csv", "a+", newline="\n") as f:
            f.seek(0)
            myDataList = f.readlines()
            today = datetime.now().strftime("%d/%m/%y")
            entry_exists = any(name in line and today in line for line in myDataList)

            if not entry_exists:
                now = datetime.now()
                dtstring = now.strftime("%H:%M:%S")
                f.writelines(f"\n{name},{roll_no},{department},{year},{semester},{dtstring},{today},Present")

    def face_rec(self):
        """Start the face recognition process and capture the video feed."""
        if not os.path.exists("haarcascade_frontalface_default.xml") or not os.path.exists("classifier.xml"):
            messagebox.showerror("Error", "Model files not found.")
            return

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        self.video_cap = cv2.VideoCapture(0)

        if not self.video_cap.isOpened():
            messagebox.showerror("Error", "Could not access the camera.")
            return

        while self.running:
            ret, img = self.video_cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            img = self.recognize(img, clf, faceCascade)
            cv2.imshow("Face Recognition", img)

            if cv2.waitKey(1) == 13:  # Enter key to exit loop
                break

        self.video_cap.release()
        cv2.destroyAllWindows()

    def on_close(self):
        """Clean up when the window is closed."""
        self.running = False
        self.face_thread.join()  # Ensure thread finishes before quitting

        # Release video capture and close OpenCV windows
        if self.video_cap is not None:
            self.video_cap.release()
        cv2.destroyAllWindows()

        # Quit the Tkinter mainloop
        self.root.quit()

        # Redirect to main.py after closing the face recognition window
        subprocess.Popen([sys.executable, "main.py"])

# Main function to run the system
if __name__ == "__main__":
    root = Tk()
    obj = FaceRecognitionSystem(root)
    root.mainloop()

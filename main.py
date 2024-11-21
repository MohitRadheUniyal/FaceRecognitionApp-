from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
from student import Student
from train import Train
from face_recognition import FaceRecognitionSystem
from attendance import Attendance
class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System")
        self.root.geometry("1366x768+0+0")

        # =============== Header with Modern Professional Look =======================
        
        # Gradient header background with two colors
        header_bg = Label(self.root, bg="#00264d")  # Dark navy color for modern look
        header_bg.place(x=0, y=0, width=1366, height=130)

        # Logo - smaller and better positioned for balance
        img = Image.open(r"Images\logo.png")
        img = img.resize((130, 130), Image.LANCZOS)  # Smaller, sleek logo
        self.photoimg = ImageTk.PhotoImage(img)
        logo_lbl = Label(self.root, image=self.photoimg, bg="#00264d")
        logo_lbl.place(x=0, y=0, width=130, height=130)

        # Title - centered with a single-line heading
        title_lbl = Label(
            self.root, 
            text="Government Polytechnic Narendra Nagar\nFace Recognition Attendance System", 
            font=("Arial", 22, "bold"),  # Simple, professional font
            bg="#00264d", 
            fg="white",
            anchor="center"
        )
        title_lbl.place(x=160, y=40, width=1000, height=60)  # Center-aligned, slightly below the logo

        # Subtle bottom line to separate the header
        header_line = Frame(self.root, bg="#00b3b3", height=2)  # Thin aqua line for accent
        header_line.place(x=0, y=130, width=1366)

        # Background image aligned to fit screen space
        bg_img = Image.open(r"Images\background.jpg")
        bg_img = bg_img.resize((1366, 638), Image.LANCZOS)  # Adjusted for below-header layout
        self.bg_photoimg = ImageTk.PhotoImage(bg_img)
        bg_lbl = Label(self.root, image=self.bg_photoimg)
        bg_lbl.place(x=0, y=132, width=1366, height=638)  # Positioned below the header line
        
        # Adjust button positions to fit a 3x2 grid layout
        # Student button
        std_img_btn = Image.open(r"Images\student.jpg")
        std_img_btn = std_img_btn.resize((400, 220), Image.LANCZOS)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(self.root, command=self.student_pannels, image=self.std_img1, cursor="hand2")  # Use self.root as the master
        std_b1.place(x=20, y=150, width=400, height=210)

        std_b1_1 = Button(self.root, command=self.student_pannels, text="Student Panel", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")  # Use self.root as the master
        std_b1_1.place(x=20, y=360, width=400, height=45) 
        
        # Detect Face button 2
        det_img_btn = Image.open(r"Images\Face.jpg")
        det_img_btn = det_img_btn.resize((400, 220), Image.LANCZOS)
        self.det_img1 = ImageTk.PhotoImage(det_img_btn)

        det_b1 = Button(self.root, command=self.face_rec, image=self.det_img1, cursor="hand2")  # Use self.root as the master
        det_b1.place(x=460, y=150, width=400, height=210)

        det_b1_1 = Button(self.root, command=self.face_rec, text="Face Detector", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")  # Use self.root as the master
        det_b1_1.place(x=460, y=360, width=400, height=45)

        # Attendance System button 3
        att_img_btn = Image.open(r"Images\traindata.jpg")
        att_img_btn = att_img_btn.resize((400, 220), Image.LANCZOS)
        self.att_img1 = ImageTk.PhotoImage(att_img_btn)

        att_b1 = Button(self.root, command=self.attendance_pannel, image=self.att_img1, cursor="hand2")  # Use self.root as the master
        att_b1.place(x=900, y=150, width=400, height=210)

        att_b1_1 = Button(self.root, command=self.attendance_pannel, text="Attendance", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")  # Use self.root as the master
        att_b1_1.place(x=900, y=360, width=400, height=45)
        
        # Train button 5
        tra_img_btn = Image.open(r"Images\train.gif")
        tra_img_btn = tra_img_btn.resize((400, 220), Image.LANCZOS)
        self.tra_img1 = ImageTk.PhotoImage(tra_img_btn)

        tra_b1 = Button(self.root, command=self.train_pannels, image=self.tra_img1, cursor="hand2")  # Use self.root as the master
        tra_b1.place(x=20, y=430, width=400, height=210)

        tra_b1_1 = Button(self.root, command=self.train_pannels, text="Data Train", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")  # Use self.root as the master
        tra_b1_1.place(x=20, y=640, width=400, height=45)

        # Photo button 6
        pho_img_btn = Image.open(r"Images\camera.jpg")
        pho_img_btn = pho_img_btn.resize((400, 220), Image.LANCZOS)
        self.pho_img1 = ImageTk.PhotoImage(pho_img_btn)

        pho_b1 = Button(self.root, command=self.open_img, image=self.pho_img1, cursor="hand2")  # Use self.root as the master
        pho_b1.place(x=460, y=430, width=400, height=210)

        pho_b1_1 = Button(self.root, command=self.open_img, text="Photos", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")  # Use self.root as the master
        pho_b1_1.place(x=460, y=640, width=400, height=45)
        
        # Exit button 8
        exi_img_btn = Image.open(r"Images\exit.jpg")
        exi_img_btn = exi_img_btn.resize((400, 210), Image.LANCZOS)
        self.exi_img1 = ImageTk.PhotoImage(exi_img_btn)

        exi_b1 = Button(self.root, command=self.Close, image=self.exi_img1, cursor="hand2")  # Use self.root as the master
        exi_b1.place(x=900, y=430, width=400, height=220)

        exi_b1_1 = Button(self.root, command=self.Close, text="Exit", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")  # Use self.root as the master
        exi_b1_1.place(x=900, y=640, width=400, height=45)

    # Placeholder methods
    def student_pannels(self):
        print("Student Panel clicked")
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)

    def face_rec(self):
         self.new_window=Toplevel(self.root)
         self.app=FaceRecognitionSystem(self.new_window)
         print("Face Detection clicked")
       
    def attendance_pannel(self):
         self.new_window=Toplevel(self.root)
         self.app=Attendance(self.new_window)
         print("Attendance Panel clicked")

    def train_pannels(self):
        self.new_window=Toplevel(self.root)
        self.app=Train(self.new_window)
        print("Train Data clicked")

    def open_img(self):
         os.startfile("data")
         print("Open Image clicked")
        

    def Close(self):
        print("Exit clicked")
        self.root.quit()

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()

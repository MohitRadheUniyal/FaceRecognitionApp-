from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import cv2

class Student:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System")
        self.root.geometry("1366x768+0+0")
        
        # Header and Logo
        header_bg = Label(self.root, bg="#00264d")
        header_bg.place(x=0, y=0, width=1366, height=130)

        img = Image.open(r"Images\logo.png")
        img = img.resize((130, 130), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        logo_lbl = Label(self.root, image=self.photoimg, bg="#00264d")
        logo_lbl.place(x=0, y=0, width=130, height=130)

        title_lbl = Label(
            self.root, 
            text="Government Polytechnic Narendra Nagar\nFace Recognition Attendance System", 
            font=("Arial", 22, "bold"), 
            bg="#00264d", 
            fg="white",
            anchor="center"
        )
        title_lbl.place(x=160, y=40, width=1000, height=60)

        header_line = Frame(self.root, bg="#00b3b3", height=2)
        header_line.place(x=0, y=130, width=1366)

        bg_img = Image.open(r"Images\background.jpg")
        bg_img = bg_img.resize((1366, 638), Image.LANCZOS)
        self.bg_photoimg = ImageTk.PhotoImage(bg_img)
        bg_lbl = Label(self.root, image=self.bg_photoimg)
        bg_lbl.place(x=0, y=132, width=1366, height=638)
        
        # Variables
        self.var_std_name = StringVar()
        self.var_roll = StringVar()
        self.var_dob = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_department = StringVar()
        self.var_radio1 = StringVar()

        # Main frame
        main_frame = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        main_frame.place(x=0, y=135, width=1366, height=555)

        # Left Frame (Student Registration Form)
        left_frame = LabelFrame(main_frame, bd=4, relief=RIDGE, bg="white", 
                                text="STUDENT REGISTER HERE", font=("times new roman", 12, "bold"))
        left_frame.place(x=10, y=10, width=683, height=540)
        
        # Course Info Frame
        course_info_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, 
                                       text="Current Course Information", font=("verdana", 12, "bold"), fg="navyblue")
        course_info_frame.place(x=10, y=5, width=660, height=140)
        
        year_label = Label(course_info_frame, text="Year", font=("verdana", 12, "bold"), bg="white", fg="navyblue")
        year_label.grid(row=0, column=0, padx=5, pady=10, sticky=W)
        year_combo = ttk.Combobox(course_info_frame, textvariable=self.var_year, width=15, font=("verdana", 12), state="readonly")
        year_combo["values"] = ("Select Year", "1st ", "2nd ", "3rd ")
        year_combo.current(0)
        year_combo.grid(row=0, column=1, padx=5, pady=10, sticky=W)

        semester_label = Label(course_info_frame, text="Semester", font=("verdana", 12, "bold"), bg="white", fg="navyblue")
        semester_label.grid(row=0, column=2, padx=5, pady=10, sticky=W)
        semester_combo = ttk.Combobox(course_info_frame, textvariable=self.var_semester, width=15, font=("verdana", 12), state="readonly")
        semester_combo["values"] = ("Select Semester", "1", "2", "3", "4", "5", "6")
        semester_combo.current(0)
        semester_combo.grid(row=0, column=3, padx=5, pady=10, sticky=W)

        dep_label = Label(course_info_frame, text="Department", font=("verdana", 12, "bold"), bg="white", fg="navyblue")
        dep_label.grid(row=1, column=0, padx=5, pady=10, sticky=W)
        department_combo = ttk.Combobox(course_info_frame, textvariable=self.var_department, width=15, font=("verdana", 12), state="readonly")
        department_combo["values"] = ("Select Department", "IT", "Civil", "Mechanical", "Gaming & Animation", "Electrical", "Electronics", "Pharmacy")
        department_combo.current(0)
        department_combo.grid(row=1, column=1, padx=5, pady=10, sticky=W)

        # Class Info Frame
        class_info_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, 
                                      text="Class Student Information", font=("verdana", 12, "bold"), fg="navyblue")
        class_info_frame.place(x=10, y=145, width=660, height=300)

        student_name_label = Label(class_info_frame, text="Student Name:", font=("verdana", 12, "bold"), 
                                   fg="navyblue", bg="white")
        student_name_label.grid(row=0, column=0, padx=5, pady=5, sticky=W,)
        student_name_entry = ttk.Entry(class_info_frame, textvariable=self.var_std_name, width=15, font=("verdana", 12))
        student_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        
        student_roll_label = Label(class_info_frame, text="Roll No:", font=("verdana", 12, "bold"), 
                                   fg="navyblue", bg="white")
        student_roll_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        student_roll_entry = ttk.Entry(class_info_frame, textvariable=self.var_roll, width=15, font=("verdana", 12))
        student_roll_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        student_dob_label = Label(class_info_frame, text="DOB:", font=("verdana", 12, "bold"), fg="navyblue", bg="white")
        student_dob_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        student_dob_entry = ttk.Entry(class_info_frame, textvariable=self.var_dob, width=15, font=("verdana", 12))
        student_dob_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        take_photo_radiobtn = ttk.Radiobutton(class_info_frame, text="Take Photo Sample", variable=self.var_radio1, value="Yes")
        take_photo_radiobtn.grid(row=4, column=0, padx=5, pady=10, sticky=W)
        no_photo_radiobtn = ttk.Radiobutton(class_info_frame, text="No Photo Sample", variable=self.var_radio1, value="No")
        no_photo_radiobtn.grid(row=5, column=0, padx=5, pady=10, sticky=W)

        # Button Frame
        btn_frame = Frame(left_frame, bd=2, bg="white", relief=RIDGE)
        btn_frame.place(x=10, y=420, width=660, height=90)
        
        save_btn = Button(btn_frame, command=self.generate_dataset, text="Save", width=18, font=("verdana", 12, "bold"), fg="white", bg="navyblue")
        save_btn.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        update_btn = Button(btn_frame, text="Update", width=18, font=("verdana", 12, "bold"), fg="white", bg="navyblue", command=self.update_data)
        update_btn.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        
        del_btn = Button(btn_frame, text="Delete", width=18, font=("verdana", 12, "bold"), fg="white", bg="navyblue", command=self.delete_data)
        del_btn.grid(row=0, column=2, padx=5, pady=5, sticky=W)

        res_btn = Button(btn_frame, text="Reset", width=18, font=("verdana", 12, "bold"), fg="white", bg="navyblue", command=self.clear_fields)
        res_btn.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        
        take_photo_btn = Button(btn_frame, command=self.photo_sample, text="Take Photo", width=18, font=("verdana", 12, "bold"), fg="white", bg="navyblue")
        take_photo_btn.grid(row=1, column=1, padx=5, pady=5, sticky=W)
        
        update_photo_btn = Button(btn_frame, text="Update a photo", width=18, font=("verdana", 12, "bold"), fg="white", bg="navyblue")
        update_photo_btn.grid(row=1, column=2, padx=5, pady=5, sticky=W)
        
          # Right Frame (Student Data Display)
        right_frame = LabelFrame(main_frame, bd=4, relief=RIDGE, bg="white", 
                                 text="STUDENT DATA", font=("times new roman", 12, "bold"))
        right_frame.place(x=703, y=10, width=650, height=540)

        # Table for displaying student data
        tree_frame = Frame(right_frame)
        tree_frame.pack(fill=BOTH, expand=True)

        self.scroll_y = Scrollbar(tree_frame, orient=VERTICAL)
        self.scroll_y.pack(side=RIGHT, fill=Y)

        self.scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)
        self.scroll_x.pack(side=BOTTOM, fill=X)

        self.student_table = ttk.Treeview(tree_frame, columns=("id", "name", "roll_no", "dob", "year", "semester", "department"),
                                          xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.scroll_x.config(command=self.student_table.xview)
        self.scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("id", text="ID")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("roll_no", text="Roll No")
        self.student_table.heading("dob", text="DOB")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("semester", text="Semester")
        self.student_table.heading("department", text="Department")
        self.student_table["show"] = "headings"
        
        self.student_table.pack(fill=BOTH, expand=True)

        # Call fetch_data on startup
        self.fetch_data()


    def generate_dataset(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="attendance_system")
            cursor = conn.cursor()

            data = (
                self.var_std_name.get(),
                self.var_roll.get(),
                self.var_dob.get(),
                self.var_year.get(),
                self.var_semester.get(),
                self.var_department.get()
            )
            cursor.execute("INSERT INTO students (name, roll_no, dob, year, semester, department) VALUES (%s, %s, %s, %s, %s, %s)", data)
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Student data saved successfully!")
            self.clear_fields()
            self.fetch_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="attendance_system")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        if rows:
            for item in self.student_table.get_children():
                self.student_table.delete(item)
            for row in rows:
                self.student_table.insert("", END, values=row)
        conn.close()

    def update_data(self):
        try:
            selected_item = self.student_table.selection()
            if not selected_item:
                messagebox.showerror("Select", "Please select a student to update")
                return
            
            student_id = self.student_table.item(selected_item)["values"][0]
            name = self.var_std_name.get()
            roll = self.var_roll.get()
            dob = self.var_dob.get()
            year = self.var_year.get()
            semester = self.var_semester.get()
            department = self.var_department.get()

            conn = mysql.connector.connect(host="localhost", user="root", password="", database="attendance_system")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE students
                SET name = %s, roll_no = %s, dob = %s, year = %s, semester = %s, department = %s
                WHERE id = %s
            """, (name, roll, dob, year, semester, department, student_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Student data updated successfully!")
            self.fetch_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def delete_data(self):
        try:
            selected_item = self.student_table.selection()
            if not selected_item:
                messagebox.showerror("Select", "Please select a student to delete")
                return
            
            student_id = self.student_table.item(selected_item)["values"][0]
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="attendance_system")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Student data deleted successfully!")
            self.fetch_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def clear_fields(self):
        self.var_std_name.set("")
        self.var_roll.set("")
        self.var_dob.set("")
        self.var_year.set("")
        self.var_semester.set("")
        self.var_department.set("")
        self.var_radio1.set("")

    def select_student(self, event):
        selected_item = self.student_table.selection()
        if selected_item:
            student_data = self.student_table.item(selected_item)["values"]
            self.var_std_name.set(student_data[1])
            self.var_roll.set(student_data[2])
            self.var_dob.set(student_data[3])
            self.var_year.set(student_data[4])
            self.var_semester.set(student_data[5])
            self.var_department.set(student_data[6])
            
        # ===================take a photo sample===============
    def photo_sample(self):
        try:
            selected_item = self.student_table.selection()
            if not selected_item:
                messagebox.showerror("Select", "Please select a student to take a photo")
                return

            student_id = self.student_table.item(selected_item)["values"][0]

            conn = mysql.connector.connect(host="localhost", user="root", password="", database="attendance_system")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            result = cursor.fetchall()
            conn.close()

            id = len(result) + 1  # Assign a unique id based on the number of entries

            face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            
            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    return img[y:y+h, x:x+w]
                return None
            
            cap = cv2.VideoCapture(0)
            img_id = 0
            
            while True:
                ret, my_frame = cap.read()
                if not ret:
                    break
                cropped_face = face_cropped(my_frame)
                if cropped_face is not None:
                    img_id += 1
                    face = cv2.resize(cropped_face, (450, 450))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    file_name_path = f"data/user.{id}.{img_id}.jpg"
                    cv2.imwrite(file_name_path, face)
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                    cv2.imshow("Cropped Face", face)

                if cv2.waitKey(1) == 13 or img_id == 100:
                    break

            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Result", "Generating dataset completed!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

                
if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()

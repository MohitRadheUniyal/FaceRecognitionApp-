import csv
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
import os

class Attendance:
    def __init__(self, root):
        # Initialize the root window and set its properties
        self.root = root
        self.root.title("Face Recognition System")
        self.root.geometry("1366x768+0+0")
        
        # Create header and logo for the application
        header_bg = Label(self.root, bg="#00264d")
        header_bg.place(x=0, y=0, width=1366, height=130)

        # Load the logo image and resize it
        img = Image.open(r"Images\logo.png")
        img = img.resize((130, 130), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        logo_lbl = Label(self.root, image=self.photoimg, bg="#00264d")
        logo_lbl.place(x=0, y=0, width=130, height=130)

        # Title label for the window
        title_lbl = Label(
            self.root, 
            text="Government Polytechnic Narendra Nagar\nFace Recognition Attendance System", 
            font=("Arial", 22, "bold"), 
            bg="#00264d", 
            fg="white",
            anchor="center"
        )
        title_lbl.place(x=160, y=40, width=1000, height=60)

        # Header line below the title
        header_line = Frame(self.root, bg="#00b3b3", height=2)
        header_line.place(x=0, y=130, width=1366)

        # Set background image for the main window
        bg_img = Image.open(r"Images\background.jpg")
        bg_img = bg_img.resize((1366, 638), Image.LANCZOS)
        self.bg_photoimg = ImageTk.PhotoImage(bg_img)
        bg_lbl = Label(self.root, image=self.bg_photoimg)
        bg_lbl.place(x=0, y=132, width=1366, height=638)
        
        # Create the main frame to hold the table
        main_frame = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        main_frame.place(x=0, y=135, width=1366, height=520)
        
        # Create a frame to hold the treeview (table) for displaying attendance data
        tree_frame = Frame(main_frame)
        tree_frame.pack(fill=BOTH, expand=True)

        # Add vertical scrollbar to the treeview
        self.scroll_y = Scrollbar(tree_frame, orient=VERTICAL)
        self.scroll_y.pack(side=RIGHT, fill=Y)

        # Add horizontal scrollbar to the treeview
        self.scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)
        self.scroll_x.pack(side=BOTTOM, fill=X)

        # Create a treeview table for displaying student attendance data
        self.student_table = ttk.Treeview(tree_frame, columns=("name", "roll_no", "department", "year", "semester", "time", "date", "status"),
                                          xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.scroll_x.config(command=self.student_table.xview)
        self.scroll_y.config(command=self.student_table.yview)

        # Define headings for each column in the treeview
        self.student_table.heading("name", text="Name")
        self.student_table.heading("roll_no", text="Roll No")
        self.student_table.heading("department", text="Department")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("semester", text="Semester")
        self.student_table.heading("time", text="Time")
        self.student_table.heading("date", text="Date")
        self.student_table.heading("status", text="Status")
        
        # Configure the treeview to show only the headers and no borders around data
        self.student_table["show"] = "headings"
        
        # Add the treeview widget to the window
        self.student_table.pack(fill=BOTH, expand=True)

        # Fetch the existing attendance data on startup
        self.fetch_data()

        # Button for downloading the data as a CSV file
        download_btn = Button(self.root, text="Download", command=self.download_csv, font=("Arial", 14, "bold"), bg="#00b3b3", fg="white")
        download_btn.place(x=0, y=650, width=1366, height=40)

    def fetch_data(self):
        # Clear the existing data from the treeview table
        for item in self.student_table.get_children():
            self.student_table.delete(item)
        
        # Read attendance data from the CSV file and insert it into the treeview
        try:
            with open("attendance.csv", mode="r") as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    self.student_table.insert("", END, values=row)
        except FileNotFoundError:
            messagebox.showerror("Error", "Attendance CSV file not found.")  # Show an error if the CSV file is missing
        
    def download_csv(self):
        # Generate a unique file name for the CSV file using the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        directory = r"C:\Users\mohit\Desktop"  # Directory where the CSV will be saved (modify as needed)
        filename = os.path.join(directory, f"attendance_{timestamp}.csv")
        
        # Ensure the directory exists before saving the file
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Save the data from the table into a new CSV file
        try:
            with open(filename, mode="w", newline="") as file:
                csvwriter = csv.writer(file)
                # Write the header row to the CSV file
                csvwriter.writerow(["Name", "Roll No", "Department", "Year", "Semester", "Time", "Date", "Status"])
                
                # Write the attendance data rows to the CSV file
                for row in self.student_table.get_children():
                    data = self.student_table.item(row)['values']
                    
                    # Ensure there are 8 elements in the row to prevent index errors
                    if len(data) == 8:
                        formatted_data = [
                            data[0],  # Name
                            f"'{data[1]}",  # Roll No (added single quote for Excel formatting)
                            data[2],  # Department
                            data[3],  # Year
                            data[4],  # Semester
                            self.format_time(data[5]),  # Format the time column
                            self.format_date(data[6]),  # Format the date column
                            data[7]   # Status
                        ]
                        csvwriter.writerow(formatted_data)
                    else:
                        # Log or handle rows that don't follow the expected structure
                        print(f"Skipping row with unexpected structure: {data}")
            
            messagebox.showinfo("Success", f"CSV file downloaded successfully as {filename}.")  # Success message
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while downloading the file: {str(e)}")  # Handle errors during CSV writing

    def format_time(self, time):
        # Format time as a string (if not already) using a specific format
        return str(time) if isinstance(time, str) else datetime.strptime(str(time), "%H:%M:%S").strftime("%H:%M:%S")

    def format_date(self, date):
        # Format date as a string (if not already) using a specific format
        return str(date) if isinstance(date, str) else datetime.strptime(str(date), "%Y-%m-%d").strftime("%B %d, %Y")

if __name__ == "__main__":
    # Initialize the Tkinter root window and start the Attendance system
    root = Tk()
    obj = Attendance(root)
    root.mainloop()
 
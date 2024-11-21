import os
import numpy as np
import cv2
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

class Train:
    def __init__(self, root):
        # Initialize the root window and set its properties
        self.root = root
        self.root.title("Face Recognition System")
        self.root.geometry("1366x768+0+0")

        # Create a header and logo
        header_bg = Label(self.root, bg="#00264d")
        header_bg.place(x=0, y=0, width=1366, height=130)

        img_path = r"Images\logo.png"
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((130, 130), Image.LANCZOS)  # Resize logo
            self.photoimg = ImageTk.PhotoImage(img)
            logo_lbl = Label(self.root, image=self.photoimg, bg="#00264d")
            logo_lbl.place(x=0, y=0, width=130, height=130)
        else:
            messagebox.showerror("Error", "Logo image not found.")  # Error if logo is missing

        # Title of the application
        title_lbl = Label(
            self.root, 
            text="Government Polytechnic Narendra Nagar\nFace Recognition Attendance System", 
            font=("Arial", 22, "bold"), 
            bg="#00264d", 
            fg="white",
            anchor="center"
        )
        title_lbl.place(x=160, y=40, width=1000, height=60)

        # Create a horizontal line below the header
        header_line = Frame(self.root, bg="#00b3b3", height=2)
        header_line.place(x=0, y=130, width=1366)

        # Set the background image
        bg_img_path = r"Images\background.jpg"
        if os.path.exists(bg_img_path):
            bg_img = Image.open(bg_img_path)
            bg_img = bg_img.resize((1366, 638), Image.LANCZOS)
            self.bg_photoimg = ImageTk.PhotoImage(bg_img)
            bg_lbl = Label(self.root, image=self.bg_photoimg)
            bg_lbl.place(x=0, y=132, width=1366, height=638)
        else:
            messagebox.showerror("Error", "Background image not found.")  # Error if background image is missing

        # Hide the main window during training process
        self.root.withdraw()

        # Start the training process automatically when the app starts
        self.train_classifier()

    def train_classifier(self):
        # Create a new window for displaying images during training
        train_window = Toplevel(self.root)
        train_window.title("Training Images")
        train_window.geometry("1366x768")  # Full window size
        
        # Label for displaying training progress
        image_label = Label(train_window, text="Training Images", font=("Arial", 20), bg="white", fg="black")
        image_label.pack(pady=10)

        # Label to display images in the new window
        display_label = Label(train_window, bg="white")
        display_label.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # Path to the directory containing training data
        data_dir = "data"
        faces = []  # List to store face images
        ids = []    # List to store IDs corresponding to each face
        current_id = 1  # Start from ID 1

        # Check if the training data directory exists
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", f"Directory '{data_dir}' does not exist.")  # Error if directory is missing
            self.root.deiconify()  # Show the main window if training fails
            train_window.destroy()
            return

        # List all images in the directory with .jpg extension
        image_files = [f for f in os.listdir(data_dir) if f.endswith(".jpg")]
        total_images = len(image_files)

        # Check if there are any images to process
        if total_images == 0:
            messagebox.showerror("Error", "No images found in the 'data' directory for training.")  # Error if no images
            self.root.deiconify()  # Show the main window if training fails
            train_window.destroy()
            return

        processed_images = 0

        # Loop through all the image files in the directory
        for filename in image_files:
            image_path = os.path.join(data_dir, filename)

            try:
                # Assign sequential IDs starting from 1
                id = current_id
                current_id += 1

                # Open the image and convert it to grayscale
                img = Image.open(image_path).convert('L')  # Convert to grayscale
                image_np = np.array(img, 'uint8')
                faces.append(image_np)
                ids.append(id)

                # Convert the image to a format suitable for Tkinter display
                img_tk = ImageTk.PhotoImage(image=Image.fromarray(image_np))
                display_label.configure(image=img_tk)
                display_label.image = img_tk  # Keep a reference to the image object

                processed_images += 1
                progress_text = f"Processing {processed_images}/{total_images} images"
                image_label.config(text=progress_text)  # Update progress label

                # Update the window to show the new image and progress
                train_window.update_idletasks()
                train_window.update()

            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                continue

        # If no valid faces were collected, show an error message
        if len(faces) == 0:
            messagebox.showerror("Error", "No valid images found for training.")
            self.root.deiconify()
            train_window.destroy()
            return

        # Train the classifier using OpenCV
        try:
            clf = cv2.face.LBPHFaceRecognizer_create()  # Create a Local Binary Pattern Histogram (LBPH) recognizer
            clf.train(faces, np.array(ids))  # Train the classifier with the collected faces and IDs

            # Save the trained classifier to a file
            classifier_path = "classifier.xml"
            clf.write(classifier_path)
            print(f"Training completed and saved to {classifier_path}")

            # Show success message
            messagebox.showinfo("Result",f"Training datasets completed successfully!\nModel saved as {classifier_path}")
        
        except Exception as e:
            messagebox.showerror("Training Error", f"Error training the classifier: {e}")
            print(f"Error training the classifier: {e}")

        # Close the training window after training is complete
        train_window.destroy()

        # Return to the main window (if desired)
        # self.root.deiconify()  # Make the main window visible again
        # messagebox.showinfo("Return to Main","Return to the main window.")  # Inform the user

if __name__ == "__main__":
    # Create the main application window and start the program
    root = Tk()
    obj = Train(root)
    root.mainloop()

import tkinter as tk  # Provides a Python interface to the Tk GUI toolkit.
from tkinter import *  # Imports all classes, functions, and constants from tkinter module.
from tkinter import ttk, font  # Additional widgets and font handling utilities for Tkinter.
from tkinter import filedialog  # Dialogs for file and directory selection.
from flask import Flask  # Web framework for creating web applications in Python.
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy integration for Flask web applications.
from sqlalchemy import create_engine, extract, desc  # SQL toolkit and Object-Relational Mapper (ORM) for Python.
from sqlalchemy.exc import OperationalError  # Exceptions related to database operations in SQLAlchemy.
from flask_bcrypt import Bcrypt  # Password hashing utilities for Flask web applications.
from PIL import ImageTk, Image  # Python Imaging Library for image manipulation.
import os  # Provides functions to interact with the operating system.
import pandas as pd  # Data manipulation and analysis library.
import tkinter.font as tkFont  # Additional font utilities for Tkinter.
from datetime import datetime, timedelta, timezone  # Date and time utilities.
from dateutil.relativedelta import relativedelta
import re  # Regular expression operations.
import numpy as np  # Numerical computing library for arrays, matrices, and mathematical functions.
from tkcalendar import *  # Calendar widget for Tkinter.
import sys 



print("Python Version: 3.12.0")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

app = Flask(__name__) # Create the Flask application instance

basedir = os.path.abspath(os.path.dirname(__file__)) # Get the absolute path of the current directory

db_path = os.path.join(basedir, resource_path('autorepair.db')) # Construct the path to the database file

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}' # Configure the SQLAlchemy database URI to connect to the SQLite database file

bcrypt = Bcrypt(app) # Initialize Bcrypt extension with the Flask application instance
db = SQLAlchemy(app) # Initialize SQLAlchemy extension with the Flask application instance

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drop_off_date = db.Column(db.String(50), nullable=False)
    check_up_date = db.Column(db.String(50), nullable=False)
    next_check_up = db.Column(db.String(15), nullable=False)
    vehicle_id = db.Column(db.String(50), nullable=False)
    mileage= db.Column(db.String(50), nullable=False)
    service_cost = db.Column(db.Integer, nullable=False)
    service_description = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    tax_number = db.Column(db.String(20), nullable=False)
    billing_address = db.Column(db.String(200), nullable=False)
    paid = db.Column(db.String(50), nullable=False)
    upload_photo = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    photos = db.Column(db.String(300), nullable=True)
    service_state = db.Column(db.String(15), default="In progress")
    date_confirm_completed_service = db.Column(db.String(15), default="Not Completed")
    code_confirm_completed_service = db.Column(db.String(20), default="Employee Code")
    date_cancel_service = db.Column(db.String(15), default="Not Cancelled")
    code_cancel_service = db.Column(db.String(20), default="Employee Code")
    last_update = db.Column(db.String(15), default="No Previous Update")
    code_last_update = db.Column(db.String(20), default="Employee Code")
    insertion_date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    code_insertion = db.Column(db.String(20), default="Employee Code")

    def __init__(self, drop_off_date, check_up_date, next_check_up, vehicle_id, mileage, service_cost, service_description, full_name, phone_number, 
                email, tax_number, billing_address, paid, upload_photo, payment_method, photos,  **kwargs):
        self.drop_off_date = drop_off_date
        self.check_up_date = check_up_date
        self.next_check_up = next_check_up
        self.vehicle_id = vehicle_id
        self.mileage = mileage
        self.service_cost = service_cost
        self.service_description = service_description
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.tax_number = tax_number
        self.billing_address = billing_address
        self.paid = paid
        self.upload_photo = upload_photo
        self.payment_method = payment_method
        self.photos = photos
        super().__init__(**kwargs)

    def __repr__(self):
        return f"Service(id={self.id}, Full Name={self.full_name}, Tax Number={self.tax_number}, Vehicle={self.vehicle_id})"

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_cost = db.Column(db.Integer, nullable=False)
    service_description = db.Column(db.String(200), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    paid = db.Column(db.String(50),  nullable=False)
    upload_photo = db.Column(db.String(50),  nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(50),  nullable=False)
    tax_number = db.Column(db.String(50), nullable=False)
    billing_address = db.Column(db.String(50), nullable=False)
    vehicle_id = db.Column(db.String(20), nullable=False)
    photos = db.Column(db.String(300), nullable=False)
    last_update = db.Column(db.String(15), default="No previous update")
    code_last_update = db.Column(db.String(20), default="Employee Code")
    insertion_date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    code_insertion = db.Column(db.String(20), default="Employee Code")

    def __init__(self, service_cost, service_description, payment_method, paid, upload_photo, full_name, phone_number, tax_number, billing_address, vehicle_id, photos, **kwargs):
        self.service_cost = service_cost
        self.service_description = service_description
        self.payment_method = payment_method
        self.paid = paid
        self.upload_photo = upload_photo
        self.full_name = full_name
        self.phone_number = phone_number
        self.tax_number = tax_number
        self.billing_address = billing_address
        self.vehicle_id = vehicle_id
        self.photos = photos
        super().__init__(**kwargs)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    employee_code = db.Column(db.String(30), unique=True, nullable=False)
    employee_type = db.Column(db.String(30), nullable=False)

    def __init__(self, full_name, username, password, employee_code, employee_type,  **kwargs):
        self.full_name = full_name
        self.username = username
        self.password = password
        self.employee_code = employee_code
        self.employee_type = employee_type
        super().__init__(**kwargs)

    def __repr__(self):
        return f"Employee(id={self.id}, Full Name={self.full_name}, Employee Type={self.employee_type})"

class Arepair:
    # Constants for window dimensions and logo path
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 620
    LOGO_PATH = resource_path('resources/arepair.png')


    def __init__(self, root, flask_app):
        # Initialize the class with root window and Flask application instance
        self.root = root
        self.flask_app = flask_app

        # Activate Flask application context
        self.app_context = flask_app.app_context()
        self.app_context.push()

        # Hide window decorations
        self.root.overrideredirect(True)

        # Load logo image
        self.logo_image = PhotoImage(file=self.LOGO_PATH)

        # Create canvas for displaying logo
        self.canvas = tk.Canvas(self.root, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)
        self.canvas.pack()
        self.canvas.create_image(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2, image=self.logo_image,
                                 anchor=tk.CENTER)

        # Configure window background color
        self.root.configure(bg='#d9dada')

        # Calculate window position to center it on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x_main = (screen_width - self.WINDOW_WIDTH) // 2
        center_y_main = (screen_height - self.WINDOW_HEIGHT) // 2

        # Set window geometry
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{center_x_main}+{center_y_main}")

        # Schedule showing the main window after 3 seconds
        self.root.after(3000, self.show_main_window)


    # Method to bind hover effects to a button
    def bind_hover_effects(self, button):
        button.bind("<Enter>", self.on_button_enter)
        button.bind("<Leave>", self.on_button_leave)

    # Method to handle mouse enter event for buttons
    @staticmethod
    def on_button_enter(event):
        event.widget.config(bg="#007fff", fg="white")

    # Method to handle mouse leave event for buttons
    @staticmethod
    def on_button_leave(event):
        event.widget.config(bg="#d9dada", fg="black")

    def green_bind_hover_effects(self, button):
        button.bind("<Enter>", self.green_on_button_enter)
        button.bind("<Leave>", self.green_on_button_leave)

    @staticmethod
    def green_on_button_enter(event):
        event.widget.config(bg="#205a3d")

    @staticmethod
    def green_on_button_leave(event):
        event.widget.config(bg="#004d00")

    def red_bind_hover_effects(self, button):
        button.bind("<Enter>", self.red_on_button_enter)
        button.bind("<Leave>", self.red_on_button_leave)

    @staticmethod
    def red_on_button_enter(event):
        event.widget.config(bg="#ff6666")

    @staticmethod
    def red_on_button_leave(event):
        event.widget.config(bg="#800000")

    def load_image(self, new_window): # Open a file dialog to select picture files
        file_paths = filedialog.askopenfilenames(
            title="Select pictures",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")],
            parent=new_window  
        )
        if file_paths:
            print("Selected files:", file_paths)

            text = file_paths
            cleaned_text = [s.replace("'", "").strip() for s in text] # cleans up the file paths, removes any single quotes

            formatted_text = ", ".join(cleaned_text) # formats them into a comma-separated string
            self.photo_paths = formatted_text

    def create_section_window(self, section):
        new_window = tk.Toplevel(self.root)
        new_window.title(section)
        new_window.iconphoto(True, PhotoImage(file=resource_path('resources/ar.png')))

        # Set the geometry of the new window
        new_window.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")

        # Center the new window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x_new_window = (screen_width - self.WINDOW_WIDTH) // 2
        center_y_new_window = (screen_height - self.WINDOW_HEIGHT) // 2
        new_window.geometry(f"+{center_x_new_window}+{center_y_new_window}")

        new_window.resizable(True, True)

        new_window.configure(bg='#d9dada')

        self.root.attributes('-disabled', True) # Disable the root window while the new window is open

        # Depending on the section, call the corresponding method to populate the new window
        if section == "Insert Service":
            self.insert_service_section(new_window)
        elif section == "Manage Services":
            self.manage_services_section(new_window)
        elif section == "Payment Records":
            self.payments_section(new_window)
        elif section == "Employees Information":
            self.employees_section(new_window)

        def close_new_window():
            self.root.attributes('-disabled', False) # Enable the root window
            new_window.destroy() # Destroy the new window

        # Call the close_new_window function when the user tries to close the new window
        new_window.protocol("WM_DELETE_WINDOW", close_new_window)

    def photo_viewer(self, window, photos, view_mode=None, result_callback=None, updated_photos=None):  # Method that creates a window to view and/or delete photos
        # Check if 'photos' is a string and split it into a list of file paths
        if isinstance(photos, str):
                paths = photos
                print(paths)
                photos = paths.split(', ')

        changed_photos = photos # This variable is used later to track changes made to the list

        # Define a function to load and resize an image
        def load_image(file_path):
            try:
                original_image = Image.open(file_path)
                width, height = original_image.size
                aspect_ratio = width / height
                target_width = 350
                target_height = int(target_width / aspect_ratio)
                resized_image = original_image.resize((target_width, target_height))
                return ImageTk.PhotoImage(resized_image)
            except Exception as e:
                print(f"Error loading image: {e}")
                return None

        # Define a function to update the displayed photo
        def update_photo(image_number):
            nonlocal photo_label, status, next_photo_button, previous_photo_button, delete_photo_button

            photo_label.grid_forget()
            delete_number = image_number - 1

            self.my_img = load_image(photos[image_number - 1])
            if self.my_img:
                photo_label = Label(photo_view_window, image=self.my_img)
                photo_label.grid(row=0, column=0, columnspan=4)
            next_photo_button.config(command=lambda: update_photo(image_number + 1))
            previous_photo_button.config(command=lambda: update_photo(image_number - 1))

            if view_mode != "Edit Mode": # If the view mode is "Edit Mode", the button to delete photos is disabled 
                delete_photo_button.config(state=DISABLED)

            delete_photo_button.config(command=lambda: delete_photo(image_number - 1))

            status.config(text="Image {} of {}".format(image_number, len(photos)))

            if len(photos) == 1 or image_number == 1:
                previous_photo_button.config(state=tk.DISABLED)
            elif image_number > 1:
                previous_photo_button.config(state=tk.NORMAL)
            
            if image_number == len(photos):

                next_photo_button.config(state=tk.DISABLED)
            else:
                next_photo_button.config(state=tk.NORMAL)

        # Define a function to delete a photo
        def delete_photo(delete_number):
            nonlocal photos

            try:
                del photos[delete_number]
                if not photos:
                    on_close(result_callback)
                else:
                    update_photo(1)
            except Exception as e:
                print(f"Error deleting photo: {e}")

        # Define a function to handle the window closure
        def on_close(result_callback):
            print(f"Original: {original_photos}")
            print(f"Changed: {changed_photos}")
            if len(original_photos) != len(', '.join(changed_photos)): # Check if there are any changes in the photos
                def handle_choice(option):
                    if option == "confirm":
                        if len(changed_photos) == 0:
                            updated_photos = "nan"
                            result_callback("confirm", updated_photos)
                            photo_view_window.destroy()
                            print("Confirm changes")
                        else:
                            updated_photos = ', '.join(changed_photos)
                            result_callback("confirm", updated_photos)
                            photo_view_window.destroy()
                            print("Confirm changes")
                    elif option == "cancel":
                        updated_photos = original_photos
                        result_callback("cancel", updated_photos)
                        photo_view_window.destroy()
                        print("Cancel changes")

                changes_warning = "Apply changes to photos?"
                self.pop_warning(photo_view_window, changes_warning, "photochanges", lambda option: handle_choice(option))
                print("There were some changes on photos")

            else:
                updated_photos = original_photos
                result_callback("cancel", updated_photos)
                photo_view_window.destroy()


        photo_view_window = tk.Toplevel(window)
        if view_mode != None:
            photo_view_window.title(f"Photo Viewer ({view_mode})")
        else:
            photo_view_window.title("Photo Viewer")
        photo_view_window.iconphoto(True, PhotoImage(file=resource_path('resources/ar.png')))
        photo_view_window.configure(bg='#d9dada')
        photo_view_window.resizable(False, False)
        photo_view_window.grab_set()

        # Create widgets for navigating and displaying photos
        photo_label = Label(photo_view_window)
        status = Label(photo_view_window, text="Image 1 of {}".format(len(photos)), fg="black", bg="#d9dada")

        previous_photo_button = tk.Button(photo_view_window, text="Previous Photo", width=15, borderwidth=1, highlightbackground="black",
                                          fg="black", bg="#d9dada", state=tk.DISABLED)
        next_photo_button = tk.Button(photo_view_window, text="Next Photo", width=15, borderwidth=1, highlightbackground="black",
                                      fg="black", bg="#d9dada")
        delete_photo_button = tk.Button(photo_view_window, text="Delete Photo", width=10, borderwidth=1, highlightbackground="black",
                                        fg="white", bg="#800000")


        previous_photo_button.grid(row=1, column=0, sticky="we")
        self.bind_hover_effects(previous_photo_button)

        next_photo_button.grid(row=1, column=1, sticky="ew")
        self.bind_hover_effects(next_photo_button)

        status.grid(row=1, column=2, sticky="ew")

        delete_photo_button.grid(row=1, column=3, sticky="ew")
        self.red_bind_hover_effects(delete_photo_button)

        update_photo(1)

        original_photos = ', '.join(photos) # Store the original photo paths

        # If the view mode is "Edit Mode" when the user tries to close the window the program will check for any changes in the photos list
        if view_mode == "Edit Mode": 
            photo_view_window.protocol("WM_DELETE_WINDOW", lambda: on_close(result_callback))

            photo_view_window.wait_window(photo_view_window)

    def change_row_color(self, tree, row_index, color):
        item_id = tree.get_children()[row_index]
        tag_name = f"row_{row_index}_tag"
        tree.item(item_id, tags=(tag_name,))
        tree.tag_configure(tag_name, background=color) # Method to change row color of treeview widget

    def toggle_combo_text(self, result, combobox): # Method to change the text color of the combobox widget 
        if result == 0:
            combobox["foreground"] = "darkred"
        else:
            combobox["foreground"] = "white"

    def toggle_entry_colors(self, result, entry): # Method to change the color of the entry boxes
        if result == 0:
            entry.configure(bg="darkred")
        else:
            entry.configure(bg="white")

    def toggle_entry_colors_ifnan(self, result, entry): # Method to change the of the entry boxes if the value is 'nan'
        if result == 0:
            entry.configure(bg="darkred")
        else:
            entry.configure(bg="white")

    def toggle_button_colors(self, result, button):  # Method to change the buttons color
        if result == 0:
            button.configure(bg='darkred')
        else:
            button.configure(bg="#d9dada")

    # Method that creates a window used to display warnings/information or confirm actions
    def pop_warning(self, window, variable, warning, choice_callback=None, photos_callback=None):
        warning_pop = tk.Toplevel(window)
        warning_pop.title("Warning")
        warning_pop.iconphoto(True, tk.PhotoImage(file=resource_path('resources/ar.png')))
        warning_pop.resizable(0,0)
        warning_pop.configure(bg="#d9dada")
        warning_pop.grab_set()

        def choice(option):
            warning_pop.destroy()
            if choice_callback:
                choice_callback(option)

        if isinstance(variable, list):

            if warning == "invalidformat":
                invalid_format = f"There was/were {len(variable)} file(s) with Invalid Format or Extension"
                label_invalid_format = tk.Label(warning_pop, text=invalid_format, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_invalid_format.pack(pady=5)


                for index, invalid in enumerate(variable, start=1):
                    invalid_label = tk.Label(warning_pop, text=f"{invalid}\n______", font=("Helvetica", 10),
                                               fg="black", bg="#d9dada")
                    invalid_label.pack()

            elif warning == "addrecvalidation":
                for error_list in variable:
                    error_text = f"There was/were {len(error_list)-1} error(s) of type: {error_list[0]}"
                    label_info_error = tk.Label(warning_pop, text=error_text, font=("Helvetica", 12),
                                                   fg="white", bg="darkred")
                    label_info_error.pack(pady=5, padx=10)

                    for error in error_list[1:]:
                        error_label = tk.Label(warning_pop, text=error, font=("Helvetica", 10),
                                                   fg="black", bg="#d9dada")
                        error_label.pack()

            elif warning == "filenotfound":
                file_not_found_warning = f"There was/were {len(variable)} file(s) not found"
                label_file_not_found = tk.Label(warning_pop, text=file_not_found_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_file_not_found.pack(pady=5)


                for notfound in variable:
                    notfound_label = tk.Label(warning_pop, text=f"{notfound}", font=("Helvetica", 10),
                                               fg="black", bg="#d9dada")
                    notfound_label.pack()

            elif warning == "wrongdatetextformat":
                wrong_format_warning = f"There was/were {len(variable)} date(s) with wrong date format\nExpected format: yyyy-mm-dd"
                label_wrong_format = tk.Label(warning_pop, text=wrong_format_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_wrong_format.pack(ipadx=10)

                for warning in variable:
                    warning_column_label = tk.Label(warning_pop, text=warning, font=("Helvetica", 10),
                                               fg="black", bg="#d9dada")
                    warning_column_label.pack(pady=(15,5))

            elif warning == "dbtotree":
                services = Service.query.all()

                if len(services) == 0:
                    warning = "The selected Database Table is empty."

                    empty_table_warning = f"Error while trying to fetch information from the Database"
                    label_empty_table_warning = tk.Label(warning_pop, text=empty_table_warning, font=("Helvetica", 12),
                                                   fg="white", bg="darkred")
                    label_empty_table_warning.pack(ipadx=10)
                    
                    empty_label = tk.Label(warning_pop, text=warning, font=("Helvetica", 10),

                                                fg="black", bg="#d9dada")
                    empty_label.pack(padx=10)
                else:

                    def check_selection(e):
                        selected_items = treeview.selection()
                        if len(selected_items) == 1:
                            confirm_record_selection_button.config(state=NORMAL)
                        else:
                            confirm_record_selection_button.config(state=DISABLED)

                    def confirm_selected():
                        selected_items = treeview.selection()
                        x = treeview.index(selected_items[0])
                        variable[1].delete(0, tk.END)
                        if variable[2] == "client":
                            variable[1].insert(0, str(df.at[x, 'Tax Number']))
                            variable[3]()
                        elif variable[2] == "vehicle":
                            variable[1].insert(0, str(df.at[x, 'Vehicle ID']).lower())
                        warning_pop.destroy()

                    def cancel_selected():
                        warning_pop.destroy()

                    warning_pop.maxsize(600,500)

                    if variable[2] == 'vehicle':

                        plate_list = []
                        for service in services:
                            if service.vehicle_id not in plate_list:
                                plate_list.append(service.vehicle_id)
                            else:
                                pass

                        df = pd.DataFrame(columns=['Vehicle ID'])

                        if len(plate_list) > 0:
                            for plate in plate_list:
                                new_df_record = {
                                    'Vehicle ID': plate
                                }

                                new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                                df = pd.concat([df, new_df_record], ignore_index=True)

                        columns_to_int = []

                    elif variable[2] == 'client':

                        check_list = []
                        client_list = []
                        for service in services:
                            print(service)
                            if service.tax_number not in check_list:
                                check_list.append(service.tax_number)
                                client_list.append(service)
                            else:
                                pass

                        df = pd.DataFrame(columns=['Full Name', 'Tax Number', 'Phone Number'])

                        if len(client_list) > 0:
                            for client in client_list:
                                new_df_record = {
                                    'Full Name': client.full_name,
                                    'Tax Number': client.tax_number,
                                    'Phone Number': client.phone_number
                                }

                                new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                                df = pd.concat([df, new_df_record], ignore_index=True)

                        columns_to_int = ['Tax Number', 'Phone Number']



                    db_valid_warning = f"Please select the {variable[2]}"
                    label_valid_record = tk.Label(warning_pop, text=db_valid_warning, font=("Helvetica", 12),
                                                   fg="white", bg="darkgreen")
                    label_valid_record.pack(pady=10)

                    treeview_confirm_frame = tk.Frame(warning_pop)
                    treeview_confirm_frame.pack()
                    treeview_confirm_frame.configure(bg="#d9dada")

                    treeScrolly = ttk.Scrollbar(treeview_confirm_frame, orient="vertical")
                    treeScrolly.pack(side="right", fill="y")

                    treeScrollx = ttk.Scrollbar(treeview_confirm_frame, orient="horizontal")
                    treeScrollx.pack(side="bottom", fill="x")

                    treeview = ttk.Treeview(treeview_confirm_frame, show="headings",
                                            yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

                    treeScrolly.config(command=treeview.yview)
                    treeScrollx.config(command=treeview.xview)

                    column_list = df.columns.tolist()

                    treeview["column"] = column_list
                    treeview["show"] = "headings"

                    for column in treeview["column"]:
                        treeview.heading(column, text=column)
                        treeview.column(column, anchor="center")

                    for column in columns_to_int:
                        try:
                            df[column] = df[column].fillna(0).astype('int64')
                            df[column] = df[column].replace(0, 'nan')
                        except ValueError:
                            pass               
                       
                    df_rows = df.to_numpy().tolist()
                    for row in df_rows:
                        treeview.insert("", "end", values=row)

                    for col in treeview["columns"]:
                        heading_width = tkFont.Font().measure(treeview.heading(col)["text"])
                        
                        max_width = max(
                            tkFont.Font().measure(str(treeview.set(item, col)))
                            for item in treeview.get_children("")
                        )
                        
                        column_width = max(heading_width, max_width) + 20 
                        
                        treeview.column(col, width=column_width, minwidth=heading_width)

                    treeview.pack(expand=True, fill="both")

                    confirm_cancel_frame = tk.Frame(warning_pop)
                    confirm_cancel_frame.pack(pady=(5,15))
                    confirm_cancel_frame.configure(bg="#d9dada")

                    confirm_record_selection_button = Button(confirm_cancel_frame, text="Confirm", fg="white",
                                                   bg="darkgreen", width=10, state=DISABLED, command=confirm_selected)
                    confirm_record_selection_button.grid(row=0, column=0, padx=10)
                    self.green_bind_hover_effects(confirm_record_selection_button) 

                    cancel_record_selection_button = Button(confirm_cancel_frame, text="Cancel", fg="white",
                                                   bg="darkred", width=10, command=lambda: choice("cancel"))
                    cancel_record_selection_button.grid(row=0, column=1, padx=10)
                    self.red_bind_hover_effects(cancel_record_selection_button)

                    treeview.bind("<ButtonRelease-1>", check_selection)

            elif warning == "showdbiteminfo":
                if variable[0] == "service":

                    if variable[1] == "vehicle":

                        services = Service.query.filter_by(vehicle_id=variable[2]).all()

                        df = pd.DataFrame(columns=['id', 'Drop-off Date', 'Check-up Date', 'Next Check-up', 'Vehicle ID', 'Mileage', 'Service Cost', 'Service Description', 'Paid', 'Billing Address', 'Payment-Method',
                                                          'Full Name', 'Phone Number', 'Email', 'Tax Number', 'Service State', 'Date Confirm Completed Service', 'Code Confirm Completed Service',
                                                           'Date Cancel Service', 'Code Cancel Service', 'Last Update', 'Code Last Update', 'Insertion Date', 'Code Insertion',  'Upload Photo', 'Receipt Photos'])

                        for service in services:                                                                    
                                new_df_record = {
                                    'id': service.id,
                                    'Drop-off Date': service.drop_off_date,
                                    'Check-up Date': service.check_up_date,
                                    'Next Check-up': service.next_check_up,
                                    'Vehicle ID': service.vehicle_id,
                                    'Mileage': service.mileage, 
                                    'Service Cost': service.service_cost, 
                                    'Service Description': service.service_description, 
                                    'Paid': service.paid, 
                                    'Billing Address': service.billing_address, 
                                    'Payment-Method': service.payment_method,
                                    'Full Name': service.full_name, 
                                    'Phone Number': service.phone_number, 
                                    'Email': service.email, 
                                    'Tax Number': service.tax_number,
                                    'Service State': service.service_state, 
                                    'Date Confirm Completed Service': service.date_confirm_completed_service,
                                    'Code Confirm Completed Service': service.code_confirm_completed_service, 
                                    'Date Cancel Service': service.date_cancel_service, 
                                    'Code Cancel Service': service.code_cancel_service,
                                    'Last Update': service.last_update,
                                    'Code Last Update': service.code_last_update,
                                    'Insertion Date': service.insertion_date,
                                    'Code Insertion': service.code_insertion,
                                    'Upload Photo': service.upload_photo,
                                    'Receipt Photos': service.photos
                                }

                                new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                                df = pd.concat([df, new_df_record], ignore_index=True)
                        
        
                    elif variable[1] == "client":

                        services = Service.query.filter_by(tax_number=variable[2]).all()

                        df = pd.DataFrame(columns=['id', 'Drop-off Date', 'Check-up Date', 'Next Check-up', 'Vehicle ID', 'Mileage', 'Service Cost', 'Service Description', 'Paid', 'Billing Address', 'Payment-Method',
                                                          'Full Name', 'Phone Number', 'Email', 'Tax Number', 'Service State', 'Date Confirm Completed Service', 'Code Confirm Completed Service',
                                                           'Date Cancel Service', 'Code Cancel Service', 'Last Update', 'Code Last Update', 'Insertion Date', 'Code Insertion',  'Upload Photo', 'Receipt Photos'])

                        for service in services:                                                                    
                                new_df_record = {
                                    'id': service.id,
                                    'Drop-off Date': service.drop_off_date,
                                    'Check-up Date': service.check_up_date,
                                    'Next Check-up': service.next_check_up,
                                    'Vehicle ID': service.vehicle_id,
                                    'Mileage': service.mileage, 
                                    'Service Cost': service.service_cost, 
                                    'Service Description': service.service_description, 
                                    'Paid': service.paid, 
                                    'Billing Address': service.billing_address, 
                                    'Payment-Method': service.payment_method,
                                    'Full Name': service.full_name, 
                                    'Phone Number': service.phone_number, 
                                    'Email': service.email, 
                                    'Tax Number': service.tax_number,
                                    'Service State': service.service_state, 
                                    'Date Confirm Completed Service': service.date_confirm_completed_service,
                                    'Code Confirm Completed Service': service.code_confirm_completed_service, 
                                    'Date Cancel Service': service.date_cancel_service, 
                                    'Code Cancel Service': service.code_cancel_service,
                                    'Last Update': service.last_update,
                                    'Code Last Update': service.code_last_update,
                                    'Insertion Date': service.insertion_date,
                                    'Code Insertion': service.code_insertion,
                                    'Upload Photo': service.upload_photo,
                                    'Receipt Photos': service.photos
                                }

                                new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                                df = pd.concat([df, new_df_record], ignore_index=True)

                elif variable[0] == "showcancelcompletedinprogress":

                    services = Service.query.filter_by(service_state=variable[1]).all()

                    df = pd.DataFrame(columns=['id', 'Drop-off Date', 'Check-up Date', 'Next Check-up', 'Vehicle ID', 'Mileage', 'Service Cost', 'Service Description', 'Paid', 'Billing Address', 'Payment-Method',
                                                      'Full Name', 'Phone Number', 'Email', 'Tax Number', 'Service State', 'Date Confirm Completed Service', 'Code Confirm Completed Service',
                                                       'Date Cancel Service', 'Code Cancel Service', 'Last Update', 'Code Last Update', 'Insertion Date', 'Code Insertion',  'Upload Photo', 'Receipt Photos'])

                    for service in services:                                                                    
                            new_df_record = {
                                'id': service.id,
                                'Drop-off Date': service.drop_off_date,
                                'Check-up Date': service.check_up_date,
                                'Next Check-up': service.next_check_up,
                                'Vehicle ID': service.vehicle_id,
                                'Mileage': service.mileage, 
                                'Service Cost': service.service_cost, 
                                'Service Description': service.service_description, 
                                'Paid': service.paid, 
                                'Billing Address': service.billing_address, 
                                'Payment-Method': service.payment_method,
                                'Full Name': service.full_name, 
                                'Phone Number': service.phone_number, 
                                'Email': service.email, 
                                'Tax Number': service.tax_number,
                                'Service State': service.service_state, 
                                'Date Confirm Completed Service': service.date_confirm_completed_service,
                                'Code Confirm Completed Service': service.code_confirm_completed_service, 
                                'Date Cancel Service': service.date_cancel_service, 
                                'Code Cancel Service': service.code_cancel_service,
                                'Last Update': service.last_update,
                                'Code Last Update': service.code_last_update,
                                'Insertion Date': service.insertion_date,
                                'Code Insertion': service.code_insertion,
                                'Upload Photo': service.upload_photo,
                                'Receipt Photos': service.photos
                            }

                            new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                            df = pd.concat([df, new_df_record], ignore_index=True)

                elif variable[0] == "paymentinfo":

                    if variable[1] == "client":

                        payments = Payment.query.filter_by(tax_number=variable[2]).all()
                        
                        df = pd.DataFrame(columns=['id', 'Service Cost', 'Service Description', 'Payment-Method', 'Paid', 'Full Name', 'Phone Number', 'Tax Number', 'Billing Address', 
                                                          'Vehicle ID', 'Last Update', 'Code Last Update', 'Insertion Date', 'Code Insertion', 'Upload Photo','Receipt Photos'])
                        for payment in payments:                                       
                            new_df_record = {
                                'id': payment.id,
                                'Service Cost': payment.service_cost,
                                'Service Description' : payment.service_description,
                                'Payment-Method': payment.payment_method,
                                'Paid': payment.paid,
                                'Full Name': payment.full_name, 
                                'Phone Number': payment.phone_number, 
                                'Tax Number': payment.tax_number, 
                                'Billing Address': payment.billing_address,
                                'Vehicle ID': payment.vehicle_id,
                                'Last Update': payment.last_update, 
                                'Code Last Update': payment.code_last_update,
                                'Insertion Date': payment.insertion_date,
                                'Code Insertion': payment.code_insertion,
                                'Upload Photo': payment.upload_photo,
                                'Receipt Photos': payment.photos
                            }

                            new_df_record = pd.DataFrame([new_df_record])  

                            df = pd.concat([df, new_df_record], ignore_index=True)


                    elif variable[1] == "vehicle":

                        payments = Payment.query.filter_by(vehicle_id=variable[2]).all()
                        
                        df = pd.DataFrame(columns=['id', 'Service Cost', 'Service Description', 'Payment-Method', 'Paid', 'Full Name', 'Phone Number', 'Tax Number', 'Billing Address', 
                                                          'Vehicle ID', 'Last Update', 'Code Last Update', 'Insertion Date', 'Code Insertion', 'Upload Photo','Receipt Photos'])
                        for payment in payments:                                    
                            new_df_record = {
                                'id': payment.id,
                                'Service Cost': payment.service_cost,
                                'Service Description' : payment.service_description,
                                'Payment-Method': payment.payment_method,
                                'Paid': payment.paid,
                                'Full Name': payment.full_name, 
                                'Phone Number': payment.phone_number, 
                                'Tax Number': payment.tax_number, 
                                'Billing Address': payment.billing_address,
                                'Vehicle ID': payment.vehicle_id,
                                'Last Update': payment.last_update, 
                                'Code Last Update': payment.code_last_update,
                                'Insertion Date': payment.insertion_date,
                                'Code Insertion': payment.code_insertion,
                                'Upload Photo': payment.upload_photo,
                                'Receipt Photos': payment.photos
                            }

                            new_df_record = pd.DataFrame([new_df_record])  

                            df = pd.concat([df, new_df_record], ignore_index=True)

                print(df)

                warning_pop.maxsize(600,500)

                db_valid_warning = "Information Table"
                label_valid_record = tk.Label(warning_pop, text=db_valid_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkgreen")
                label_valid_record.pack(pady=10)

                treeview_confirm_frame = tk.Frame(warning_pop)
                treeview_confirm_frame.pack()
                treeview_confirm_frame.configure(bg="#d9dada")


                # Create vertical scrollbar
                treeScrolly = ttk.Scrollbar(treeview_confirm_frame, orient="vertical")
                treeScrolly.pack(side="right", fill="y")

                # Create horizontal scrollbar
                treeScrollx = ttk.Scrollbar(treeview_confirm_frame, orient="horizontal")
                treeScrollx.pack(side="bottom", fill="x")

                treeview = ttk.Treeview(treeview_confirm_frame, show="headings",
                                        yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)


                treeScrolly.config(command=treeview.yview)
                treeScrollx.config(command=treeview.xview)

                def convert_to_datetime(date_string):
                    try:
                        return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                    except ValueError:
                        return date_string

                column_list = df.columns.tolist()

                if 'Next Check-up' in column_list:
                    df['Check-up Date'] = df['Check-up Date'].apply(convert_to_datetime)
                    df['Drop-off Date'] = df['Drop-off Date'].apply(convert_to_datetime)
                    df['Next Check-up'] = df['Next Check-up'].apply(convert_to_datetime)
                    df['Insertion Date'] = df['Insertion Date'].apply(convert_to_datetime)
                    photo_col = "Receipt Photos"
                    columns_to_int = ['Service Cost', 'Vehicle ID', 'Tax Number', 'Phone Number', 'Mileage']
                else:
                    df['Insertion Date'] = df['Insertion Date'].apply(convert_to_datetime)
                    photo_col = "Receipt Photos"
                    columns_to_int = ['Service Cost', 'Vehicle ID', 'Tax Number', 'Phone Number']



                def grab_photo_path(e):
                    global photos
                    selected_items = treeview.selection()
                    if len(selected_items) > 0:
                        x = treeview.index(selected_items[0])
                        if df.at[x, photo_col] == 'nan':
                            verify_photo_button.config(state=DISABLED)
                        else:
                            verify_photo_button.config(state=NORMAL)
                            paths = df.at[x, photo_col]
                            photos = paths.split(',')



                treeview["column"] = column_list
                treeview["show"] = "headings"

                for column in treeview["column"]:
                    treeview.heading(column, text=column)
                    treeview.column(column, anchor="center")

                for column in columns_to_int:
                    try:
                        df[column] = df[column].fillna(0).astype('int64')
                        df[column] = df[column].replace(0, 'nan')
                    except ValueError:
                        pass             
                   
                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    treeview.insert("", "end", values=row)

                for col in treeview["columns"]:
                    heading_width = tkFont.Font().measure(treeview.heading(col)["text"])
                    
                    max_width = max(
                        tkFont.Font().measure(str(treeview.set(item, col)))
                        for item in treeview.get_children("")
                    )
                    
                    column_width = max(heading_width, max_width) + 20

                    treeview.column(col, width=column_width, minwidth=heading_width)

                treeview.column(photo_col, width=120, minwidth=120)

                treeview.pack(expand=True, fill="both")

                verify_photo_frame = tk.Frame(warning_pop)
                verify_photo_frame.pack(pady=(15,5), expand=True, fill="both")
                verify_photo_frame.configure(bg="#d9dada")

                verify_photo_button = Button(verify_photo_frame, text="Verify Photos of Selected", fg="black",
                                               bg="#d9dada", width=20, state=DISABLED, command=lambda: self.photo_viewer(warning_pop, photos, "View Mode"))
                verify_photo_button.pack(side="right", padx=5)
                self.bind_hover_effects(verify_photo_button) 

                treeview.bind("<ButtonRelease-1>", grab_photo_path)

            elif warning == "cannotdeleteservice":
                can_not_delete_warning = f"There is/are {len(variable)} service(s) that can't be deleted due to being currently in progress"
                label_can_not_delete_warning = tk.Label(warning_pop, text=can_not_delete_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_can_not_delete_warning.pack(ipadx=10)

                for warning in variable:
                    warning_label = tk.Label(warning_pop, text=warning, font=("Helvetica", 10),
                                               fg="black", bg="#d9dada")
                    warning_label.pack(pady=(10,5))

            elif warning == "managerexpirewarning":
                can_not_delete_warning = f"There is/are {len(variable)} vehicle(s) with the next check-up expiring within 5 or less days"
                label_can_not_delete_warning = tk.Label(warning_pop, text=can_not_delete_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_can_not_delete_warning.pack(ipadx=10)

                for warning in variable:
                    warning_label = tk.Label(warning_pop, text=warning, font=("Helvetica", 10),
                                               fg="black", bg="#d9dada")
                    warning_label.pack(pady=(10,5))

        elif isinstance(variable, str):
            if warning == "nanselectedphoto":
                nan_selected_photo_warning = "The Photos column of the selected item is empty"
                label_nan_selected_photo_warning = tk.Label(warning_pop, text=nan_selected_photo_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_nan_selected_photo_warning.pack(pady=5, padx=10)
                
                empty_selected_photos_label = tk.Label(warning_pop, text=f"Index: {variable}", font=("Helvetica", 10),
                                            fg="black", bg="#d9dada")
                empty_selected_photos_label.pack()

            elif warning == "noselectedtoupdate":
                no_selected_update_warning = "Error while trying to update record"
                label_no_selected_update_warning = tk.Label(warning_pop, text=no_selected_update_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_no_selected_update_warning.pack(pady=5, padx=10)
                
                no_selected_update_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),
                                            fg="black", bg="#d9dada")
                no_selected_update_label.pack()

            elif warning == "noselectedtoseephotos":
                no_selected_viewphotos_warning = "Error while trying to see record photos"
                label_no_selected_viewphotos_warning = tk.Label(warning_pop, text=no_selected_viewphotos_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_no_selected_viewphotos_warning.pack(pady=5, padx=10)
                
                no_selected_viewphotos_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),
                                            fg="black", bg="#d9dada")
                no_selected_viewphotos_label.pack()

            elif warning == "noselectedtoremove":
                no_selected_remove_warning = "Error while trying to remove record"
                label_no_selected_remove_warning = tk.Label(warning_pop, text=no_selected_remove_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_no_selected_remove_warning.pack(pady=5, padx=10)
                
                no_selected_remove_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="black", bg="#d9dada")
                no_selected_remove_label.pack()
 
            elif warning == "photochanges":
                label_photo_changes_warning = tk.Label(warning_pop, text=variable, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_photo_changes_warning.pack(ipadx=30, ipady=5)
                
                confirm_cancel_frame = tk.Frame(warning_pop)
                confirm_cancel_frame.pack(pady=15)
                confirm_cancel_frame.configure(bg="#d9dada")

                confirm_photo_changes_button = Button(confirm_cancel_frame, text="Confirm", fg="white",
                                               bg="darkgreen", width=6, command=lambda: choice("confirm"))
                confirm_photo_changes_button.grid(row=0, column=0, padx=10)
                self.green_bind_hover_effects(confirm_photo_changes_button) 

                cancel_photo_changes_button = Button(confirm_cancel_frame, text="Cancel", fg="white",
                                               bg="darkred", width=6, command=lambda: choice("cancel"))
                cancel_photo_changes_button.grid(row=0, column=1, padx=10)
                self.red_bind_hover_effects(cancel_photo_changes_button)

            elif warning == "wrongdatetextformat":
                date_wrong_format_warning = "Date with wrong text format\nexpected: 'yyyy mm dd'"
                label_date_wrong_format_warning = tk.Label(warning_pop, text=date_wrong_format_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_date_wrong_format_warning.pack(ipadx=10)
                
                date_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="black", bg="#d9dada")
                date_label.pack(padx=10)

            elif warning == "wrongemployeecode":
                wrong_code_warning = "Error while validating employee code"
                label_wrong_code_warning = tk.Label(warning_pop, text=wrong_code_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_wrong_code_warning.pack(ipadx=10)
                
                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="black", bg="#d9dada")
                warning_label.pack(padx=10)

            elif warning == "cannotdeletealldb":
                delete_warning = "Error while trying to delete record(s)"
                label_delete_warning = tk.Label(warning_pop, text=delete_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_delete_warning.pack(ipadx=10)

                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="black", bg="#d9dada")
                warning_label.pack(padx=10)

            elif warning == "erroraddemploye":
                cant_add_warning = "Error while trying to add new employee"
                label_cant_add_warning = tk.Label(warning_pop, text=cant_add_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_cant_add_warning.pack(ipadx=10)
                
                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="black", bg="#d9dada")
                warning_label.pack(padx=10)

            elif warning == "employeecodeexists":
                cant_add_warning = "Error while trying to add new employee"
                label_cant_add_warning = tk.Label(warning_pop, text=cant_add_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_cant_add_warning.pack(ipadx=10)
                
                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="black", bg="#d9dada")
                warning_label.pack(padx=10)

            elif warning == "databaselocked":
                cant_add_warning = "Error due to Database being locked"
                label_cant_add_warning = tk.Label(warning_pop, text=cant_add_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_cant_add_warning.pack(ipadx=10)
                
                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="black", bg="#d9dada")
                warning_label.pack(padx=10)

            elif warning == "employeesdata":
                section_warning = "Error while trying to access employees data"
                label_warning = tk.Label(warning_pop, text=section_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_warning.pack(ipadx=10)

                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),
                                           fg="black", bg="#d9dada")
                warning_label.pack(pady=(15,5))

        elif isinstance(variable, dict):
            if warning == "validateaddrecord":
                validate_add_record_warning = f"Please confirm to add record"
                label_validate_add_record_warning = tk.Label(warning_pop, text=f"{validate_add_record_warning}", font=("Helvetica", 12),
                                               fg="White", bg="darkgreen")
                label_validate_add_record_warning.pack(pady=5, padx=20)

                limit=15

                for index, (key, value) in enumerate(variable.items()):
                    if index < limit:
                        validate_add_record_label = tk.Label(warning_pop, text=f"{key} : {value[0]}", font=("Helvetica", 10),
                                                    fg="black", bg="#d9dada")
                        validate_add_record_label.pack(pady=3)
                    else:
                        break

                photos_validate_label_button_frame = tk.Frame(warning_pop)
                photos_validate_label_button_frame.pack()
                photos_validate_label_button_frame.configure(bg="#d9dada")
                
                photos_to_validate_label = tk.Label(photos_validate_label_button_frame, text="Receipt Photos :", font=("Helvetica", 10),
                                                    fg="black", bg="#d9dada")
                photos_to_validate_label.grid(row=0, column=0)

                photos_to_validate_button = Button(photos_validate_label_button_frame, text="Verify Photos", fg="black",
                                               bg="#d9dada", width=10)
                photos_to_validate_button.grid(row=0, column=1)

                if variable['Receipt Photos'] != 'nan':
                    paths = variable['Receipt Photos'].strip("()")
                    photos_to_validate_label.config(text="Receipt Photos :")

                    split_paths = paths.split(', ')

                    photos_to_validate_button.config(command=lambda: self.photo_viewer(warning_pop, split_paths, "View Mode"))
                else:
                    photos_to_validate_button.config(state=DISABLED)
                
                confirm_cancel_frame = tk.Frame(warning_pop)
                confirm_cancel_frame.pack(pady=15)
                confirm_cancel_frame.configure(bg="#d9dada")

                confirm_record_validation_button = Button(confirm_cancel_frame, text="Confirm", fg="white",
                                               bg="darkgreen", width=10, command=lambda: choice("confirm"))
                confirm_record_validation_button.grid(row=0, column=0, padx=10)
                self.green_bind_hover_effects(confirm_record_validation_button) 

                cancel_record_validation_button = Button(confirm_cancel_frame, text="Cancel", fg="white",
                                               bg="darkred", width=10, command=lambda: choice("cancel"))
                cancel_record_validation_button.grid(row=0, column=1, padx=10)
                self.red_bind_hover_effects(cancel_record_validation_button)

        elif isinstance(variable, pd.core.frame.DataFrame):
            print("Is instance of Dataframe")
            if warning == "export":

                export_warning = f"Please select the desired Export Format"
                label_export_warning = tk.Label(warning_pop, text=export_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkgreen")
                label_export_warning.pack(pady=10)

                format_frame = tk.Frame(warning_pop)
                format_frame.pack(pady=(5,15))
                format_frame.configure(bg="#d9dada")

                column_list = variable.columns.tolist()

                current_date = str(datetime.now(timezone.utc))[:19].replace(":", "-")

                def export_excel(file_name):
                    file_name += "-Excel"
                    variable.to_excel(f"{file_name}.xlsx", index=False)
                    warning_pop.destroy()

                def export_csv(file_name):
                    file_name += "-CSV"
                    variable.to_csv(f"{file_name}.csv", index=False)
                    warning_pop.destroy()


                if "Check-up Date" in column_list or "check_up_date" in column_list:
                    single_item = f"Service-ID {variable.at[0, 'id']} - {current_date}"
                    multiple_items = f"Services {current_date}"
                elif "Employee Type" in column_list or "employee_type" in column_list:
                    single_item = f"Employee-ID {variable.at[0, 'id']} - {current_date}"
                    multiple_items = f"Employees {current_date}"
                else:
                    single_item = f"Payment-ID {variable.at[0, 'id']} - {current_date}"
                    multiple_items = f"Payments {current_date}"

                if len(variable) == 1:
                    file_name = single_item
                    print(file_name)
                else:
                    file_name = multiple_items
                    print(file_name)


                csv_button = Button(format_frame, text="CSV Format", fg="black",
                                               bg="#d9dada", width=10, command=lambda: export_csv(file_name))
                csv_button.grid(row=0, column=0, padx=10)
                self.bind_hover_effects(csv_button) 

                excel_button = Button(format_frame, text="Excel Format", fg="black",
                                               bg="#d9dada", width=10, command=lambda: export_excel(file_name))
                excel_button.grid(row=0, column=1, padx=10)
                self.bind_hover_effects(excel_button)

    # Method to validate the values of the inputs or selection boxes, to make sure no data is missing or the type of data is wrong
    def validate_data(self, type_of_data, num, alpha, defined, empty):
        global not_num, not_alpha, not_defined, is_empty, errors_found
              
        if type_of_data == "entries":
            not_num = ["Invalid input, must only contain numbers"]
            for column_num, value_num in num.items():
                first_value = value_num[0]
                try:
                    int(first_value)
                except ValueError:
                    not_num.append(column_num)
                    
            not_alpha = ["Invalid input, must only contain letters"]
            for column_word, value_word in alpha.items():
                first_value = value_word[0]
                clean_first_value = re.sub(r'[^\w\s]', '', first_value).replace(' ','')
                if all(char.isalpha() for char in clean_first_value):
                    pass
                else:
                    not_alpha.append(column_word)

            not_defined = ["Must select one of the options"]
            for column_defined, value_defined in defined.items():
                first_value = value_defined[0]
                if first_value == "Not Defined":
                    not_defined.append(column_defined)
                else:
                    pass

            is_empty = ["Entry is empty"]
            for column_all, value_all in empty.items():
                first_value = value_all[0]
                if len(first_value) == 0 or str(first_value).lower() == "empty" or str(first_value).lower() == "0":
                    is_empty.append(column_all)
                else:
                    pass

        elif type_of_data == "data_add_database":
            not_num = ["Invalid input, must only contain numbers"]
            for column_num, value_num in num.items():
                try:
                    int(value_num)
                except ValueError:
                    not_num.append(column_num)
                    
            not_alpha = ["Invalid input, must only contain letters"]
            for column_word, value_word in alpha.items():
                clean_first_value = re.sub(r'[^\w\s]', '', value_word).replace(' ','')
                if all(char.isalpha() for char in clean_first_value):
                    pass
                else:
                    not_alpha.append(column_word)

            not_defined = ["Must select one of the options"]
            for column_defined, value_defined in defined.items():
                first_value = value_defined[0]
                second_value = value_defined[1]
                if first_value.lower() not in [val.lower() for val in second_value] or first_value.lower() == 'not defined':
                    not_defined.append(column_defined)
                else:
                    pass

            is_empty = ["Entry is empty"]
            for column_all, value_all in empty.items():
                if len(value_all) == 0 or value_all.lower() == "nan" or value_all.lower() == "0":
                    is_empty.append(column_all)
                else:
                    pass

        errors_found = is_empty, not_defined, not_alpha, not_num

    # Method to verify the photo path and format of each photo in the list of photos
    def verify_photo_path(self, possible_photo_paths):
        global invalid_photo_paths, valid_photo_paths, valid_photo_type, invalid_photo_type

        paths_list = possible_photo_paths.split(',')

        paths_list = [path.strip() for path in paths_list]

        allowed_extensions = ['.png', '.jpg', '.jpeg']

        invalid_photo_type = []
        valid_photo_type = []
        for path in paths_list:
            if any(path.lower().endswith(ext) for ext in allowed_extensions):
                valid_photo_type.append(path)
            else:
                invalid_photo_type.append(path)

        invalid_photo_paths = []
        valid_photo_paths = []
        for path in valid_photo_type:
            try:
                print(f"Image open: {Image.open(path)}")
                Image.open(path)
                valid_photo_paths.append(path)
            except FileNotFoundError:
                invalid_photo_paths.append(path)

    # Method that creates a window where the user can select a date
    def datepicker(self, window, entry, date_type, button=None, check_date=None, next_entry=None):
        picker_calendar = tk.Toplevel(window)
        picker_calendar.title("Select a date")
        picker_calendar.iconphoto(True, tk.PhotoImage(file=resource_path('resources/ar.png')))
        picker_calendar.resizable(0,0)
        picker_calendar.configure(bg="black")
        picker_calendar.grab_set()

        def select_date():
            selected_date = cal.get_date()
            entry.config(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.insert(0, selected_date)
            entry.config(state="readonly")
            if button is not None:
                if check_date is not None:
                    button.config(state=DISABLED)
                    selected_dt = datetime.strptime(selected_date, '%Y-%m-%d').date()
                    next_date = str(selected_dt + relativedelta(months=+6))
                    next_entry.config(state=tk.NORMAL)
                    next_entry.delete(0, tk.END)
                    next_entry.insert(0, next_date)
                    next_entry.config(state="readonly")
                else:
                    button.config(state=NORMAL)

            picker_calendar.destroy()

        current_date = datetime.now().date()

        cal = Calendar(picker_calendar, selectmode='day', date_pattern='yyyy-mm-dd', date=current_date)
        cal.pack()

        if date_type == 'check-up':
            date = datetime.strptime(check_date, '%Y-%m-%d').date()
            cal.config(mindate=date)
        else:
            pass

        get_date_button = tk.Button(picker_calendar, text="Select Date", command=select_date)
        get_date_button.pack(pady=5)

    # Method to verify the employee code that the user tries to use when confirming certain actions
    def check_employee_code(self, code, must_be_manager=False):

        if code == "":
            code_result = "Must enter employee code to confirm this action"
        else:
            employee = None
            employee = Employee.query.filter(Employee.employee_code.ilike(code)).first()
            if employee is not None:
                if must_be_manager is True:
                    if employee.employee_type == "Manager":
                        code_result = "valid"
                    else:
                        code_result = "The employee with the given code is not allowed to perform this action\nMust be a Manager"
                else: code_result = "valid" 
            else:
                code_result = "The given employee code doesn't match any registered employee code" 

        return code_result

    # Method to create a window where the user can create new users/employees
    def new_employee(self):
        new_employee_window = tk.Toplevel(self.root)
        new_employee_window.title("New User")
        new_employee_window.iconphoto(True, tk.PhotoImage(file=resource_path('resources/ar.png')))
        new_employee_window.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x_new_employee = (screen_width - self.WINDOW_WIDTH) // 2
        center_y_new_employee = (screen_height - self.WINDOW_HEIGHT) // 2

        new_employee_window.geometry(f"+{center_x_new_employee}+{center_y_new_employee}")
        new_employee_window.resizable(False, False)
        new_employee_window.configure(bg='#d9dada')

        def confirm_register():
            try:
                must_be_number = {}

                must_not_have_number = {
                        'Full Name': (new_fullname_entry.get(), new_fullname_entry)
                    }

                must_be_defined = {
                        'Employee Type': (selected_type.get(), type_combobox)
                }

                must_not_be_empty = {
                     
                        'Full Name': (new_fullname_entry.get(), new_fullname_entry),
                        'Username': (new_username_entry.get(), new_username_entry),
                        'Password': (new_password_entry.get(), new_password_entry),
                        'Confirm Password': (confirm_password_entry.get(), confirm_password_entry),                               
                        'Employee Code': (employee_code_entry.get(), employee_code_entry)
                    }

                self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

                if any(len(error_list) > 1 for error_list in errors_found):
                    result_of_validation = "Error Found" 
                    print("Error Found")
                else:
                    result_of_validation = "No Error Found"
                    print("No Error Found")

                if result_of_validation == "No Error Found":
                    try:
                        with self.flask_app.app_context():
                            db.create_all()
                            code =  re.sub(r'[^\w\s]', '', str(employee_code_entry.get()).lower())
                            existing_code = Employee.query.filter(Employee.employee_code.ilike(code)).first()
                            if existing_code is not None:
                                self.toggle_entry_colors(0, employee_code_entry)
                                warning = f"The following employee code {code} already exists in the Database\nPlease choose a different employee code"
                                self.pop_warning(new_employee_window, warning, "employeecodeexists")
                            else:
                                self.toggle_entry_colors(1, employee_code_entry)
                                if new_password_entry.get() == confirm_password_entry.get():
                                    self.toggle_entry_colors(1, new_password_entry)
                                    self.toggle_entry_colors(1, confirm_password_entry)
                                    if len(new_password_entry.get()) < 10:
                                        warning="Password is too short\nPlease use at least 10 characters"
                                        self.pop_warning(new_employee_window, warning, "erroraddemploye")
                                        return
                                    existing_user = Employee.query.filter(Employee.username.ilike(new_username_entry.get())).first()
                                    if existing_user:
                                        warning="Username already exists\nChoose a different username"
                                        self.pop_warning(new_employee_window, warning, "erroraddemploye")
                                        return

                                    password_hash = bcrypt.generate_password_hash(new_password_entry.get()).decode('utf-8')

                                    new_employee = Employee(full_name=new_fullname_entry.get(), 
                                        username=new_username_entry.get(), 
                                        password=password_hash,
                                        employee_code=employee_code_entry.get(),
                                        employee_type=selected_type.get())

                                    db.session.add(new_employee)

                                    db.session.commit()
                                    new_employee_window.destroy()
                                else:
                                    self.toggle_entry_colors(0, new_password_entry)
                                    self.toggle_entry_colors(0, confirm_password_entry)
                                    warning="Passwords do not match"
                                    self.pop_warning(new_employee_window, warning, "erroraddemploye")
                    except OperationalError as e:
                        warning = "Database is locked. Please close the Database and try again."
                        self.pop_warning(new_employee_window, warning, "databaselocked")
                        db.session.rollback()
                        print("Database is locked. Please try again later.")
                else:
                    for key in must_not_be_empty:
                        if key in is_empty:
                            entry_value = must_not_be_empty[key][1]
                            self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                            if key == "Year":
                                year_entry.config(readonlybackground="darkred")
                        else:
                            self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                    for key in must_be_defined:
                        if key in not_defined:
                            combobox_value = must_be_defined[key][1]
                            self.toggle_combo_text(0, must_be_defined[key][1])
                        else:
                            self.toggle_combo_text(1, must_be_defined[key][1])

                    for key in must_not_have_number:
                        if key in not_alpha or key in is_empty:
                            entry_value = must_not_have_number[key][1]
                            self.toggle_entry_colors(0, must_not_have_number[key][1])
                        else:
                            self.toggle_entry_colors(1, must_not_have_number[key][1])

                    for key in must_be_number:
                        if key in not_num or key in is_empty:
                            entry_value = must_be_number[key][1]
                            self.toggle_entry_colors(0, must_be_number[key][1])
                        else:
                            self.toggle_entry_colors(1, must_be_number[key][1])

                    errors_adding = []
                    for error_list in errors_found:
                        if len(error_list) > 1:
                            errors_adding.append(error_list)

                    if len(errors_adding) > 0:
                        self.pop_warning(new_employee_window, errors_adding, "addrecvalidation")
            except Exception as e:
                print(e)

        label_font = ("Helvetica", 20)
        new_employee_label = tk.Label(new_employee_window, text="Register new User", font=label_font, fg="black", bg='#d9dada')
        new_employee_label.pack(pady=(50, 20))

        new_fullname_label = tk.Label(new_employee_window, text="Full Name:", fg="black", bg='#d9dada')
        new_fullname_label.pack(side=tk.TOP, padx=10, pady=2)
        new_fullname_entry = Entry(new_employee_window, width=35, bd=1, highlightbackground="black")
        new_fullname_entry.pack(side=tk.TOP, pady=2)

        new_username_label = tk.Label(new_employee_window, text="Choose a Username:", fg="black", bg='#d9dada')
        new_username_label.pack(side=tk.TOP, padx=10, pady=2)
        new_username_entry = Entry(new_employee_window, width=35, bd=1, highlightbackground="black")
        new_username_entry.pack(side=tk.TOP, pady=2)

        new_password_label = tk.Label(new_employee_window, text="Password:", fg="black", bg='#d9dada')
        new_password_label.pack(side=tk.TOP, padx=10, pady=(10, 2))
        new_password_entry = Entry(new_employee_window, show="*", width=35, bd=1, highlightbackground="black")
        new_password_entry.pack(side=tk.TOP, pady=2)

        confirm_password_label = tk.Label(new_employee_window, text="Confirm Password:", fg="black", bg='#d9dada')
        confirm_password_label.pack(side=tk.TOP, padx=10, pady=(10, 2))
        confirm_password_entry = Entry(new_employee_window, show="*", width=35, bd=1, highlightbackground="black")
        confirm_password_entry.pack(side=tk.TOP, pady=2)

        employee_code_label = tk.Label(new_employee_window, text="Employee code:", fg="black", bg='#d9dada')
        employee_code_label.pack(side=tk.TOP, padx=10, pady=(10, 2))
        employee_code_entry = Entry(new_employee_window, width=35, bd=1, highlightbackground="black")
        employee_code_entry.pack(side=tk.TOP, pady=2)

        type_employee_label = tk.Label(new_employee_window, text="Employee type:",
                         font=("Helvetica", 10), fg="black", bg='#d9dada')
        type_employee_label.pack(side=tk.TOP, padx=10, pady=(10, 2))
        employee_types = ['Not Defined', 'Regular', 'Manager']
        selected_type = tk.StringVar()
        type_combobox = ttk.Combobox(new_employee_window,
                                        textvariable=selected_type,
                                        values=employee_types, state="readonly",  justify="center", height=4, width=10,
                                        style="TCombobox")
        type_combobox.pack(side=tk.TOP, pady=2)
        type_combobox.set(employee_types[0]) 

        new_register_button = tk.Button(new_employee_window, text="Register", width=15, command=confirm_register, fg="white", bg="#004d00", borderwidth=1, highlightbackground="black")
        new_register_button.pack(side=tk.TOP, pady=(20, 30))
        self.green_bind_hover_effects(new_register_button)

        new_employee_window.grab_set()

    # Section to insert/make services into the database
    def insert_service_section(self, new_window):

        new_window.geometry("1000x340")

        def check_if_photos():
            if hasattr(self, 'photo_paths'):
                see_photos_button.configure(state=tk.NORMAL)

                self.check_image_path = resource_path('resources/check.png')
                self.check_photos_image = ImageTk.PhotoImage(Image.open(self.check_image_path))
                reload_show_photos_button.configure(image=self.check_photos_image)
            else:
                see_photos_button.configure(state=tk.DISABLED)

                self.update_photos_button_image_path = resource_path('resources/update.png')
                self.update_photos_button_image = ImageTk.PhotoImage(Image.open(self.update_photos_button_image_path))

                reload_show_photos_button.configure(image=self.update_photos_button_image)

        def add_service_db():
            must_be_number = {
                    'Tax Number': (tax_num_entry.get(), tax_num_entry),
                    'Phone Number': (phone_entry.get(), phone_entry),
                    'Service Cost': (service_cost_entry.get(), service_cost_entry),
                    'Mileage': (mileage_entry.get(), mileage_entry)
                }

            must_not_have_number = {'Full Name': (full_name_entry.get(), full_name_entry)
                }

            must_be_defined = {
                    'Payment-Method' : (selected_pay_type.get(), pay_type_combobox)
                }

            must_not_be_empty = {
                    'Vehicle ID': (vehicle_id_entry.get(), vehicle_id_entry),
                    'Tax Number': (tax_num_entry.get(), tax_num_entry),
                    'Check-up Date': (check_up_entry.get(), check_up_entry),
                    'Drop-off Date': (drop_entry.get(), drop_entry),
                    'Service Cost': (service_cost_entry.get(), service_cost_entry),
                    'Service Description': (service_description_entry.get(), service_description_entry),
                    'Phone Number': (phone_entry.get(), phone_entry),
                    'Next Check-up': (next_check_up_entry.get(), next_check_up_entry),
                    'Full Name': (full_name_entry.get(), full_name_entry),
                    'Mileage': (mileage_entry.get(), mileage_entry)
                }

            self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

            if photo_checkbox_var.get():
                upload = 'Yes'
                if hasattr(self, 'photo_paths'):
                    self.toggle_button_colors(1, select_photos_button)
                    photos = self.photo_paths
                else:
                    is_empty.append("Photos")
            else:
                upload = 'No'
                photos = 'nan'

            if any(len(error_list) > 1 for error_list in errors_found):
                result_of_validation = "Error Found"
            else:
                result_of_validation = "No Error Found"

            if result_of_validation == "No Error Found":
                code_check=self.check_employee_code(str(employee_code_entry.get()), False)
                if code_check == "valid":
                    self.toggle_combo_text(1, pay_type_combobox)

                    entries = [service_cost_entry, service_description_entry, tax_num_entry, billing_address_entry,
                    full_name_entry, phone_entry, email_entry, vehicle_id_entry, employee_code_entry, mileage_entry]

                    read_only_entries = [check_up_entry, drop_entry, next_check_up_entry]
                    
                    for entry in entries:
                        self.toggle_entry_colors(1, entry)

                    for entry in read_only_entries:
                        entry.config(readonlybackground="white")


                    self.toggle_button_colors(1, select_photos_button)
                    self.bind_hover_effects(select_photos_button)

                    def handle_choice(option, possible_new_record):
                        if option == "confirm":
                            try:
                                def create_payment_record():
                                    payment_record = Payment(
                                        service_cost = int(service_cost_entry.get()),
                                        service_description = str(service_description_entry.get()),
                                        payment_method = selected_pay_type.get(),
                                        paid = box_value,
                                        upload_photo = upload,
                                        full_name = str(full_name_entry.get()),
                                        phone_number = int(phone_entry.get()),
                                        tax_number = re.sub(r'[^\w\s]', '', str(tax_num_entry.get()).lower()),
                                        billing_address = str(billing_address_entry.get()), 
                                        vehicle_id = re.sub(r'[^\w\s]', '', str(vehicle_id_entry.get()).lower()),
                                        photos = photos,
                                        code_insertion = str(employee_code_entry.get())
                                        )

                                    db.session.add(payment_record)
                                    db.session.commit()

                                with self.flask_app.app_context():
                                    db.create_all()

                                    service = Service(
                                        drop_off_date = str(drop_entry.get()),
                                        check_up_date = str(check_up_entry.get()),
                                        next_check_up = str(next_check_up_entry.get()),
                                        vehicle_id = re.sub(r'[^\w\s]', '', str(vehicle_id_entry.get()).lower()),
                                        mileage = str(mileage_entry.get()),
                                        service_description = str(service_description_entry.get()),
                                        full_name = str(full_name_entry.get()),
                                        phone_number = int(phone_entry.get()),
                                        email = str(email_entry.get()),
                                        tax_number = re.sub(r'[^\w\s]', '', str(tax_num_entry.get()).lower()),
                                        service_cost = int(service_cost_entry.get()),
                                        billing_address = str(billing_address_entry.get()),
                                        payment_method = selected_pay_type.get(),
                                        paid = box_value,
                                        upload_photo = upload,
                                        photos = photos,
                                        code_insertion = str(employee_code_entry.get())
                                    )

                                    db.session.add(service)
                                    db.session.commit()

                                    create_payment_record()
                                    print("Checkbox is checked.")
                                    
                                    for entry in entries:
                                        entry.delete(0, tk.END)

                                    for entry in read_only_entries:
                                        entry.config(state=tk.NORMAL)
                                        entry.delete(0, tk.END)
                                        entry.config(state="readonly")

                                    combos = [[pay_type_combobox, pay_types]]
                                    for combo in combos:
                                        self.toggle_combo_text(1, combo[0])
                                        combo[0].set(combo[1][0])

                                    if hasattr(self, 'photo_paths'):
                                        del self.photo_paths

                                                        
                                    paid_checkbox_var.set(0)
                                    photo_checkbox_var.set(0)

                                    check_if_photos()
                            except OperationalError as e:
                                warning = "Database is locked. Please close the Database and try again."
                                self.pop_warning(new_window, warning, "databaselocked")
                                db.session.rollback()
                                print("Database is locked. Please try again later.")

                        elif option == "cancel":
                            print("User canceled")

                    if paid_checkbox_var.get():
                        box_value = "Yes"
                    else:
                        box_value = "No"

                    optional_entries = [billing_address_entry, email_entry]

                    for entry in optional_entries:
                        if len(entry.get()) == 0:
                            entry.insert(0, 'Not Inserted')

                    possible_new_record = {
                    'Drop-off Date': [drop_entry.get()],
                    'Check-up Date': [check_up_entry.get()],
                    'Next Check-up' : [next_check_up_entry.get()],
                    'Vehicle ID': [vehicle_id_entry.get()],
                    'Mileage': [mileage_entry.get()], 
                    'Service Cost': [service_cost_entry.get()], 
                    'Service Description': [service_description_entry.get()],
                    'Full Name': [full_name_entry.get()], 
                    'Phone Number': [int(phone_entry.get())], 
                    'Email': [email_entry.get()],
                    'Paid' : [box_value],
                    'Upload Photo' : [upload],
                    'Tax Number': [int(tax_num_entry.get())], 
                    'Billing Address': [billing_address_entry.get()], 
                    'Payment-Method': [selected_pay_type.get()],
                    'Receipt Photos': photos,
                    }

                    self.pop_warning(new_window, possible_new_record, "validateaddrecord", lambda option: handle_choice(option, possible_new_record))
                else:
                    self.pop_warning(new_window, code_check, "wrongemployeecode")
                    self.toggle_entry_colors(0, employee_code_entry)
            else:
                for key in must_not_be_empty:
                    if key in is_empty:
                        entry_value = must_not_be_empty[key][1]
                        self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                        if key == "Check-up Date":
                            check_up_entry.config(readonlybackground="darkred")
                        if key == "Drop-off Date":
                            drop_entry.config(readonlybackground="darkred")
                        if key == "Next Check-up":
                            next_check_up_entry.config(readonlybackground="darkred")
                    else:
                        self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                for key in must_be_defined:
                    if key in not_defined:
                        combobox_value = must_be_defined[key][1]
                        self.toggle_combo_text(0, must_be_defined[key][1])
                    else:
                        self.toggle_combo_text(1, must_be_defined[key][1])

                for key in must_not_have_number:
                    if key in not_alpha or key in is_empty:
                        entry_value = must_not_have_number[key][1]
                        self.toggle_entry_colors(0, must_not_have_number[key][1])
                    else:
                        self.toggle_entry_colors(1, must_not_have_number[key][1])

                if "Photos" in is_empty:
                    self.toggle_button_colors(0, select_photos_button)
                    self.red_bind_hover_effects(select_photos_button)

                else:
                    self.toggle_button_colors(1, select_photos_button)
                    self.bind_hover_effects(select_photos_button)

                for key in must_be_number:
                    if key in not_num or key in is_empty:
                        entry_value = must_be_number[key][1]
                        self.toggle_entry_colors(0, must_be_number[key][1])
                    else:
                        self.toggle_entry_colors(1, must_be_number[key][1])

                errors_adding = []
                for error_list in errors_found:
                    if len(error_list) > 1:
                        errors_adding.append(error_list)

                if len(errors_adding) > 0:
                    self.pop_warning(new_window, errors_adding, "addrecvalidation")

        insert_service_frame = tk.Frame(new_window)
        insert_service_frame.configure(bg="#d9dada")
        insert_service_frame.pack(pady=10)

        # Function to retrieve the data of the selected client and then fills the entry boxes with the respective information
        def client_info(*args):
            try:
                cleaned_tax_number = re.sub(r'[^\w\s]', '', str(tax_num_entry.get()).lower())
                existing_client = Service.query.filter(Service.tax_number.ilike(cleaned_tax_number)).first()

                client_entries = [full_name_entry, phone_entry, email_entry, billing_address_entry, tax_num_entry]

                if existing_client:
                    for entry in client_entries:
                        entry.delete(0, tk.END)

                    full_name_entry.insert(0, str(existing_client.full_name))
                    phone_entry.insert(0, int(existing_client.phone_number))
                    email_entry.insert(0, str(existing_client.email))
                    tax_num_entry.insert(0, str(existing_client.tax_number))
                    billing_address_entry.insert(0, str(existing_client.billing_address))
                else:
                    pass
            except ValueError:
                pass

        def update_photos_button_state():
            if photo_checkbox_var.get():
                select_photos_button.config(state=NORMAL)
            else:
                select_photos_button.config(state=DISABLED)

        select_vehicle_button = tk.Button(insert_service_frame, text="Select Vehicle", width=20, borderwidth=1, highlightbackground="black",
                                              fg="black", bg="#d9dada")
        select_vehicle_button.grid(row=0, column=0, columnspan=2, pady=5, padx=5)
        self.bind_hover_effects(select_vehicle_button)

        select_client_button = tk.Button(insert_service_frame, text="Select Client", width=15, borderwidth=1, highlightbackground="black",
                                              fg="black", bg="#d9dada")
        select_client_button.grid(row=0, column=2, columnspan=2, pady=5, padx=5)
        self.bind_hover_effects(select_client_button)

        drop_button = tk.Button(insert_service_frame, text="Select the Drop-off Date", width=22, borderwidth=1, highlightbackground="black",
                                              fg="black", bg="#d9dada", command=lambda: self.datepicker(new_window, drop_entry, "drop", check_up_button))
        drop_button.grid(row=1, column=0, pady=5, padx=(10, 5), sticky=tk.E)
        self.bind_hover_effects(drop_button)
        drop_entry = tk.Entry(insert_service_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        drop_entry.grid(row=1, column=1, pady=5, padx=(5, 10), sticky=tk.W)


        check_up_button = tk.Button(insert_service_frame, text="Select the Check-up Date", width=22, borderwidth=1, highlightbackground="black",
                                              fg="black", bg="#d9dada", state=DISABLED, command=lambda: self.datepicker(new_window, check_up_entry, "check-up", check_up_button, drop_entry.get(), next_check_up_entry))
        check_up_button.grid(row=2, column=0, pady=5, padx=(10, 5), sticky=tk.E)
        self.bind_hover_effects(check_up_button)
        check_up_entry = tk.Entry(insert_service_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        check_up_entry.grid(row=2, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        next_check_up_label = tk.Label(insert_service_frame, text="Next Check-up:",
                               font=("Helvetica", 10), fg="black", bg="#d9dada")
        next_check_up_label.grid(row=3, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        next_check_up_entry = tk.Entry(insert_service_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        next_check_up_entry.grid(row=3, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        vehicle_id_label = tk.Label(insert_service_frame, text="Vehicle ID:",
                               font=("Helvetica", 10), fg="black", bg="#d9dada")
        vehicle_id_label.grid(row=4, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        vehicle_id_entry = tk.Entry(insert_service_frame, bd=1, highlightbackground="black",  width=10)
        vehicle_id_entry.grid(row=4, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        mileage_label = tk.Label(insert_service_frame, text="Mileage:",
                               font=("Helvetica", 10), fg="black", bg="#d9dada")
        mileage_label.grid(row=5, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        mileage_entry = tk.Entry(insert_service_frame, bd=1, highlightbackground="black",  width=10)
        mileage_entry.grid(row=5, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        service_cost_label = tk.Label(insert_service_frame, text="Service Cost:",
                               font=("Helvetica", 10), fg="black", bg="#d9dada")
        service_cost_label.grid(row=1, column=4, pady=5, padx=(20, 5), sticky=tk.E)
        service_cost_entry = tk.Entry(insert_service_frame, bd=1, highlightbackground="black",  width=10)
        service_cost_entry.grid(row=1, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        pay_method_label = tk.Label(insert_service_frame, text="Payment-Method:",
                                 font=("Helvetica", 10), fg="black", bg="#d9dada")
        pay_method_label.grid(row=2, column=4, pady=5, padx=(10, 5), sticky=tk.E)
        pay_types = ["Not Defined", "Cash", "Credit Card", "Paypal", "Bank Transfer", "Google Pay", "Apple Pay"]
        selected_pay_type = tk.StringVar()
        pay_type_combobox = ttk.Combobox(insert_service_frame,
                                        textvariable=selected_pay_type,
                                        values=pay_types, state="readonly",  justify="center", height=4, width=10,
                                        style="TCombobox")
        pay_type_combobox.grid(row=2, column=5, pady=5, padx=(5, 10), sticky=tk.W)
        pay_type_combobox.set(pay_types[0])

        paid_checkbox_label = tk.Label(insert_service_frame, text="Paid",
                                 font=("Helvetica", 12), fg="black", bg="#d9dada")
        paid_checkbox_label.grid(row=3, column=4, pady=5, padx=(10, 5), sticky=tk.E)

        paid_checkbox_var = tk.BooleanVar()
        paid_checkbox = tk.Checkbutton(insert_service_frame, variable=paid_checkbox_var, font=("Helvetica", 12), fg="black", bg="#d9dada")
        paid_checkbox.grid(row=3, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        photo_checkbox_label = tk.Label(insert_service_frame, text="Upload Receipt Photos",
                                 font=("Helvetica", 12), fg="black", bg="#d9dada")
        photo_checkbox_label.grid(row=4, column=4, pady=5, padx=(10, 5), sticky=tk.E)

        photo_checkbox_var = tk.BooleanVar()
        photo_checkbox = tk.Checkbutton(insert_service_frame, variable=photo_checkbox_var, command=update_photos_button_state, font=("Helvetica", 12), fg="black", bg="#d9dada")
        photo_checkbox.grid(row=4, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        select_photos_button = tk.Button(insert_service_frame, text="Select Receipt Photos", width=18, borderwidth=1, highlightbackground="black",
                                         fg="black", bg="#d9dada", state=DISABLED, command=lambda: self.load_image(new_window))
        select_photos_button.grid(row=5, column=4, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(select_photos_button)


        def handle_photo_viewer_result(result, updated_photos):
            if result == "confirm":
                self.photo_paths = updated_photos
                if self. photo_paths == 'nan':
                    del self.photo_paths
                    check_if_photos()
            elif result == "cancel":
                print("User cancelled changes")

        updated_photos = []
        see_photos_button = tk.Button(insert_service_frame, text="See Receipt Photos", width=18, borderwidth=1, highlightbackground="black",
                                      fg="black", bg="#d9dada", state=DISABLED,
                                      command=lambda: self.photo_viewer(new_window, self.photo_paths, "Edit Mode", handle_photo_viewer_result, updated_photos))
        see_photos_button.grid(row=5, column=5, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(see_photos_button)

        update_photos_button_image_path = resource_path('resources/update.png')
        self.update_photos_button_image = ImageTk.PhotoImage(Image.open(update_photos_button_image_path))
        reload_show_photos_button = tk.Button(insert_service_frame, image=self.update_photos_button_image,
                                              command=check_if_photos, borderwidth=0, highlightthickness=0)
        reload_show_photos_button.grid(row=5, column=6, pady=5, padx=5, sticky="w")

        full_name_label = tk.Label(insert_service_frame, text="Full Name:",
                                   font=("Helvetica", 10), fg="black", bg="#d9dada")
        full_name_label.grid(row=1, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        full_name_entry = tk.Entry(insert_service_frame, bd=1, highlightbackground="black",  width=10)
        full_name_entry.grid(row=1, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        phone_label = tk.Label(insert_service_frame, text="Phone Number:",
                               font=("Helvetica", 10), fg="black", bg="#d9dada")
        phone_label.grid(row=2, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        phone_entry = tk.Entry(insert_service_frame, bd=1, highlightbackground="black",  width=10)
        phone_entry.grid(row=2, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        email_label = tk.Label(insert_service_frame, text="Email:",
                               font=("Helvetica", 10), fg="black", bg="#d9dada")
        email_label.grid(row=3, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        email_entry = tk.Entry(insert_service_frame, bd=1, highlightbackground="black",  width=10)
        email_entry.grid(row=3, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        tax_num_label = tk.Label(insert_service_frame, text="Tax Number:",
                               font=("Helvetica", 10), fg="black", bg="#d9dada")
        tax_num_label.grid(row=4, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        tax_num_entry = tk.Entry(insert_service_frame, bd=1, highlightbackground="black",  width=10)
        tax_num_entry.grid(row=4, column=3, pady=5, padx=(5, 10), sticky=tk.W)
        tax_num_entry.bind("<KeyRelease>", client_info)

        billing_address_label = tk.Label(insert_service_frame, text="Billing Address:",
                                 font=("Helvetica", 10), fg="black", bg="#d9dada")
        billing_address_label.grid(row=5, column=2, pady=5, padx=(10, 5), sticky=tk.E)
        billing_address_entry = tk.Entry(insert_service_frame, bd=1, highlightbackground="black",  width=10)
        billing_address_entry.grid(row=5, column=3, pady=5, padx=(5, 10), sticky=tk.W) 
 
        service_description_label = tk.Label(insert_service_frame, text="Service Description:",
                          font=("Helvetica", 10), fg="black", bg="#d9dada")
        service_description_label.grid(row=6, column=0, pady=5, padx=5, sticky=tk.E)

        service_description_entry = tk.Entry(insert_service_frame, bd=1, highlightbackground="black",  width=50)
        service_description_entry.grid(row=6, column=1, columnspan=3, padx=(5,10), pady=5)

        employee_code_label = tk.Label(insert_service_frame, text="Employee Code:",
                          font=("Helvetica", 10), fg="black", bg="#d9dada")
        employee_code_label.grid(row=6, column=4, pady=5, padx=5, sticky=tk.E)

        employee_code_entry = tk.Entry(insert_service_frame, bd=1, highlightbackground="black",  width=10)
        employee_code_entry.grid(row=6, column=5, padx=5, pady=5, sticky=tk.W)

        add_service_button = tk.Button(insert_service_frame, text="Add Service", width=20, borderwidth=1, highlightbackground="black",
                                          fg="white", bg="#004d00",
                                          command=add_service_db)
        add_service_button.grid(row=9, column=0, columnspan=7, padx=5, pady=(20,5), sticky=tk.E+tk.W)
        self.green_bind_hover_effects(add_service_button)

        get_vehicle = ["service", vehicle_id_entry, "vehicle"]
        select_vehicle_button.config(command=lambda: self.pop_warning(new_window, get_vehicle, "dbtotree"))

        get_client = ["service", tax_num_entry, "client", client_info]
        select_client_button.config(command=lambda: self.pop_warning(new_window, get_client, "dbtotree"))

    # Section to manage services
    def manage_services_section(self, new_window):
        treeFrame = tk.Frame(new_window)
        treeFrame.pack(expand=True, fill="both")
        treeFrame.configure(bg="#d9dada")

        df_section_info = "Database table is empty"
        df_section_info_label = tk.Label(treeFrame, text=df_section_info, font=("Helvetica", 10),
                                           fg="darkred", bg="#d9dada")
        df_section_info_label.pack(pady=(140, 0))
        
        edit_treeview_frame = tk.Frame(new_window)
        edit_treeview_frame.pack(pady=10)
        edit_treeview_frame.configure(bg="#d9dada")

        try:
            database_uri = self.flask_app.config['SQLALCHEMY_DATABASE_URI']
            engine = create_engine(database_uri)
            df = pd.read_sql_table("service", con=engine)
            engine.dispose()
        except ValueError:
            print("ValueError")

        def create_tree_from_db(df):
            for widget in treeFrame.winfo_children():
                widget.destroy()

            treeScrolly = ttk.Scrollbar(treeFrame, orient="vertical")
            treeScrolly.pack(side="right", fill="y")

            treeScrollx = ttk.Scrollbar(treeFrame, orient="horizontal")
            treeScrollx.pack(side="bottom", fill="x")

            treeview = ttk.Treeview(treeFrame, show="headings",
                                    yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

            treeScrolly.config(command=treeview.yview)
            treeScrollx.config(command=treeview.xview)

            def update_tree_data(df):

                def reset():
                    all_services_checkbox_var.set(1)
                    paid_services_checkbox_var.set(0)
                    unpaid_services_checkbox_var.set(0)
                    search_entry.delete(0, tk.END)
                    found_label.config(text="Not Found", fg="black", bg="#d9dada", width=15)
                    filter_box(all_services_checkbox_var)

                def search(*args):
                    try:
                        cleaned_tax_number = re.sub(r'[^\w\s]', '', str(search_entry.get()).lower())
                        existing_client = Service.query.filter(Service.tax_number.ilike(cleaned_tax_number)).first()

                        cleaned_vehicle_id = re.sub(r'[^\w\s]', '', str(search_entry.get()).lower())
                        existing_vehicle = Service.query.filter(Service.vehicle_id.ilike(cleaned_vehicle_id)).first()

                        list_box = [all_services_checkbox_var, unpaid_services_checkbox_var, paid_services_checkbox_var]
                        if existing_client or existing_vehicle:
                            found_label.config(text="Valid", bg="darkgreen", fg="white", width=15)
                            for box in list_box:
                                if box.get() == 1:
                                    print(box)
                                    filter_box(box)
                            print("Exists")
                        else:
                            found_label.config(text="Not Found", fg="black", bg="#d9dada", width=15)
                            print("Dont exist")

                    except ValueError:
                        pass

                def export_selected():
                    selected_items = treeview.selection()
                    if len(selected_items) > 0:

                        selected_df = pd.DataFrame(columns=['id', 'Drop-off Date', 'Check-up Date','Next Check-up', 'Vehicle ID', 'Mileage', 'Service Cost', 'Service Description', 'Paid', 'Billing Address', 'Payment-Method',
                                                          'Full Name', 'Phone Number', 'Email', 'Tax Number', 'Service State', 'Date Confirm Completed Service', 'Code Confirm Completed Service',
                                                           'Date Cancel Service', 'Code Cancel Service', 'Last Update', 'Code Last Update', 'Insertion Date', 'Code Insertion',  'Upload Photo', 'Photos'])
                        for record in selected_items: 
                            x = treeview.index(record)                                       
                            new_df_record = {
                                'id': df.at[x, 'id'],
                                'Drop-off Date': df.at[x, 'drop_off_date'],
                                'Check-up Date': df.at[x, 'check_up_date'],
                                'Next Check-up': df.at[x, 'next_check_up'],
                                'Vehicle ID': df.at[x, 'vehicle_id'],
                                'Mileage': df.at[x, 'mileage'], 
                                'Service Cost': df.at[x, 'service_cost'], 
                                'Service Description': df.at[x, 'service_description'], 
                                'Paid': df.at[x, 'paid'], 
                                'Billing Address': df.at[x, 'billing_address'], 
                                'Payment-Method': df.at[x, 'payment_method'],
                                'Full Name': df.at[x, 'full_name'], 
                                'Phone Number': df.at[x, 'phone_number'], 
                                'Email': df.at[x, 'email'], 
                                'Tax Number': df.at[x, 'tax_number'],
                                'Service State': df.at[x, 'service_state'], 
                                'Date Confirm Completed Service': df.at[x, 'date_confirm_completed_service'],
                                'Code Confirm Completed Service': df.at[x, 'code_confirm_completed_service'], 
                                'Date Cancel Service': df.at[x, 'date_cancel_service'], 
                                'Code Cancel Service': df.at[x, 'code_cancel_service'],
                                'Last Update': df.at[x, 'last_update'],
                                'Code Last Update': df.at[x, 'code_last_update'],
                                'Insertion Date': df.at[x, 'insertion_date'],
                                'Code Insertion': df.at[x, 'code_insertion'],
                                'Upload Photo': df.at[x, 'upload_photo'],
                                'Photos': df.at[x, 'photos']
                            }

                            new_df_record = pd.DataFrame([new_df_record])

                            selected_df = pd.concat([selected_df, new_df_record], ignore_index=True)
                        self.pop_warning(new_window, selected_df, "export")

                # Function to see the information of the client inserted in the selected service
                def check_client_services():
                    selected_items = treeview.selection()

                    if len(selected_items) > 0:
                        x = treeview.index(selected_items[0])
                        get_client_service = ["service", "client", str(df.at[x, 'tax_number'])]
                        self.pop_warning(new_window, get_client_service, "showdbiteminfo")

                # Function to see the information of the vehicle inserted in the selected service
                def check_vehicle_services():
                    selected_items = treeview.selection()

                    if len(selected_items) > 0:
                        x = treeview.index(selected_items[0])
                        get_vehicle_service = ["service", "vehicle", str(df.at[x, 'vehicle_id'])]
                        self.pop_warning(new_window, get_vehicle_service, "showdbiteminfo")

                # Function that allows to confirm that the selected service is completed
                def confirm_completed_service():
                    selected_items = treeview.selection()

                    if len(selected_items) > 0:
                        x = treeview.index(selected_items[0])
                        print(employee_code_entry.get())
                        result = self.check_employee_code(str(employee_code_entry.get()), False)
                        print(result)
                        if result == "valid":
                            try:
                                self.toggle_entry_colors(1, employee_code_entry)
                                current_date_str = str(datetime.now().date())
                                service = Service.query.filter_by(id=int(df.at[x, 'id'])).first()
                                service.service_state = "Completed"
                                service.date_cancel_service = "Not Applicable"
                                service.code_cancel_service = "Not Applicable"
                                service.code_confirm_completed_service = str(employee_code_entry.get())
                                service.date_confirm_completed_service = current_date_str

                                db.session.commit()

                                df.at[x, 'service_state'] = "Completed"
                                df.at[x, 'date_cancel_service'] = "Not Applicable"
                                df.at[x, 'code_cancel_service'] = "Not Applicable"
                                df.at[x, 'code_confirm_completed_service'] = str(employee_code_entry.get())
                                df.at[x, 'date_confirm_completed_service'] = current_date_str
                                refresh_tree(df)
                            except OperationalError as e:
                                warning = "Database is locked. Please close the Database and try again."
                                self.pop_warning(new_window, warning, "databaselocked")
                                db.session.rollback()
                                print("Database is locked. Please try again later.")
                        else:
                            self.toggle_entry_colors(0, employee_code_entry)
                            self.pop_warning(new_window, result, "wrongemployeecode")

                # Function that allows canceling the selected service
                def cancel_service():
                    selected_items = treeview.selection()

                    if len(selected_items) > 0:
                        x = treeview.index(selected_items[0])
                        result = self.check_employee_code(str(employee_code_entry.get()), True)
                        if result == "valid":
                            try:
                                self.toggle_entry_colors(1, employee_code_entry)
                                current_date_str = str(datetime.now().date())
                                service = Service.query.filter_by(id=int(df.at[x, 'id'])).first()
                                service.service_state = "Cancelled"
                                service.date_confirm_completed_service = "Not Applicable"
                                service.code_confirm_completed_service = "Not Applicable"
                                service.code_cancel_service = str(employee_code_entry.get())
                                service.date_cancel_service = current_date_str

                                db.session.commit()

                                df.at[x, 'service_state'] = "Cancelled"
                                df.at[x, 'code_confirm_completed_service'] = "Not Applicable"
                                df.at[x, 'date_confirm_completed_service'] = "Not Applicable"
                                df.at[x, 'code_cancel_service'] = str(employee_code_entry.get())
                                df.at[x, 'date_cancel_service'] = current_date_str
                                refresh_tree(df)
                            except OperationalError as e:
                                warning = "Database is locked. Please close the Database and try again."
                                self.pop_warning(new_window, warning, "databaselocked")
                                db.session.rollback()
                                print("Database is locked. Please try again later.")
                        else:
                            self.toggle_entry_colors(0, employee_code_entry)
                            self.pop_warning(new_window, result, "wrongemployeecode")
                                        
                def verify_data():
                    for index, row in df.iterrows():
                        not_num = []
                        must_be_number = {
                            'Service Cost': row['service_cost'],
                            'Phone Number': row['phone_number'],
                            'Mileage': row['mileage']
                        }
                        for column_num, value_num in must_be_number.items():
                            try:
                                int(value_num)
                            except ValueError:
                                not_num.append(value_num)

                        not_alpha = []
                        must_not_have_number = {
                            'Full Name': str(row['full_name']),
                            'Payment-Method': str(row['payment_method']),
                            'Paid': str(row['paid']),
                            'Upload Photo': str(row['upload_photo'])
                        }

                        for column_word, value_word in must_not_have_number.items():
                            clean_value_word = re.sub(r'[^\w\s]', '', value_word).replace(' ','')
                            if all(char.isalpha() for char in clean_value_word):
                                pass
                            else:
                                not_alpha.append(value_word)

                        is_empty = []
                        all_data = {
                            'Service Cost': row['service_cost'],
                            'Service Description': str(row['service_description']),
                            'Paid': str(row['paid']),
                            'Phone Number': row['phone_number'],
                            'Full Name': str(row['full_name']),
                            'Next Check-up': str(row['next_check_up']),
                            'Payment-Method': str(row['payment_method']),
                            'Check-up Date': str(row['check_up_date']),
                            'Drop-off Date': str(row['drop_off_date']),
                            'Vehicle ID': str(row['vehicle_id']),
                            'Email': str(row['email']),
                            'Billing Address': str(row['billing_address']),
                            'Tax Number': str(row['tax_number']),
                            'Upload Photo': str(row['upload_photo']),
                            'Mileage': str(row['mileage'])
                        }
                        for column_all, value_all in all_data.items():
                            if value_all == 'nan':
                                is_empty.append(value_all)
                            else:
                                pass

                        not_defined = []
                        must_be_defined = {
                            'Payment-Method': (str(row['payment_method']), pay_types)
                        }
                        for column_defined, value_defined in must_be_defined.items():
                            if value_defined[0].lower() not in [val.lower() for val in value_defined[1]] or value_defined[0].lower() == 'not defined':
                                not_defined.append(value_defined)
                            else:
                                pass

                        errors_found = not_num, not_alpha, is_empty, not_defined

                        if str(row['upload_photo']) != 'No':
                            possible_photo_path_list = str(row['photos'])

                            self.verify_photo_path(possible_photo_path_list)
                            if len(valid_photo_paths) > 0 or len(valid_photo_type) > 0:
                                pass
                            if len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                                is_empty.append("Photos")

                        date_check_up_check = str(row['check_up_date'])
                        date_drop_check = str(row['drop_off_date'])
                        date_next_check = str(row['next_check_up'])

                        dates_to_check = [date_check_up_check, date_drop_check]
                        pattern = r"\b\d{4}-\d{2}-\d{2}\b"                    

                        if any(len(error_list) > 0 for error_list in errors_found) or any(bool(re.match(pattern, date)) == False for date in dates_to_check): 
                            result_of_validation = "Error Found"
                            self.change_row_color(treeview, index, "darkred")
                        else:
                            self.change_row_color(treeview, index, "white")
                            result_of_validation = "No Error Found"

                        if str(row['service_state']) ==  "Completed":
                            self.change_row_color(treeview, index, "white")
                        elif str(row['service_state']) ==  "Cancelled":
                            self.change_row_color(treeview, index, "#777777")
                        elif str(row['service_state']) == "In progress":
                            self.change_row_color(treeview, index, "lightgreen")

                def refresh_tree(df):
                          
                    treeview.delete(*treeview.get_children())

                    def convert_to_datetime(date_string):
                        try:
                            return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                        except ValueError:
                            return date_string

                    df['check_up_date'] = df['check_up_date'].apply(convert_to_datetime)
                    df['drop_off_date'] = df['drop_off_date'].apply(convert_to_datetime)
                    df['next_check_up'] = df['next_check_up'].apply(convert_to_datetime)
                    df['insertion_date'] = df['insertion_date'].apply(convert_to_datetime)

                    treeview["column"] = list(df)
                    treeview["show"] = "headings"

                    for column in treeview["column"]:
                        treeview.heading(column, text=column)
                        treeview.column(column, anchor="center")


                    columns_to_int = ['service_cost', 'vehicle_id', 'tax_number', 'phone_number', 'mileage']
                    for column in columns_to_int:
                        try:
                            df[column] = df[column].fillna(0).astype('int64')
                            df[column] = df[column].replace(0, 'nan')
                        except ValueError:
                            pass              
                       
                    df_rows = df.to_numpy().tolist()
                    for row in df_rows:
                        treeview.insert("", "end", values=row)

                    for col in treeview["columns"]:
                        heading_width = tkFont.Font().measure(treeview.heading(col)["text"])

                        try:
                            max_width = max(
                                tkFont.Font().measure(str(treeview.set(item, col)))
                                for item in treeview.get_children("")
                            )
                        except OverflowError:
                            max_width = 0  
                        
                        column_width = max(heading_width, max_width) + 20 
                        treeview.column(col, width=column_width, minwidth=column_width)

                    treeview.column("photos", width=120, minwidth=120)
                    treeview.update_idletasks()

                    verify_data()

                def clear_entries():

                    entries = [service_cost_entry, service_description_entry, tax_num_entry, billing_address_entry,
                    full_name_entry, phone_entry, email_entry, vehicle_id_entry, employee_code_entry, mileage_entry]

                    read_only_entries = [check_up_entry, drop_entry, next_check_up_entry]

                    for entry in entries:
                        entry.delete(0, tk.END)
                        self.toggle_entry_colors(1, entry)

                    for entry in read_only_entries:
                        entry.config(state=tk.NORMAL)
                        entry.delete(0, tk.END)
                        entry.config(state="readonly")
                        entry.config(readonlybackground="white")

                    combos = [[pay_type_combobox, pay_types]]
                    for combo in combos:
                        self.toggle_combo_text(1, combo[0])
                        combo[0].set(combo[1][0])

                    self.toggle_button_colors(1, select_photos_button)
                    self.bind_hover_effects(select_photos_button)

                    self.toggle_button_colors(1, selected_receipt_photos_button)
                    self.bind_hover_effects(selected_receipt_photos_button)

                    paid_checkbox_var.set(0)
                    photo_checkbox_var.set(0)

                    if hasattr(self, 'photo_paths'):
                        del self.photo_paths
                    see_photos_button.configure(state=tk.DISABLED)
                    reload_show_photos_button.configure(image=self.update_photos_button_image)

                def select_record(e):
                    clear_entries()
                    selected_items = treeview.selection()

                    if len(selected_items) > 0:
                        x = treeview.index(selected_items[0])
                        self.toggle_entry_colors(1, employee_code_entry)
                        self.toggle_button_colors(1, select_photos_button)

                        export_selected_button.configure(state=NORMAL)
                        vehicle_services_button.configure(state=NORMAL)
                        client_services_button.configure(state=NORMAL)

                        if str(df.at[x, 'service_state']) == "In progress":
                            cancel_service_button.configure(state=NORMAL)
                            confirm_completed_button.configure(state=NORMAL)
                        else:
                            cancel_service_button.configure(state=DISABLED)
                            confirm_completed_button.configure(state=DISABLED)

                        type_pay = str(df.at[x, "payment_method"]).lower()

                        pay_type_combobox.set(pay_types[0]) 
                        mapping = {p.lower(): pay_types[i] for i, p in enumerate(pay_types)}
                        pay_type_combobox.set(mapping.get(type_pay, mapping["not defined"]))

                        if pay_type_combobox.get() == 'Not Defined':
                            self.toggle_combo_text(0, pay_type_combobox)
                        else:
                            self.toggle_combo_text(1, pay_type_combobox)

                        all_entries = [[str(df.at[x,'service_cost']), service_cost_entry], [str(df.at[x, 'service_description']), service_description_entry], [str(df.at[x, 'tax_number']), tax_num_entry],
                        [str(df.at[x, 'billing_address']), billing_address_entry], [str(df.at[x, 'full_name']), full_name_entry], [str(df.at[x, 'phone_number']), phone_entry], [str(df.at[x, 'email']), email_entry],
                        [str(df.at[x, 'vehicle_id']), vehicle_id_entry], [str(df.at[x, 'mileage']), mileage_entry]]

                        for value in all_entries:
                            if value[0].lower() == 'nan':
                                self.toggle_entry_colors_ifnan(0, value[1])
                                value[1].delete(0, 'end')
                                value[1].insert(0, 'EMPTY')
                            else:
                                value[1].insert(0, str(value[0]))
                                self.toggle_entry_colors_ifnan(1, value[1])

                        number_entries = [[str(df.at[x,'service_cost']), service_cost_entry], [str(df.at[x, 'phone_number']), phone_entry], [str(df.at[x, 'mileage']), mileage_entry]]

                        for value in number_entries:
                            try:
                                int(value[0])
                                self.toggle_entry_colors(1, value[1])
                            except ValueError:
                                self.toggle_entry_colors(0, value[1])

                        if any(not char.isalpha() for char in df.at[x, 'full_name']) or str(df.at[x, 'full_name']).lower() == "empty":
                            self.toggle_entry_colors(0, full_name_entry)
                        else:
                            self.toggle_entry_colors(1, full_name_entry)
                        
                        if str(df.at[x, 'paid']).lower() == 'yes':
                            paid_checkbox_var.set(1)
                        else:
                            paid_checkbox_var.set(0)

                        if str(df.at[x, 'upload_photo']).lower() == 'yes':
                            photo_checkbox_var.set(1)
                            select_photos_button.config(state=NORMAL)
                        else:
                            photo_checkbox_var.set(0)
                            select_photos_button.config(state=DISABLED)

                        read_only_entries = [check_up_entry, drop_entry, next_check_up_entry]

                        for entry in read_only_entries:
                            entry.config(state=tk.NORMAL)

                        date_check_up_check = str(df.at[x, 'check_up_date'])
                        date_drop_check = str(df.at[x, 'drop_off_date'])
                        next_check_up_check = str(df.at[x, 'next_check_up'])

                        dates_to_check = [[date_check_up_check, check_up_entry], [date_drop_check, drop_entry], [next_check_up_check, next_check_up_entry]]
                        pattern = r"\b\d{4}-\d{2}-\d{2}\b"                                
                        inval_date = []
                        for date in dates_to_check:
                            if bool(re.match(pattern, date[0])) == False:
                                date[1].insert(0, str(date[0]))
                                date[1].config(readonlybackground="darkred")
                                inval_date.append(date)
                            else:
                                date[1].insert(0, str(date[0]))
                                date[1].config(readonlybackground="white")

                        for entry in read_only_entries:
                            entry.config(state="readonly")

                        if str(df.at[x, 'upload_photo']) != 'No':
                            self.verify_photo_path(str(df.at[x, "photos"]))
                            if str(df.at[x, "photos"]).lower() == "nan" or len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                                self.toggle_button_colors(0, selected_receipt_photos_button)
                            else:
                                self.toggle_button_colors(1, selected_receipt_photos_button)
                                print(df.at[x, "photos"])
                        else:
                            self.toggle_button_colors(1, selected_receipt_photos_button)

                        if str(df.at[x,'photos']) == 'nan':
                            selected_receipt_photos_button.config(state=DISABLED)
                        else:
                            selected_receipt_photos_button.config(state=NORMAL)

                    else:
                        pass

                def update_record():
                    must_be_number = {
                            'Tax Number': (tax_num_entry.get(), tax_num_entry),
                            'Phone Number': (phone_entry.get(), phone_entry),
                            'Service Cost': (service_cost_entry.get(), service_cost_entry),
                            'Mileage': (mileage_entry.get(), mileage_entry)
                        }

                    must_not_have_number = {'Full Name': (full_name_entry.get(), full_name_entry)
                        }

                    must_be_defined = {
                            'Payment-Method' : (selected_pay_type.get(), pay_type_combobox)
                        }

                    must_not_be_empty = {
                            'Vehicle ID': (vehicle_id_entry.get(), vehicle_id_entry),
                            'Tax Number': (tax_num_entry.get(), tax_num_entry),
                            'Check-up Date': (check_up_entry.get(), check_up_entry),
                            'Drop-off Date': (drop_entry.get(), drop_entry),
                            'Service Cost': (service_cost_entry.get(), service_cost_entry),
                            'Service Description': (service_description_entry.get(), service_description_entry),
                            'Phone Number': (phone_entry.get(), phone_entry),
                            'Next Check-up':(next_check_up_entry.get(), next_check_up_entry),
                            'Full Name': (full_name_entry.get(), full_name_entry),
                            'Mileage': (mileage_entry.get(), mileage_entry)
                        }
                    self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

                    selected_items = treeview.selection()
                    if len(selected_items) > 0:
                        x = treeview.index(selected_items[0])

                        if photo_checkbox_var.get():
                            upload = 'Yes'

                            if hasattr(self, 'photo_paths'):
                                photos = self.photo_paths
                            else:
                                self.verify_photo_path(str(df.at[x, 'photos']))
                                if str(df.at[x, 'photos']).lower() == "nan" or len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                                    is_empty.append("Photos")
                        else:
                            upload = 'No'
                            photos = 'nan'


                        date_check_up_check = str(check_up_entry.get())
                        date_drop_check = str(drop_entry.get())
                        date_next_check = str(next_check_up_entry.get())

                        dates_to_check = [date_check_up_check, date_drop_check]
                        pattern = r"\b\d{4}-\d{2}-\d{2}\b" 

                        if any(len(error_list) > 1 for error_list in errors_found) or any(bool(re.match(pattern, date)) == False for date in dates_to_check): 
                            result_of_validation = "Error Found"
                        else:
                            result_of_validation = "No Error Found"

                        service = Service.query.filter_by(id=int(df.at[x, 'id'])).first()

                        if result_of_validation == "No Error Found":
                            result = self.check_employee_code(str(employee_code_entry.get()), False)
                            if result == "valid":
                                self.toggle_entry_colors(1, employee_code_entry)
                                try:
                                    date_update = str(datetime.now(timezone.utc).date())

                                    if paid_checkbox_var.get():
                                        box_value = "Yes"
                                    else:
                                        box_value = "No"

                                    optional_entries = [billing_address_entry, email_entry]

                                    for entry in optional_entries:
                                        if len(entry.get()) == 0:
                                            entry.insert(0, 'Not Inserted')

                                    def update_payment_record():
                                        pay_record = Payment.query.filter_by(id=service.id).first()
                                        pay_record.service_cost = int(service_cost_entry.get())
                                        pay_record.service_description = str(service_description_entry.get())
                                        pay_record.payment_method = selected_pay_type.get()
                                        pay_record.paid = box_value
                                        pay_record.full_name = str(full_name_entry.get())
                                        pay_record.phone_number = int(phone_entry.get())
                                        pay_record.tax_number = re.sub(r'[^\w\s]', '', str(tax_num_entry.get()).lower())
                                        pay_record.billing_address = str(billing_address_entry.get())
                                        pay_record.vehicle_id = re.sub(r'[^\w\s]', '', str(vehicle_id_entry.get()).lower())
                                        pay_record.code_last_update = str(employee_code_entry.get())
                                        pay_record.last_update = str(date_update)
                                        pay_record.upload_photo = upload

                                        if hasattr(self, 'photo_paths'):
                                            pay_record.photos = photos
                                        else:
                                            pass

                                        db.session.commit()

                                    service.drop_off_date = str(drop_entry.get())
                                    service.check_up_date = str(check_up_entry.get())
                                    service.next_check_up = str(next_check_up_entry.get())
                                    service.vehicle_id = re.sub(r'[^\w\s]', '', str(vehicle_id_entry.get()).lower())
                                    service.mileage = str(mileage_entry.get())
                                    service.service_description = str(service_description_entry.get())
                                    service.full_name = str(full_name_entry.get())
                                    service.phone_number = int(phone_entry.get())
                                    service.email = str(email_entry.get())
                                    service.tax_number = re.sub(r'[^\w\s]', '', str(tax_num_entry.get()).lower())
                                    service.service_cost = int(service_cost_entry.get())
                                    service.billing_address = str(billing_address_entry.get())
                                    service.payment_method = selected_pay_type.get()
                                    service.paid = box_value
                                    service.code_last_update = str(employee_code_entry.get())
                                    service.last_update = str(date_update)
                                    service.upload_photo = upload
                                    
                                    if hasattr(self, 'photo_paths'):
                                        service.photos = photos
                                    else:
                                        pass

                                    db.session.commit()
                                    self.toggle_button_colors(1, selected_receipt_photos_button)

                                    df.at[x, "drop_off_date"] = drop_entry.get()
                                    df.at[x, "check_up_date"] = check_up_entry.get()
                                    df.at[x, "next_check_up"] = next_check_up_entry.get()
                                    df.at[x, "vehicle_id"] = re.sub(r'[^\w\s]', '', str(vehicle_id_entry.get()).lower())
                                    df.at[x, "mileage"] = str(mileage_entry.get())
                                    df.at[x, "service_description"] = service_description_entry.get()
                                    df.at[x, "service_cost"] = service_cost_entry.get()
                                    df.at[x, "full_name"] = full_name_entry.get()
                                    df.at[x, "phone_number"] = str(phone_entry.get())
                                    df.at[x, "email"] = str(email_entry.get())
                                    df.at[x, "tax_number"] = re.sub(r'[^\w\s]', '', str(tax_num_entry.get()).lower())
                                    df.at[x, "billing_address"] = billing_address_entry.get()
                                    df.at[x, "payment_method"] = selected_pay_type.get()
                                    df.at[x, "paid"] = box_value
                                    df.at[x, "code_last_update"] = str(employee_code_entry.get())
                                    df.at[x, "last_update"] = str(date_update)
                                    df.at[x, "upload_photo"] = upload

                                    if hasattr(self, 'photo_paths'):
                                        df.at[x, 'photos'] = photos
                                    else:
                                        pass

                                    update_payment_record()
                                    clear_entries()
                                    refresh_tree(df)
                                except OperationalError as e:
                                    warning = "Database is locked. Please close the Database and try again."
                                    self.pop_warning(new_window, warning, "databaselocked")
                                    db.session.rollback()
                                    print("Database is locked. Please try again later.")
                            else:
                                self.toggle_entry_colors(0, employee_code_entry)
                                self.pop_warning(new_window, result, "wrongemployeecode")
                        else:
                            wrong_date_format = []
                            for date in dates_to_check:
                                if bool(re.match(pattern, date)) == False:
                                    wrong_date_format.append(date)
                                    self.pop_warning(new_window, wrong_date_format, "wrongdatetextformat")

                            for key in must_not_be_empty:
                                if key in is_empty:
                                    entry_value = must_not_be_empty[key][1]
                                    self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                                    if key == "Check-up Date":
                                        check_up_entry.config(readonlybackground="darkred")
                                    if key == "Drop-off Date":
                                        drop_entry.config(readonlybackground="darkred")
                                    if key == "Next Check-up":
                                        next_check_up_entry.config(readonlybackground="darkred")
                                else:
                                    self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                            for key in must_be_defined:
                                if key in not_defined:
                                    combobox_value = must_be_defined[key][1]
                                    self.toggle_combo_text(0, must_be_defined[key][1])
                                else:
                                    self.toggle_combo_text(1, must_be_defined[key][1])

                            for key in must_not_have_number:
                                if key in not_alpha or key in is_empty:
                                    entry_value = must_not_have_number[key][1]
                                    self.toggle_entry_colors(0, must_not_have_number[key][1])
                                else:
                                    self.toggle_entry_colors(1, must_not_have_number[key][1])

                            if "Photos" in is_empty:
                                self.toggle_button_colors(0, select_photos_button)
                            else:
                                self.toggle_button_colors(1, select_photos_button)

                            for key in must_be_number:
                                if key in not_num or key in is_empty:
                                    entry_value = must_be_number[key][1]
                                    self.toggle_entry_colors(0, must_be_number[key][1])
                                else:
                                    self.toggle_entry_colors(1, must_be_number[key][1])

                            errors_adding = []
                            for error_list in errors_found:
                                if len(error_list) > 1:
                                    errors_adding.append(error_list)
                            if len(errors_adding) > 0:
                                self.pop_warning(new_window, errors_adding, "addrecvalidation")
                    else:
                        warning = "Must select an item to Update"
                        self.pop_warning(new_window, warning, "noselectedtoupdate" )

                def remove_selected():
                    selected_items = treeview.selection()
                    if len(selected_items) > 0:
                        try:
                            if len(selected_items) == Service.query.count():
                                warning = "Can not delete all the data from the Services Database"
                                self.pop_warning(new_window, warning, "cannotdeletealldb" )
                            else:
                                code_check=self.check_employee_code(str(employee_code_entry.get()), True)
                                if code_check == "valid":
                                    self.toggle_entry_colors(1, employee_code_entry)
                                    can_not_delete = []
                                    for record in selected_items:
                                        x = treeview.index(record)
                                        service = Service.query.filter_by(id=int(df.at[x, 'id'])).first()
                                        if service.service_state == "In progress":
                                            can_not_delete.append(service.id)
                                        else:
                                            pay_record = Payment.query.filter_by(id=service.id).first()
                                            db.session.delete(service)
                                            db.session.delete(pay_record)
                                            db.session.commit()     
                                            treeview.delete(record)
                                            df.drop(index=x, inplace=True)
                                            df.reset_index(drop=True, inplace=True)
                                    verify_data()
                                    clear_entries()
                                    if len(can_not_delete) > 0:
                                        self.pop_warning(new_window, can_not_delete, "cannotdeleteservice")
                                else:
                                    self.toggle_entry_colors(0, employee_code_entry)
                                    self.pop_warning(new_window, code_check, "wrongemployeecode")
                        except OperationalError as e:
                            warning = "Database is locked. Please close the Database and try again."
                            self.pop_warning(new_window, warning, "databaselocked")
                            db.session.rollback()
                            print("Database is locked. Please try again later.")
                    else:
                        warning = "Must select at least one record to remove"
                        self.pop_warning(new_window, warning, "noselectedtoremove")

                def selected_receipt_photos():
                    selected_items = treeview.selection()
                    print(selected_items)
                    if len(selected_items) > 0:
                        x = treeview.index(selected_items[0])
                        photos_of_selected = str(df.at[x, "photos"])

                        if photos_of_selected.lower() != "nan":
                            self.verify_photo_path(photos_of_selected)

                            if len(valid_photo_type) > 0:
                                print(valid_photo_type)
                                if len(valid_photo_paths) > 0:
                                    def handle_photo_viewer_result(result, updated_photos):
                                        if result == "confirm":
                                            try:
                                                service = Service.query.filter_by(id=int(df.at[x, 'id'])).first()
                                                service.photos = updated_photos
                                                pay_record = Payment.query.filter_by(id=service.id).first()
                                                pay_record.photos = updated_photos
                                                db.session.commit() 
                                                df.at[x, 'photos'] = updated_photos
                                            except OperationalError as e:
                                                warning = "Database is locked. Please close the Database and try again."
                                                self.pop_warning(new_window, warning, "databaselocked")
                                                db.session.rollback()
                                                print("Database is locked. Please try again later.")
                                        elif result == "cancel":
                                            print("User cancelled changes")

                                    if str(df.at[x, "service_state"]) == "In progress":
                                        mode = "View Mode"
                                    else:
                                        mode = "Edit Mode"

                                    updated_photos = []
                                    self.photo_viewer(new_window, valid_photo_paths, mode, handle_photo_viewer_result, updated_photos)
                                if len(invalid_photo_paths) > 0:
                                    self.pop_warning(new_window, invalid_photo_paths,"filenotfound")
                                    self.toggle_button_colors(0, selected_receipt_photos_button)
                            for path in invalid_photo_type:
                                if path == "":
                                    invalid_photo_type.remove(path)
                            if len(invalid_photo_type) > 0:
                                self.pop_warning(new_window, invalid_photo_type,"invalidformat")
                                self.toggle_button_colors(0, selected_receipt_photos_button)
                        else:
                            x += 1
                            self.pop_warning(new_window, str(x), "nanselectedphoto")
                            self.toggle_button_colors(0, selected_receipt_photos_button)
                    else:
                        warning = "Must select a record to see photos"
                        self.pop_warning(new_window, warning, "noselectedtoseephotos")

                def expiring_check_up():
                    self.pop_warning(self.root, expiring_list, "managerexpirewarning")

                refresh_tree(df)

                update_button.config(command=update_record)
                clear_entries_button.config(command=clear_entries)
                selected_receipt_photos_button.config(command=selected_receipt_photos)
                remove_selected_button.config(command=remove_selected)
                refresh_tree_button.config(command=lambda: refresh_tree(df))               
                reset_button.config(command=reset)
                client_services_button.config(command=check_client_services)
                vehicle_services_button.config(command=check_vehicle_services)
                confirm_completed_button.config(command=confirm_completed_service)
                cancel_service_button.config(command=cancel_service)
                export_all_button.config(command=lambda: self.pop_warning(new_window, df, "export"), state=NORMAL)
                export_selected_button.config(command=export_selected)
                check_up_expiring_button.config(command=expiring_check_up)

                treeview.bind("<ButtonRelease-1>", select_record)
                search_entry.bind("<KeyRelease>", search)



            update_button = Button(edit_treeview_frame, text="Update Record", fg="black", bg="#d9dada")
            update_button.grid(row=0, column=0, padx=5, pady=3)
            self.bind_hover_effects(update_button)

            clear_entries_button = Button(edit_treeview_frame, text="Clear Entries", fg="black", bg="#d9dada")
            clear_entries_button.grid(row=0, column=1, padx=5, pady=3)
            self.bind_hover_effects(clear_entries_button)

            selected_receipt_photos_button = Button(edit_treeview_frame, text="See Selected Receipt Photos",
                                                    fg="black",
                                                    bg="#d9dada")
            selected_receipt_photos_button.grid(row=0, column=2, padx=5, pady=3)
            self.bind_hover_effects(selected_receipt_photos_button)

            remove_selected_button = Button(edit_treeview_frame, text="Remove Selected Record(s)", fg="black",
                                            bg="#d9dada")
            remove_selected_button.grid(row=0, column=3, padx=5, pady=3)
            self.bind_hover_effects(remove_selected_button)

            refresh_tree_button = Button(edit_treeview_frame, text="Refresh Tree", fg="black",
                                       bg="#d9dada")
            refresh_tree_button.grid(row=0, column=4, padx=5, pady=3)
            self.bind_hover_effects(refresh_tree_button)

            check_up_expiring_button = Button(edit_treeview_frame, text="Expiring Check-up",
                                                    fg="black",
                                                    bg="#d9dada", state=DISABLED)
            check_up_expiring_button.grid(row=0, column=5, padx=5, pady=3)
            self.bind_hover_effects(check_up_expiring_button)

            employee_code_label = tk.Label(edit_treeview_frame, text="Employee Code:",
                              font=("Helvetica", 10), fg="black", bg="#d9dada")
            employee_code_label.grid(row=0, column=6, pady=5, padx=(20, 5), sticky=tk.E)

            employee_code_entry = tk.Entry(edit_treeview_frame, bd=1, highlightbackground="black",  width=10)
            employee_code_entry.grid(row=0, column=7, padx=5, pady=3)


            def filter_box(box):
                print(box)
                filter_list = [[paid_services_checkbox_var, Service.query.filter_by(paid="Yes").all()], [unpaid_services_checkbox_var, Service.query.filter_by(paid="No").all()]]

                if search_entry.get():
                    print("search not empty")
                else:
                    print("search empty")

                current_text = found_label.cget("text")
                print(current_text)
                if current_text == 'Valid':
                    print("Button is normal")
                    content = re.sub(r'[^\w\s]', '', str(search_entry.get()).lower())
                    print(content)
                    if all_services_checkbox_var == box:
                        all_services_checkbox_var.set(1)
                        paid_services_checkbox_var.set(0)
                        unpaid_services_checkbox_var.set(0)
                        vehicle = Service.query.filter(Service.vehicle_id == content).all()
                        client = Service.query.filter(Service.tax_number == content).all()
                        if len(vehicle) > 0:
                            services = vehicle
                        elif len(client) > 0:
                            services = client
                    elif paid_services_checkbox_var == box:
                        unpaid_services_checkbox_var.set(0)
                        all_services_checkbox_var.set(0)
                        vehicle = Service.query.filter(Service.paid == "Yes", Service.vehicle_id == content).all()
                        client = Service.query.filter(Service.paid == "Yes", Service.tax_number == content).all()
                        if len(vehicle) > 0:
                            services = vehicle
                        elif len(client) > 0:
                            services = client
                        else:
                            services = 0
                    elif unpaid_services_checkbox_var == box:
                        all_services_checkbox_var.set(0)
                        paid_services_checkbox_var.set(0)
                        vehicle = Service.query.filter(Service.paid == "No", Service.vehicle_id == content).all()
                        client = Service.query.filter(Service.paid == "No", Service.tax_number == content).all()
                        if len(vehicle) > 0:
                            services = vehicle
                        elif len(client) > 0:
                            services = client
                        else:
                            services = 0
                    else:
                        all_services_checkbox_var.set(1)
                        vehicle = Service.query.filter(Service.vehicle_id == content).all()
                        client = Service.query.filter(Service.tax_number == content).all()
                        if len(vehicle) > 0:
                            services = vehicle
                        elif len(client) > 0:
                            services = client


                elif current_text == 'Not Found':
                    search_entry.delete(0, tk.END)

                    if all_services_checkbox_var == box:
                        all_services_checkbox_var.set(1)
                        services = Service.query.all()
                        paid_services_checkbox_var.set(0)
                        unpaid_services_checkbox_var.set(0)
                    elif any(b[0].get() == 1 for b in filter_list):
                        print("One box is checked")

                        for b in filter_list:
                            if b[0] != box:
                                b[0].set(0)
                            else:
                                all_services_checkbox_var.set(0)
                                services = b[1]
                    else:
                        print("No box is checked")
                        services = Service.query.all()
                        all_services_checkbox_var.set(1)



                if services == 0 or len(services) == 0:
                    df = pd.DataFrame(columns=['id', 'drop_off_date', 'check_up_date', 'next_check_up', 'vehicle_id', 'mileage', 'service_cost', 'service_description', 'paid', 'billing_address', 'payment_method',
                              'full_name', 'phone_number', 'email', 'tax_number', 'service_state', 'date_confirm_completed_service', 'code_confirm_completed_service',
                               'date_cancel_service', 'code_cancel_service', 'last_update', 'code_last_update', 'insertion_date', 'code_insertion',  'upload_photo', 'photos'])

                                                                
                    new_df_record = {
                        'id': 'Not Found', 
                        'drop_off_date': 'Not Found',
                        'check_up_date': 'Not Found',
                        'next_check_up': 'Not Found',
                        'vehicle_id': 'Not Found',
                        'mileage': 'Not Found', 
                        'service_cost': 'Not Found', 
                        'service_description': 'Not Found', 
                        'paid': 'Not Found', 
                        'billing_address': 'Not Found', 
                        'payment_method': 'Not Found',
                        'full_name': 'Not Found', 
                        'phone_number': 'Not Found', 
                        'email': 'Not Found', 
                        'tax_number': 'Not Found',
                        'service_state': 'Not Found', 
                        'date_confirm_completed_service': 'Not Found',
                        'code_confirm_completed_service': 'Not Found', 
                        'date_cancel_service': 'Not Found', 
                        'code_cancel_service': 'Not Found',
                        'last_update': 'Not Found',
                        'code_last_update': 'Not Found',
                        'insertion_date': 'Not Found',
                        'code_insertion': 'Not Found',
                        'upload_photo': 'Not Found',
                        'photos': 'Not Found'
                    }

                    new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                    df = pd.concat([df, new_df_record], ignore_index=True)
                else:
                    df = pd.DataFrame(columns=['id', 'drop_off_date', 'check_up_date', 'next_check_up', 'vehicle_id', 'mileage', 'service_cost', 'service_description', 'paid', 'billing_address', 'payment_method',
                              'full_name', 'phone_number', 'email', 'tax_number', 'service_state', 'date_confirm_completed_service', 'code_confirm_completed_service',
                               'date_cancel_service', 'code_cancel_service', 'last_update', 'code_last_update', 'insertion_date', 'code_insertion',  'upload_photo', 'photos'])

                    for service in services:                                                                    
                            new_df_record = {
                                'id': service.id,
                                'drop_off_date': service.drop_off_date,
                                'check_up_date': service.check_up_date,
                                'next_check_up': service.next_check_up,
                                'vehicle_id': service.vehicle_id,
                                'mileage': service.mileage, 
                                'service_cost': service.service_cost, 
                                'service_description': service.service_description, 
                                'paid': service.paid, 
                                'billing_address': service.billing_address, 
                                'payment_method': service.payment_method,
                                'full_name': service.full_name, 
                                'phone_number': service.phone_number, 
                                'email': service.email, 
                                'tax_number': service.tax_number,
                                'service_state': service.service_state, 
                                'date_confirm_completed_service': service.date_confirm_completed_service,
                                'code_confirm_completed_service': service.code_confirm_completed_service, 
                                'date_cancel_service': service.date_cancel_service, 
                                'code_cancel_service': service.code_cancel_service,
                                'last_update': service.last_update,
                                'code_last_update': service.code_last_update,
                                'insertion_date': service.insertion_date,
                                'code_insertion': service.code_insertion,
                                'upload_photo': service.upload_photo,
                                'photos': service.photos
                            }

                            new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                            df = pd.concat([df, new_df_record], ignore_index=True)

                update_tree_data(df)

            all_services_checkbox_label = tk.Label(edit_treeview_frame, text="All Services",
                                     font=("Helvetica", 12), fg="black", bg="#d9dada")
            all_services_checkbox_label.grid(row=1, column=0, pady=5, padx=(10, 5), sticky=tk.E)
            all_services_checkbox_var = tk.BooleanVar()
            all_services_checkbox = tk.Checkbutton(edit_treeview_frame, variable=all_services_checkbox_var, command=lambda:filter_box(all_services_checkbox_var), font=("Helvetica", 12), fg="black", bg="#d9dada")
            all_services_checkbox.grid(row=1, column=1, pady=5, padx=(5, 10), sticky=tk.W)
            all_services_checkbox_var.set(1)

            paid_services_checkbox_label = tk.Label(edit_treeview_frame, text="Paid Services",
                                     font=("Helvetica", 12), fg="black", bg="#d9dada")
            paid_services_checkbox_label.grid(row=1, column=2, pady=5, padx=(10, 5), sticky=tk.E)
            paid_services_checkbox_var = tk.BooleanVar()
            paid_services_checkbox = tk.Checkbutton(edit_treeview_frame, variable=paid_services_checkbox_var, command=lambda:filter_box(paid_services_checkbox_var), font=("Helvetica", 12), fg="black", bg="#d9dada")
            paid_services_checkbox.grid(row=1, column=3, pady=5, padx=(5, 10), sticky=tk.W)

            unpaid_services_checkbox_label = tk.Label(edit_treeview_frame, text="Unpaid Services",
                                     font=("Helvetica", 12), fg="black", bg="#d9dada")
            unpaid_services_checkbox_label.grid(row=1, column=4, pady=5, padx=(10, 5), sticky=tk.E)
            unpaid_services_checkbox_var = tk.BooleanVar()
            unpaid_services_checkbox = tk.Checkbutton(edit_treeview_frame, variable=unpaid_services_checkbox_var, command=lambda:filter_box(unpaid_services_checkbox_var), font=("Helvetica", 12), fg="black", bg="#d9dada")
            unpaid_services_checkbox.grid(row=1, column=5, pady=5, padx=(5, 10), sticky=tk.W)

            search_entry = tk.Entry(edit_treeview_frame, bd=1, highlightbackground="black",  width=10)
            search_entry.grid(row=1, column=6, padx=5, pady=3)

            found_label = tk.Label(edit_treeview_frame, text="Not Found",
                                     font=("Helvetica", 12), fg="black", bg="#d9dada", width=15)
            found_label.grid(row=1, column=7, padx=5, pady=3)

            reset_button = Button(edit_treeview_frame, text="Reset", fg="black", bg="#d9dada")
            reset_button.grid(row=1, column=8, padx=5, pady=3)
            self.bind_hover_effects(reset_button)          

            # Below is the code responsible to search the databse for all the services in each one of the three possible states (In progress/Completed/Cancelled)
            cancelled_services = Service.query.filter_by(service_state="Cancelled").all()
            if len(cancelled_services) > 0:
                see_cancelled_button.config(command=lambda: self.pop_warning(new_window, ["showcancelcompletedinprogress", "Cancelled"], "showdbiteminfo") , state=NORMAL)

            completed_services = Service.query.filter_by(service_state="Completed").all()
            if len(completed_services) > 0:
                see_completed_button.config(command=lambda: self.pop_warning(new_window, ["showcancelcompletedinprogress", "Completed"], "showdbiteminfo") , state=NORMAL)

            in_progress_services = Service.query.filter_by(service_state="In progress").all()
            if len(in_progress_services) > 0:
                see_in_progress_button.config(command=lambda: self.pop_warning(new_window, ["showcancelcompletedinprogress", "In progress"], "showdbiteminfo") , state=NORMAL)

            services_check = Service.query.all()
            single_list = []
            expiring_list = []
            for service in services_check:
                current_date = datetime.now()

                date_next_check_up = datetime.strptime(str(service.next_check_up), "%Y-%m-%d")
                days_left_to_check_up = (date_next_check_up - current_date).days
                days_left_to_check_up +=1

                if days_left_to_check_up <= 10 and days_left_to_check_up >=0:
                    check_up_expiring_button.config(state=NORMAL)
                    if service.vehicle_id not in single_list:
                        single_list.append(service.vehicle_id)
                        expiring_list.append(f"License Plate: {service.vehicle_id}   Next Check-up: {service.next_check_up}")
                    else:
                        pass

            update_tree_data(df)
            treeview.pack(expand=True, fill="both")

        def check_if_photos():
            if hasattr(self, 'photo_paths'):
                see_photos_button.configure(state=tk.NORMAL)
                self.check_image_path = resource_path('resources/check.png')
                self.check_photos_image = ImageTk.PhotoImage(Image.open(self.check_image_path))
                reload_show_photos_button.configure(image=self.check_photos_image)
            else:
                see_photos_button.configure(state=tk.DISABLED)
                self.update_photos_button_image_path = resource_path('resources/update.png')
                self.update_photos_button_image = ImageTk.PhotoImage(Image.open(self.update_photos_button_image_path))
                reload_show_photos_button.configure(image=self.update_photos_button_image)

        edit_service_frame = tk.Frame(new_window)
        edit_service_frame.configure(bg="#d9dada")
        edit_service_frame.pack(pady=(0,10))


        # Function to retrieve the data of the selected client and then fills the entry boxes with the respective information
        def client_info(*args):
            try:
                cleaned_tax_number = re.sub(r'[^\w\s]', '', str(tax_num_entry.get()).lower())
                existing_client = Service.query.filter(Service.tax_number.ilike(cleaned_tax_number)).first()

                client_entries = [full_name_entry, phone_entry, email_entry, billing_address_entry, tax_num_entry]

                if existing_client:
                    for entry in client_entries:
                        entry.delete(0, tk.END)

                    full_name_entry.insert(0, str(existing_client.full_name))
                    phone_entry.insert(0, int(existing_client.phone_number))
                    email_entry.insert(0, str(existing_client.email))
                    tax_num_entry.insert(0, str(existing_client.tax_number))
                    billing_address_entry.insert(0, str(existing_client.billing_address))
                else:
                    pass

            except ValueError:
                pass

        def update_photos_button_state():
            if photo_checkbox_var.get():
                select_photos_button.config(state=NORMAL)
            else:
                select_photos_button.config(state=DISABLED)
                
        select_vehicle_button = tk.Button(edit_service_frame, text="Select Vehicle", width=20, borderwidth=1, highlightbackground="black",
                                              fg="black", bg="#d9dada")
        select_vehicle_button.grid(row=0, column=0, columnspan=2, pady=5, padx=5)
        self.bind_hover_effects(select_vehicle_button)

        select_client_button = tk.Button(edit_service_frame, text="Select Client", width=15, borderwidth=1, highlightbackground="black",
                                              fg="black", bg="#d9dada")
        select_client_button.grid(row=0, column=2, columnspan=2, pady=5, padx=5)
        self.bind_hover_effects(select_client_button)

        vehicle_services_button = tk.Button(edit_service_frame, text="Check Vehicle Services", width=20, borderwidth=1, highlightbackground="black",
                                              fg="black", bg="#d9dada", state=DISABLED)
        vehicle_services_button.grid(row=0, column=4, pady=5, padx=5)
        self.bind_hover_effects(vehicle_services_button)

        client_services_button = tk.Button(edit_service_frame, text="Check Client Services", width=20, borderwidth=1, highlightbackground="black",
                                              fg="black", bg="#d9dada", state=DISABLED)
        client_services_button.grid(row=0, column=5, pady=5, padx=5)
        self.bind_hover_effects(client_services_button)

        drop_button = tk.Button(edit_service_frame, text="Select the Drop-off Date", width=22, borderwidth=1, highlightbackground="black",
                                              fg="black", bg="#d9dada", command=lambda: self.datepicker(new_window, drop_entry, "drop", check_up_button))
        drop_button.grid(row=1, column=0, pady=5, padx=(10, 5), sticky=tk.E)
        self.bind_hover_effects(drop_button)
        drop_entry = tk.Entry(edit_service_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        drop_entry.grid(row=1, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        check_up_button = tk.Button(edit_service_frame, text="Select the Check-up Date", width=22, borderwidth=1, highlightbackground="black",
                                              fg="black", bg="#d9dada", state=DISABLED, command=lambda: self.datepicker(new_window, check_up_entry, "check-up", check_up_button, drop_entry.get(), next_check_up_entry))
        check_up_button.grid(row=2, column=0, pady=5, padx=(10, 5), sticky=tk.E)
        self.bind_hover_effects(check_up_button)
        check_up_entry = tk.Entry(edit_service_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        check_up_entry.grid(row=2, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        next_check_up_label = tk.Label(edit_service_frame, text="Next Check-up:",
                               font=("Helvetica", 10), fg="black", bg="#d9dada")
        next_check_up_label.grid(row=3, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        next_check_up_entry = tk.Entry(edit_service_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        next_check_up_entry.grid(row=3, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        vehicle_id_label = tk.Label(edit_service_frame, text="Vehicle ID:",
                               font=("Helvetica", 10), fg="black", bg="#d9dada")
        vehicle_id_label.grid(row=4, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        vehicle_id_entry = tk.Entry(edit_service_frame, bd=1, highlightbackground="black",  width=10)
        vehicle_id_entry.grid(row=4, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        mileage_label = tk.Label(edit_service_frame, text="Mileage:",
                               font=("Helvetica", 10), fg="black", bg="#d9dada")
        mileage_label.grid(row=5, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        mileage_entry = tk.Entry(edit_service_frame, bd=1, highlightbackground="black",  width=10)
        mileage_entry.grid(row=5, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        service_cost_label = tk.Label(edit_service_frame, text="Service Cost:",
                               font=("Helvetica", 10), fg="black", bg="#d9dada")
        service_cost_label.grid(row=1, column=4, pady=5, padx=(20, 5), sticky=tk.E)
        service_cost_entry = tk.Entry(edit_service_frame, bd=1, highlightbackground="black",  width=10)
        service_cost_entry.grid(row=1, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        pay_method_label = tk.Label(edit_service_frame, text="Payment-Method:",
                                 font=("Helvetica", 10), fg="black", bg="#d9dada")
        pay_method_label.grid(row=2, column=4, pady=5, padx=(10, 5), sticky=tk.E)
        pay_types = ["Not Defined", "Cash", "Credit Card", "Paypal", "Bank Transfer", "Google Pay", "Apple Pay"]
        selected_pay_type = tk.StringVar()
        pay_type_combobox = ttk.Combobox(edit_service_frame,
                                        textvariable=selected_pay_type,
                                        values=pay_types, state="readonly",  justify="center", height=4, width=10,
                                        style="TCombobox")
        pay_type_combobox.grid(row=2, column=5, pady=5, padx=(5, 10), sticky=tk.W)
        pay_type_combobox.set(pay_types[0])

        checkbox_label = tk.Label(edit_service_frame, text="Paid",
                                 font=("Helvetica", 12), fg="black", bg="#d9dada")
        checkbox_label.grid(row=3, column=4, pady=5, padx=(10, 5), sticky=tk.E)

        paid_checkbox_var = tk.BooleanVar()
        paid_checkbox = tk.Checkbutton(edit_service_frame, variable=paid_checkbox_var, font=("Helvetica", 12), fg="black", bg="#d9dada")
        paid_checkbox.grid(row=3, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        photo_checkbox_label = tk.Label(edit_service_frame, text="Upload Receipt Photos",
                                 font=("Helvetica", 12), fg="black", bg="#d9dada")
        photo_checkbox_label.grid(row=4, column=4, pady=5, padx=(10, 5), sticky=tk.E)

        photo_checkbox_var = tk.BooleanVar()
        photo_checkbox = tk.Checkbutton(edit_service_frame, variable=photo_checkbox_var, command=update_photos_button_state, font=("Helvetica", 12), fg="black", bg="#d9dada")
        photo_checkbox.grid(row=4, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        select_photos_button = tk.Button(edit_service_frame, text="Select Receipt Photos", width=20, borderwidth=1, highlightbackground="black",
                                         fg="black", bg="#d9dada", command=lambda: self.load_image(new_window))
        select_photos_button.grid(row=5, column=4, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(select_photos_button)


        def handle_photo_viewer_result(result, updated_photos):
            if result == "confirm":
                self.photo_paths = updated_photos
                if self. photo_paths == 'nan':
                    del self.photo_paths
                    check_if_photos()
            elif result == "cancel":
                print("User cancelled changes")

        updated_photos = []
        see_photos_button = tk.Button(edit_service_frame, text="See Receipt Photos", width=25, borderwidth=1, highlightbackground="black",
                                      fg="black", bg="#d9dada", state=DISABLED,
                                      command=lambda: self.photo_viewer(new_window, self.photo_paths, "Edit Mode", handle_photo_viewer_result, updated_photos))
        see_photos_button.grid(row=5, column=5, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(see_photos_button)

        update_photos_button_image_path = resource_path('resources/update.png')
        self.update_photos_button_image = ImageTk.PhotoImage(Image.open(update_photos_button_image_path))
        reload_show_photos_button = tk.Button(edit_service_frame, image=self.update_photos_button_image,
                                              command=check_if_photos, borderwidth=0, highlightthickness=0)
        reload_show_photos_button.grid(row=5, column=6, pady=5, padx=5, sticky="w")

        full_name_label = tk.Label(edit_service_frame, text="Full Name:",
                                   font=("Helvetica", 10), fg="black", bg="#d9dada")
        full_name_label.grid(row=1, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        full_name_entry = tk.Entry(edit_service_frame, bd=1, highlightbackground="black",  width=10)
        full_name_entry.grid(row=1, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        phone_label = tk.Label(edit_service_frame, text="Phone Number:",
                               font=("Helvetica", 10), fg="black", bg="#d9dada")
        phone_label.grid(row=2, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        phone_entry = tk.Entry(edit_service_frame, bd=1, highlightbackground="black",  width=10)
        phone_entry.grid(row=2, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        email_label = tk.Label(edit_service_frame, text="Email:",
                               font=("Helvetica", 10), fg="black", bg="#d9dada")
        email_label.grid(row=3, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        email_entry = tk.Entry(edit_service_frame, bd=1, highlightbackground="black",  width=10)
        email_entry.grid(row=3, column=3, pady=5, padx=(5, 10), sticky=tk.W)


        tax_num_label = tk.Label(edit_service_frame, text="Tax Number:",
                               font=("Helvetica", 10), fg="black", bg="#d9dada")
        tax_num_label.grid(row=4, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        tax_num_entry = tk.Entry(edit_service_frame, bd=1, highlightbackground="black",  width=10)
        tax_num_entry.grid(row=4, column=3, pady=5, padx=(5, 10), sticky=tk.W)
        tax_num_entry.bind("<KeyRelease>", client_info)

        billing_address_label = tk.Label(edit_service_frame, text="Billing Address:",
                                 font=("Helvetica", 10), fg="black", bg="#d9dada")
        billing_address_label.grid(row=5, column=2, pady=5, padx=(10, 5), sticky=tk.E)
        billing_address_entry = tk.Entry(edit_service_frame, bd=1, highlightbackground="black",  width=10)
        billing_address_entry.grid(row=5, column=3, pady=5, padx=(5, 10), sticky=tk.W)     
 
        service_description_label = tk.Label(edit_service_frame, text="Service Description:",
                          font=("Helvetica", 10), fg="black", bg="#d9dada")
        service_description_label.grid(row=6, column=0, pady=5, padx=5, sticky=tk.E)

        service_description_entry = tk.Entry(edit_service_frame, bd=1, highlightbackground="black",  width=50)
        service_description_entry.grid(row=6, column=1, columnspan=3, padx=(5,10), pady=5)

        get_vehicle = ["service", vehicle_id_entry, "vehicle"]
        select_vehicle_button.config(command=lambda: self.pop_warning(new_window, get_vehicle, "dbtotree"))

        get_client = ["service", tax_num_entry, "client", client_info]
        select_client_button.config(command=lambda: self.pop_warning(new_window, get_client, "dbtotree"))


        cancel_service_button = tk.Button(edit_service_frame, text="Cancel Service", width=20, borderwidth=1, highlightbackground="black",
                              fg="black", bg="#d9dada", state=DISABLED)
        cancel_service_button.grid(row=6, column=4, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(cancel_service_button)

        confirm_completed_button = tk.Button(edit_service_frame, text="Confirm Service is Completed", width=25, borderwidth=1, highlightbackground="black",
                              fg="black", bg="#d9dada", state=DISABLED)
        confirm_completed_button.grid(row=6, column=5, columnspan=2, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(confirm_completed_button)

        see_in_progress_button = tk.Button(edit_service_frame, text="Services In Progress", width=20, borderwidth=1, highlightbackground="black",
                              fg="black", bg="#d9dada", state=DISABLED)
        see_in_progress_button.grid(row=7, column=0, pady=5, padx=5)
        self.bind_hover_effects(see_in_progress_button)

        see_completed_button = tk.Button(edit_service_frame, text="Services Completed", width=20, borderwidth=1, highlightbackground="black",
                              fg="black", bg="#d9dada", state=DISABLED)
        see_completed_button.grid(row=7, column=1, pady=5, padx=5)
        self.bind_hover_effects(see_completed_button)

        see_cancelled_button = tk.Button(edit_service_frame, text="Services Cancelled", width=20, borderwidth=1, highlightbackground="black",
                              fg="black", bg="#d9dada", state=DISABLED)
        see_cancelled_button.grid(row=7, column=2, pady=5, padx=5)
        self.bind_hover_effects(see_cancelled_button)


        export_selected_button = tk.Button(edit_service_frame, text="Export Selected", width=20, borderwidth=1, highlightbackground="black",
                              fg="black", bg="#d9dada", state=DISABLED)
        export_selected_button.grid(row=7, column=4, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(export_selected_button)

        export_all_button = tk.Button(edit_service_frame, text="Export All", width=25, borderwidth=1, highlightbackground="black",
                              fg="black", bg="#d9dada", state=DISABLED)
        export_all_button.grid(row=7, column=5, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(export_all_button)

        if df is not None and not df.empty:
            create_tree_from_db(df)
        else:
            print("Database table is empty")

    # Section to see paymment records data, to update a payment record data or delete a record 
    # the user must do it to the service related to the intended record (same id) in the manage services section
    def payments_section(self, new_window):
        treeFrame = tk.Frame(new_window)
        treeFrame.pack(expand=True, fill="both")
        treeFrame.configure(bg="#d9dada")

        df_section_info = "Database table is empty"
        df_section_info_label = tk.Label(treeFrame, text=df_section_info, font=("Helvetica", 10),
                                           fg="darkred", bg="#d9dada")
        df_section_info_label.pack(pady=(140, 0))
        
        treeview_frame = tk.Frame(new_window)
        treeview_frame.pack(pady=10)
        treeview_frame.configure(bg="#d9dada")
        try:
            database_uri = self.flask_app.config['SQLALCHEMY_DATABASE_URI']
            engine = create_engine(database_uri)
            df = pd.read_sql_table("payment", con=engine)
            engine.dispose()
        except ValueError:
            print("ValueError")

        def create_tree_from_db(df):
            for widget in treeFrame.winfo_children():
                widget.destroy()

            treeScrolly = ttk.Scrollbar(treeFrame, orient="vertical")
            treeScrolly.pack(side="right", fill="y")

            treeScrollx = ttk.Scrollbar(treeFrame, orient="horizontal")
            treeScrollx.pack(side="bottom", fill="x")

            treeview = ttk.Treeview(treeFrame, show="headings",
                                    yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

            treeScrolly.config(command=treeview.yview)
            treeScrollx.config(command=treeview.xview)

            def update_tree_data(df):

                def reset():
                    all_services_checkbox_var.set(1)
                    paid_services_checkbox_var.set(0)
                    unpaid_services_checkbox_var.set(0)
                    search_entry.delete(0, tk.END)
                    found_label.config(text="Not Found", fg="black", bg="#d9dada", width=15)
                    filter_box(all_services_checkbox_var)

                def search(*args):
                    try:
                        cleaned_tax_number = re.sub(r'[^\w\s]', '', str(search_entry.get()).lower())
                        existing_client = Service.query.filter(Service.tax_number.ilike(cleaned_tax_number)).first()

                        cleaned_vehicle_id = re.sub(r'[^\w\s]', '', str(search_entry.get()).lower())
                        existing_vehicle = Service.query.filter(Service.vehicle_id.ilike(cleaned_vehicle_id)).first()

                        list_box = [all_services_checkbox_var, unpaid_services_checkbox_var, paid_services_checkbox_var]
                        if existing_client or existing_vehicle:
                            found_label.config(text="Valid", bg="darkgreen", fg="white", width=15)
                            for box in list_box:
                                if box.get() == 1:
                                    print(box)
                                    filter_box(box)
                            print("Exists")
                        else:
                            found_label.config(text="Not Found", fg="black", bg="#d9dada", width=15)
                            print("Dont exist")

                    except ValueError:
                        pass

                def export_selected():
                    selected_items = treeview.selection()
                    if len(selected_items) > 0:

                        selected_df = pd.DataFrame(columns=['id', 'Service Cost', 'Service Description', 'Payment-Method', 'Paid', 'Full Name', 'Phone Number', 'Tax Number', 'Billing Address', 
                                                          'Vehicle ID', 'Last Update', 'Code Last Update', 'Insertion Date', 'Code Insertion', 'Upload Photo','Receipt Photos'])
                        for record in selected_items: 
                            x = treeview.index(record)                                       
                            new_df_record = {
                                'id': df.at[x, 'id'],
                                'Service Cost': df.at[x, 'service_cost'],
                                'Service Description' : df.at[x, 'service_description'],
                                'Payment-Method': df.at[x, 'payment_method'],
                                'Paid': df.at[x, 'paid'],
                                'Full Name': df.at[x, 'full_name'], 
                                'Phone Number': df.at[x, 'phone_number'], 
                                'Tax Number': df.at[x, 'tax_number'], 
                                'Billing Address': df.at[x, 'billing_address'],
                                'Vehicle ID': df.at[x, 'vehicle_id'],
                                'Last Update': df.at[x, 'last_update'], 
                                'Code Last Update': df.at[x, 'code_last_update'],
                                'Insertion Date': df.at[x, 'insertion_date'],
                                'Code Insertion': df.at[x, 'code_insertion'],
                                'Upload Photo': df.at[x, 'upload_photo'],
                                'Receipt Photos': df.at[x, 'photos']
                            }

                            new_df_record = pd.DataFrame([new_df_record])  

                            selected_df = pd.concat([selected_df, new_df_record], ignore_index=True)
                        self.pop_warning(new_window, selected_df, "export")

                # Function to see the information of the client inserted in the service related to this payment
                def check_client_payments():
                    selected_items = treeview.selection()

                    if len(selected_items) > 0:
                        x = treeview.index(selected_items[0])
                        get_client = ["paymentinfo", "client", str(df.at[x, 'tax_number'])]
                        self.pop_warning(new_window, get_client, "showdbiteminfo")

                # Function to see the information of the vehicle inserted in the service related to this payment
                def check_vehicle_payments():
                    selected_items = treeview.selection()

                    if len(selected_items) > 0:
                        x = treeview.index(selected_items[0])
                        get_vehicle = ["paymentinfo", "vehicle", str(df.at[x, 'vehicle_id'])]
                        self.pop_warning(new_window, get_vehicle, "showdbiteminfo")

                def verify_data():
                    for index, row in df.iterrows():
                        not_num = []
                        must_be_number = {
                            'Service Cost': row['service_cost'],
                            'Phone Number': row['phone_number']
                        }
                        for column_num, value_num in must_be_number.items():
                            try:
                                int(value_num)
                            except ValueError:
                                not_num.append(value_num)

                        not_alpha = []
                        must_not_have_number = {
                            'Full Name': str(row['full_name']),
                            'Payment-Method': str(row['payment_method']),
                            'Paid': str(row['paid']),
                            'Upload Photo': str(row['upload_photo'])
                        }

                        for column_word, value_word in must_not_have_number.items():
                            clean_value_word = re.sub(r'[^\w\s]', '', value_word).replace(' ','')
                            if all(char.isalpha() for char in clean_value_word):
                                pass
                            else:
                                not_alpha.append(value_word)

                        is_empty = []
                        all_data = {
                            'Service Cost': row['service_cost'],
                            'Service Description': str(row['service_description']),
                            'Paid': str(row['paid']),
                            'Phone Number': row['phone_number'],
                            'Full Name': str(row['full_name']),
                            'Payment-Method': str(row['payment_method']),
                            'Vehicle ID': str(row['vehicle_id']),
                            'Billing Address': str(row['billing_address']),
                            'Tax Number': str(row['tax_number']),
                            'Upload Photo': str(row['upload_photo'])
                        }
                        for column_all, value_all in all_data.items():
                            if value_all == 'nan':
                                is_empty.append(value_all)
                            else:
                                pass

                        not_defined = []

                        errors_found = not_num, not_alpha, is_empty, not_defined

                        if str(row['upload_photo']) != 'No':
                            possible_photo_path_list = str(row['photos'])

                            self.verify_photo_path(possible_photo_path_list)
                            if len(valid_photo_paths) > 0 or len(valid_photo_type) > 0:
                                pass
                            if len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                                is_empty.append("Photos")
                  

                        if any(len(error_list) > 0 for error_list in errors_found): 
                            result_of_validation = "Error Found"
                            self.change_row_color(treeview, index, "darkred")
                        else:
                            self.change_row_color(treeview, index, "white")
                            result_of_validation = "No Error Found"

                def refresh_tree(df):
                          
                    treeview.delete(*treeview.get_children())

                    def convert_to_datetime(date_string):
                        try:
                            return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                        except ValueError:
                            return date_string

                    df['insertion_date'] = df['insertion_date'].apply(convert_to_datetime)
                    treeview["column"] = list(df)
                    treeview["show"] = "headings"

                    for column in treeview["column"]:
                        treeview.heading(column, text=column)
                        treeview.column(column, anchor="center")


                    columns_to_int = ['service_cost', 'vehicle_id', 'tax_number', 'phone_number']
                    for column in columns_to_int:
                        try:
                            df[column] = df[column].fillna(0).astype('int64')
                            df[column] = df[column].replace(0, 'nan')
                        except ValueError:
                            pass              
                       
                    df_rows = df.to_numpy().tolist()
                    for row in df_rows:
                        treeview.insert("", "end", values=row)

                    for col in treeview["columns"]:
                        heading_width = tkFont.Font().measure(treeview.heading(col)["text"])

                        try:
                            max_width = max(
                                tkFont.Font().measure(str(treeview.set(item, col)))
                                for item in treeview.get_children("")
                            )
                        except OverflowError:
                            max_width = 0 
                        
                        column_width = max(heading_width, max_width) + 20
                        
                        treeview.column(col, width=column_width, minwidth=column_width)

                    treeview.column("photos", width=120, minwidth=120)
                    treeview.update_idletasks()

                    verify_data()

                def select_record(e):
                    selected_items = treeview.selection()

                    if len(selected_items) > 0:
                        x = treeview.index(selected_items[0])

                        export_selected_button.configure(state=NORMAL)
                        check_vehicle_button.configure(state=NORMAL)
                        check_client_button.configure(state=NORMAL)
                        if str(df.at[x,'photos']) == 'nan':
                            selected_receipt_photos_button.config(state=DISABLED)
                        else:
                            selected_receipt_photos_button.config(state=NORMAL)
                    else:
                        pass

                def selected_receipt_photos():
                    selected_items = treeview.selection()
                    if len(selected_items) > 0:
                        x = treeview.index(selected_items[0])
                        photos_of_selected = str(df.at[x, "photos"])

                        if photos_of_selected.lower() != "nan":
                            self.verify_photo_path(photos_of_selected)
                            if len(valid_photo_type) > 0:
                                if len(valid_photo_paths) > 0:
                                    self.photo_viewer(new_window, valid_photo_paths, "View Mode")
                                if len(invalid_photo_paths) > 0:
                                    self.pop_warning(new_window, invalid_photo_paths,"filenotfound")
                                    self.toggle_button_colors(0, selected_receipt_photos_button)
                            print(invalid_photo_type)
                            for path in invalid_photo_type:
                                if path == "":
                                    invalid_photo_type.remove(path)
                            if len(invalid_photo_type) > 0:
                                self.pop_warning(new_window, invalid_photo_type,"invalidformat")
                                self.toggle_button_colors(0, selected_receipt_photos_button)
                        else:
                            x += 1
                            self.pop_warning(new_window, str(x), "nanselectedphoto")
                            self.toggle_button_colors(0, selected_receipt_photos_button)
                    else:
                        warning = "Must select a record to see photos"
                        self.pop_warning(new_window, warning, "noselectedtoseephotos")

                refresh_tree(df)

                check_client_button.config(command=check_client_payments)
                check_vehicle_button.config(command=check_vehicle_payments)
                export_all_button.config(command=lambda: self.pop_warning(new_window, df, "export"), state=NORMAL)
                export_selected_button.config(command=export_selected)
                selected_receipt_photos_button.config(command=selected_receipt_photos)
                reset_button.config(command=reset)

                treeview.bind("<ButtonRelease-1>", select_record)
                search_entry.bind("<KeyRelease>", search)

            selected_receipt_photos_button = Button(treeview_frame, text="See Selected Receipt Photos",
                                                    fg="black",
                                                    bg="#d9dada")
            selected_receipt_photos_button.grid(row=0, column=1, columnspan=2, padx=20, pady=3)
            self.bind_hover_effects(selected_receipt_photos_button)

            export_selected_button = tk.Button(treeview_frame, text="Export Selected Data", width=22, borderwidth=1, highlightbackground="black",
                                          fg="black", bg="#d9dada", state=DISABLED)
            export_selected_button.grid(row=0, column=4, columnspan=2, pady=15, padx=20)
            self.bind_hover_effects(export_selected_button)

            export_all_button = tk.Button(treeview_frame, text="Export All Data", width=22, borderwidth=1, highlightbackground="black",
                                          fg="black", bg="#d9dada", state=DISABLED)
            export_all_button.grid(row=0, column=6, columnspan=2, pady=15, padx=20)
            self.bind_hover_effects(export_all_button)

            def filter_box(box):
                print(box)
                filter_list = [[paid_services_checkbox_var, Service.query.filter_by(paid="Yes").all()], [unpaid_services_checkbox_var, Service.query.filter_by(paid="No").all()]]

                if search_entry.get():
                    print("search not empty")
                else:
                    print("search empty")

                current_text = found_label.cget("text")
                print(current_text)
                if current_text == 'Valid':
                    print("Button is normal")
                    content = re.sub(r'[^\w\s]', '', str(search_entry.get()).lower())
                    print(content)
                    if all_services_checkbox_var == box:
                        all_services_checkbox_var.set(1)
                        paid_services_checkbox_var.set(0)
                        unpaid_services_checkbox_var.set(0)
                        vehicle = Service.query.filter(Service.vehicle_id == content).all()
                        client = Service.query.filter(Service.tax_number == content).all()
                        if len(vehicle) > 0:
                            services = vehicle
                        elif len(client) > 0:
                            services = client
                    elif paid_services_checkbox_var == box:
                        unpaid_services_checkbox_var.set(0)
                        all_services_checkbox_var.set(0)
                        vehicle = Service.query.filter(Service.paid == "Yes", Service.vehicle_id == content).all()
                        client = Service.query.filter(Service.paid == "Yes", Service.tax_number == content).all()
                        if len(vehicle) > 0:
                            services = vehicle
                        elif len(client) > 0:
                            services = client
                        else:
                            services = 0
                    elif unpaid_services_checkbox_var == box:
                        all_services_checkbox_var.set(0)
                        paid_services_checkbox_var.set(0)
                        vehicle = Service.query.filter(Service.paid == "No", Service.vehicle_id == content).all()
                        client = Service.query.filter(Service.paid == "No", Service.tax_number == content).all()
                        if len(vehicle) > 0:
                            services = vehicle
                        elif len(client) > 0:
                            services = client
                        else:
                            services = 0
                    else:
                        all_services_checkbox_var.set(1)
                        vehicle = Service.query.filter(Service.vehicle_id == content).all()
                        client = Service.query.filter(Service.tax_number == content).all()
                        if len(vehicle) > 0:
                            services = vehicle
                        elif len(client) > 0:
                            services = client


                elif current_text == 'Not Found':
                    search_entry.delete(0, tk.END)
                    print("Button is disabled")

                    if all_services_checkbox_var == box:
                        all_services_checkbox_var.set(1)
                        services = Service.query.all()
                        paid_services_checkbox_var.set(0)
                        unpaid_services_checkbox_var.set(0)
                    elif any(b[0].get() == 1 for b in filter_list):
                        print("One box is checked")

                        for b in filter_list:
                            if b[0] != box:
                                b[0].set(0)
                            else:
                                all_services_checkbox_var.set(0)
                                services = b[1]
                    else:
                        print("No box is checked")
                        services = Service.query.all()
                        all_services_checkbox_var.set(1)



                if services == 0 or len(services) == 0:
                    df = pd.DataFrame(columns=['id', 'service_cost', 'service_description', 'payment_method', 'paid', 'full_name', 'phone_number', 'tax_number', 
                        'billing_address', 'vehicle_id', 'last_update', 'code_last_update', 'insertion_date', 'code_insertion',  'upload_photo', 'photos'])

                                                                
                    new_df_record = {
                        'id': 'Not Found',
                        'service_cost': 'Not Found', 
                        'service_description': 'Not Found',  
                        'payment_method': 'Not Found', 
                        'paid': 'Not Found',
                        'full_name': 'Not Found', 
                        'phone_number': 'Not Found', 
                        'tax_number': 'Not Found', 
                        'billing_address': 'Not Found', 
                        'vehicle_id': 'Not Found',
                        'last_update': 'Not Found',
                        'code_last_update': 'Not Found',
                        'insertion_date': 'Not Found',
                        'code_insertion': 'Not Found',
                        'upload_photo': 'Not Found',
                        'photos': 'Not Found'
                    }

                    new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                    df = pd.concat([df, new_df_record], ignore_index=True)
                else:
                    df = pd.DataFrame(columns=['id', 'service_cost', 'service_description', 'payment_method', 'paid', 'full_name', 'phone_number', 'tax_number', 
                        'billing_address', 'vehicle_id', 'last_update', 'code_last_update', 'insertion_date', 'code_insertion',  'upload_photo', 'photos'])

                    for service in services:                                                                    
                            new_df_record = {
                                'id': service.id,
                                'service_cost': service.service_cost, 
                                'service_description': service.service_description, 
                                'payment_method': service.payment_method,
                                'paid': service.paid,
                                'full_name': service.full_name, 
                                'phone_number': service.phone_number,
                                'tax_number': service.tax_number, 
                                'billing_address': service.billing_address,
                                'vehicle_id': service.vehicle_id, 
                                'last_update': service.last_update,
                                'code_last_update': service.code_last_update,
                                'insertion_date': service.insertion_date,
                                'code_insertion': service.code_insertion,
                                'upload_photo': service.upload_photo,
                                'photos': service.photos
                            }

                            new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                            df = pd.concat([df, new_df_record], ignore_index=True)

                update_tree_data(df)

            all_services_checkbox_label = tk.Label(treeview_frame, text="All Services",
                                     font=("Helvetica", 12), fg="black", bg="#d9dada")
            all_services_checkbox_label.grid(row=1, column=0, pady=5, padx=(10, 5), sticky=tk.E)
            all_services_checkbox_var = tk.BooleanVar()
            all_services_checkbox = tk.Checkbutton(treeview_frame, variable=all_services_checkbox_var, command=lambda:filter_box(all_services_checkbox_var), font=("Helvetica", 12), fg="black", bg="#d9dada")
            all_services_checkbox.grid(row=1, column=1, pady=5, padx=(5, 10), sticky=tk.W)
            all_services_checkbox_var.set(1)

            paid_services_checkbox_label = tk.Label(treeview_frame, text="Paid Services",
                                     font=("Helvetica", 12), fg="black", bg="#d9dada")
            paid_services_checkbox_label.grid(row=1, column=2, pady=5, padx=(10, 5), sticky=tk.E)
            paid_services_checkbox_var = tk.BooleanVar()
            paid_services_checkbox = tk.Checkbutton(treeview_frame, variable=paid_services_checkbox_var, command=lambda:filter_box(paid_services_checkbox_var), font=("Helvetica", 12), fg="black", bg="#d9dada")
            paid_services_checkbox.grid(row=1, column=3, pady=5, padx=(5, 10), sticky=tk.W)

            unpaid_services_checkbox_label = tk.Label(treeview_frame, text="Unpaid Services",
                                     font=("Helvetica", 12), fg="black", bg="#d9dada")
            unpaid_services_checkbox_label.grid(row=1, column=4, pady=5, padx=(10, 5), sticky=tk.E)
            unpaid_services_checkbox_var = tk.BooleanVar()
            unpaid_services_checkbox = tk.Checkbutton(treeview_frame, variable=unpaid_services_checkbox_var, command=lambda:filter_box(unpaid_services_checkbox_var), font=("Helvetica", 12), fg="black", bg="#d9dada")
            unpaid_services_checkbox.grid(row=1, column=5, pady=5, padx=(5, 10), sticky=tk.W)

            search_entry = tk.Entry(treeview_frame, bd=1, highlightbackground="black",  width=10)
            search_entry.grid(row=1, column=6, padx=5, pady=3)

            found_label = tk.Label(treeview_frame, text="Not Found",
                                     font=("Helvetica", 12), fg="black", bg="#d9dada", width=15)
            found_label.grid(row=1, column=7, padx=5, pady=3)

            reset_button = Button(treeview_frame, text="Reset", fg="black", bg="#d9dada", width=20)
            reset_button.grid(row=1, column=8, padx=5, pady=3)
            self.bind_hover_effects(reset_button) 

            update_tree_data(df)
            treeview.pack(expand=True, fill="both")



        payments_frame = tk.Frame(new_window)
        payments_frame.configure(bg="#d9dada")
        payments_frame.pack(pady=(0,10))


        check_vehicle_button = tk.Button(payments_frame, text="Check Vehicle Payments", width=20, borderwidth=1, highlightbackground="black",
                                      fg="black", bg="#d9dada", state=DISABLED)
        check_vehicle_button.grid(row=0, column=0, pady=20, padx=20, sticky="w")
        self.bind_hover_effects(check_vehicle_button)

        check_client_button = tk.Button(payments_frame, text="Check Client Payments", width=20, borderwidth=1, highlightbackground="black",
                                      fg="black", bg="#d9dada", state=DISABLED)
        check_client_button.grid(row=0, column=1, pady=20, padx=20, sticky="w")
        self.bind_hover_effects(check_client_button)


        if df is not None and not df.empty:
            create_tree_from_db(df)
        else:
            print("Database table is empty")

    # Section to see employees data
    def employees_section(self, new_window):
        treeFrame = tk.Frame(new_window)
        treeFrame.pack(expand=True, fill="both")
        treeFrame.configure(bg='#d9dada')

        df_section_info = "Database table is empty"
        df_section_info_label = tk.Label(treeFrame, text=df_section_info, font=("Helvetica", 10),
                                           fg="darkred", bg='#d9dada')
        df_section_info_label.pack(pady=(140, 0))
        
        treeview_frame = tk.Frame(new_window)
        treeview_frame.pack(pady=10)
        treeview_frame.configure(bg='#d9dada')
        try:
            database_uri = self.flask_app.config['SQLALCHEMY_DATABASE_URI']
            engine = create_engine(database_uri)
            df = pd.read_sql_table("employee", con=engine)
            df = df.drop(columns=['password'])
            engine.dispose()
        except ValueError:
            print("ValueError")

        def create_tree_from_db(df):
            for widget in treeFrame.winfo_children():
                widget.destroy()

            treeScrolly = ttk.Scrollbar(treeFrame, orient="vertical")
            treeScrolly.pack(side="right", fill="y")

            treeScrollx = ttk.Scrollbar(treeFrame, orient="horizontal")
            treeScrollx.pack(side="bottom", fill="x")

            treeview = ttk.Treeview(treeFrame, show="headings",
                                    yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

            treeScrolly.config(command=treeview.yview)
            treeScrollx.config(command=treeview.xview)

            def export_selected():
                selected_items = treeview.selection()
                if len(selected_items) > 0:

                    selected_df = pd.DataFrame(columns=['id', 'Full Name', 'Username', 'Employee Code', 'Employee Type'])
                    for record in selected_items: 
                        x = treeview.index(record)                                       
                        new_df_record = {
                            'id': df.at[x, 'id'],
                            'Full Name': df.at[x, 'full_name'],
                            'Username': df.at[x, 'username'],
                            'Employee Code': df.at[x, 'employee_code'], 
                            'Employee Type': df.at[x, 'employee_type']
                        }

                        new_df_record = pd.DataFrame([new_df_record])  

                        selected_df = pd.concat([selected_df, new_df_record], ignore_index=True)
                    self.pop_warning(new_window, selected_df, "export")


            def refresh_tree(df):
                      
                treeview.delete(*treeview.get_children())

                treeview["column"] = list(df)
                treeview["show"] = "headings"

                for column in treeview["column"]:
                    treeview.heading(column, text=column)
                    treeview.column(column, anchor="center")
           
                   
                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    treeview.insert("", "end", values=row)

                for col in treeview["columns"]:
                    heading_width = tkFont.Font().measure(treeview.heading(col)["text"])

                    try:
                        max_width = max(
                            tkFont.Font().measure(str(treeview.set(item, col)))
                            for item in treeview.get_children("")
                        )
                    except OverflowError:
                        max_width = 0 
                    
                    column_width = max(heading_width, max_width) + 20
                    
                    treeview.column(col, width=column_width, minwidth=column_width)

                treeview.update_idletasks()

            def select_record(e):
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])

                    export_selected_button.configure(state=NORMAL)
                else:
                    pass

            def remove_selected():
                selected_items = treeview.selection()
                if len(selected_items) > 0:
                    try:
                        if len(selected_items) == Employee.query.count():
                            warning = "Can not delete all the data from the Employees Database"
                            self.pop_warning(new_window, warning, "cannotdeletealldb" )
                        else:
                            for record in selected_items:
                                x = treeview.index(record)
                                employee = Employee.query.filter_by(id=int(df.at[x, 'id'])).first()
                                db.session.delete(employee)
                                db.session.commit()     
                                treeview.delete(record)
                                df.drop(index=x, inplace=True)
                                df.reset_index(drop=True, inplace=True)
                    except OperationalError as e:
                        warning = "Database is locked. Please close the Database and try again."
                        self.pop_warning(new_window, warning, "databaselocked")
                        db.session.rollback()
                        print("Database is locked. Please try again later.")
                else:
                    warning = "Must select at least one record to remove"
                    self.pop_warning(new_window, warning, "noselectedtoremove")


            refresh_tree(df)
            treeview.pack(expand=True, fill="both")

            remove_selected_button = Button(treeview_frame, text="Remove Selected Record(s)", width=22, borderwidth=1, highlightbackground="black",
                                                    fg="black",
                                                    bg='#d9dada', command=remove_selected)
            remove_selected_button.grid(row=0, column=0, padx=20, pady=3)
            self.bind_hover_effects(remove_selected_button)

            export_selected_button = tk.Button(treeview_frame, text="Export Selected Data", width=22, borderwidth=1, highlightbackground="black",
                                          fg="black", bg='#d9dada', state=DISABLED)
            export_selected_button.grid(row=0, column=1, pady=15, padx=20)
            self.bind_hover_effects(export_selected_button)

            export_all_button = tk.Button(treeview_frame, text="Export All Data", width=22, borderwidth=1, highlightbackground="black",
                                          fg="black", bg='#d9dada', state=DISABLED)
            export_all_button.grid(row=0, column=2, pady=15, padx=20)
            self.bind_hover_effects(export_all_button)
 

            treeview.bind("<ButtonRelease-1>", select_record)


            export_all_button.config(command=lambda: self.pop_warning(new_window, df, "export"), state=NORMAL)
            export_selected_button.config(command=export_selected)
            remove_selected_button.config(command=remove_selected)


        if df is not None and not df.empty:
            create_tree_from_db(df)
        else:
            print("Database table is empty")

    # Frame that is presented to the user after the login
    def show_authenticated_frame(self, authenticated_username, success_message=None):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        insert_menu = tk.Menu(menu_bar, tearoff=0)
        insert_menu.add_command(label="Insert Service",
                                command=lambda: self.create_section_window("Insert Service"))

        menu_bar.add_cascade(label="Insert", menu=insert_menu)

        manage_menu = tk.Menu(menu_bar, tearoff=0)
        manage_menu.add_command(label="Manage Services",
                                command=lambda: self.create_section_window("Manage Services"))
        menu_bar.add_cascade(label="Manage", menu=manage_menu)

        pay_menu = tk.Menu(menu_bar, tearoff=0)
        pay_menu.add_command(label="Check Payment Records", command=lambda: self.create_section_window("Payment Records"))
        menu_bar.add_cascade(label="Payments", menu=pay_menu)

        employee = Employee.query.filter_by(username=authenticated_username).first()

        employee_menu = tk.Menu(menu_bar, tearoff=0)
        employee_menu.add_command(label="Check Employees Information", command=lambda: self.create_section_window("Employees Information")
                                 if employee.employee_type == "Manager" else self.pop_warning(self.root, "Only managers can access this area", "employeesdata"))
        menu_bar.add_cascade(label="Employees", menu=employee_menu)

        head_frame = tk.Frame(self.root)
        head_frame.pack(fill=tk.BOTH, expand=True)
        head_frame.pack_propagate(False)
        head_frame.configure(bg='#d9dada')

        # Each function below is linked to its respective button in the initial dashboard and sends a string to the create_tree_info
        # the function uses the string to search the string that matches it and displays the information related to the string 
        def show_last_services():
            create_tree_info("last_services")
        def show_last_payments():
            create_tree_info("last_payments")       
        def show_not_paid():
            create_tree_info("not_paid")
        def show_month_services():
             create_tree_info("month_services")
        def show_year_services():
            create_tree_info("year_services")

        buttons = [
            ("Last Services", show_last_services),
            ("Last Payments", show_last_payments),
            ("Unpaid Services", show_not_paid),
            ("Current Month Services", show_month_services),
            ("Current Year Services", show_year_services)
        ]
        for i, (text, command) in enumerate(buttons):
            button = tk.Button(head_frame, text=text, width=20, borderwidth=1, highlightbackground="black", fg="black", bg='#d9dada',
                               command=command)
            button.grid(row=0, column=i, sticky="w")
            self.bind_hover_effects(button)

        head_frame.grid_columnconfigure(5, weight=1)  

        welcome_label = tk.Label(head_frame, text=f"You're logged in as, {authenticated_username}",
                                 font=("Helvetica", 10), fg="black", bg='#d9dada')
        welcome_label.grid(row=0, column=6, padx=5, pady=5, sticky="e")

        # Funtion that allows the user to logout 
        def logout():
            print("Cleanup tasks completed. Logging out...")
            success_message = "Logout successful!"
            self.show_main_window(authenticated=False, success_message=success_message)

        logout_button = tk.Button(head_frame, text="Logout", width=10, fg="white", bg="#800000", borderwidth=1, highlightbackground="black",
                                  command=logout)
        logout_button.grid(row=0, column=7, sticky="e")
        self.red_bind_hover_effects(logout_button)

        info_frame = tk.Frame(self.root)
        info_frame.pack(fill=tk.BOTH, expand=True)
        info_frame.configure(bg='#d9dada')

        # Function that searches for specific data inside of the database, creates a dataframe and displays it to the user using the treeview widget
        def create_tree_info(info):
            
            try:
                for widget in treeFrame.winfo_children():
                    widget.destroy()

                current_month = datetime.now().month
                current_year = datetime.now().year

                if info == "last_services":
                    last_services = Service.query.order_by(desc(Service.insertion_date)).all()

                    df = pd.DataFrame(columns=['id', 'Drop-off Date', 'Check-up Date', 'Next Check-up', 'Vehicle ID', 'Mileage', 'Service Cost', 'Service Description', 'Paid', 'Billing Address', 'Payment-Method',
                                                      'Full Name', 'Phone Number', 'Email', 'Tax Number', 'Service State', 'Date Confirm Completed Service', 'Code Confirm Completed Service',
                                                       'Date Cancel Service', 'Code Cancel Service', 'Last Update', 'Code Last Update', 'Insertion Date', 'Code Insertion',  'Upload Photo', 'Receipt Photos'])

                    for service in last_services:                                                                    
                            new_df_record = {
                                'id': service.id,
                                'Drop-off Date': service.drop_off_date,
                                'Check-up Date': service.check_up_date,
                                'Next Check-up': service.next_check_up,
                                'Vehicle ID': service.vehicle_id,
                                'Mileage': service.mileage,
                                'Service Cost': service.service_cost, 
                                'Service Description': service.service_description, 
                                'Paid': service.paid, 
                                'Billing Address': service.billing_address, 
                                'Payment-Method': service.payment_method,
                                'Full Name': service.full_name, 
                                'Phone Number': service.phone_number, 
                                'Email': service.email, 
                                'Tax Number': service.tax_number,
                                'Service State': service.service_state, 
                                'Date Confirm Completed Service': service.date_confirm_completed_service,
                                'Code Confirm Completed Service': service.code_confirm_completed_service, 
                                'Date Cancel Service': service.date_cancel_service, 
                                'Code Cancel Service': service.code_cancel_service,
                                'Last Update': service.last_update,
                                'Code Last Update': service.code_last_update,
                                'Insertion Date': service.insertion_date,
                                'Code Insertion': service.code_insertion,
                                'Upload Photo': service.upload_photo,
                                'Receipt Photos': service.photos
                            }

                            new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                            df = pd.concat([df, new_df_record], ignore_index=True)

                elif info == "last_payments":
                    last_payments = Payment.query.filter_by(paid="Yes").order_by(Payment.insertion_date.desc()).all()

                    df = pd.DataFrame(columns=['id', 'Service Cost', 'Service Description', 'Payment-Method', 'Paid', 'Full Name', 'Phone Number', 'Tax Number', 'Billing Address', 
                                                      'Vehicle ID', 'Last Update', 'Code Last Update', 'Insertion Date', 'Code Insertion', 'Upload Photo','Receipt Photos'])
                    for payment in last_payments:                                       
                        new_df_record = {
                            'id': payment.id,
                            'Service Cost': payment.service_cost,
                            'Service Description' : payment.service_description,
                            'Payment-Method': payment.payment_method,
                            'Paid': payment.paid,
                            'Full Name': payment.full_name, 
                            'Phone Number': payment.phone_number, 
                            'Tax Number': payment.tax_number, 
                            'Billing Address': payment.billing_address,
                            'Vehicle ID': payment.vehicle_id,
                            'Last Update': payment.last_update, 
                            'Code Last Update': payment.code_last_update,
                            'Insertion Date': payment.insertion_date,
                            'Code Insertion': payment.code_insertion,
                            'Upload Photo': payment.upload_photo,
                            'Receipt Photos': payment.photos
                        }

                        new_df_record = pd.DataFrame([new_df_record])  

                        df = pd.concat([df, new_df_record], ignore_index=True)

                elif info == "not_paid":
                    not_paid_services = Payment.query.filter_by(paid="No").all()

                    df = pd.DataFrame(columns=['id', 'Service Cost', 'Service Description', 'Payment-Method', 'Paid', 'Full Name', 'Phone Number', 'Tax Number', 'Billing Address', 
                                                      'Vehicle ID', 'Last Update', 'Code Last Update', 'Insertion Date', 'Code Insertion', 'Upload Photo','Receipt Photos'])
                    for payment in not_paid_services:                                       
                        new_df_record = {
                            'id': payment.id,
                            'Service Cost': payment.service_cost,
                            'Service Description' : payment.service_description,
                            'Payment-Method': payment.payment_method,
                            'Paid': payment.paid,
                            'Full Name': payment.full_name, 
                            'Phone Number': payment.phone_number, 
                            'Tax Number': payment.tax_number, 
                            'Billing Address': payment.billing_address,
                            'Vehicle ID': payment.vehicle_id,
                            'Last Update': payment.last_update, 
                            'Code Last Update': payment.code_last_update,
                            'Insertion Date': payment.insertion_date,
                            'Code Insertion': payment.code_insertion,
                            'Upload Photo': payment.upload_photo,
                            'Receipt Photos': payment.photos
                        }

                        new_df_record = pd.DataFrame([new_df_record])  

                        df = pd.concat([df, new_df_record], ignore_index=True)

                elif info == "month_services":
                    current_month_services = Service.query.filter(
                        extract('month', Service.insertion_date) == current_month,
                        extract('year', Service.insertion_date) == current_year,
                        Service.service_state != 'Cancelled').all()

                    df = pd.DataFrame(columns=['id', 'Drop-off Date', 'Check-up Date', 'Next Check-up', 'Vehicle ID', 'Mileage', 'Service Cost', 'Service Description', 'Paid', 'Billing Address', 'Payment-Method',
                                                      'Full Name', 'Phone Number', 'Email', 'Tax Number', 'Service State', 'Date Confirm Completed Service', 'Code Confirm Completed Service',
                                                       'Date Cancel Service', 'Code Cancel Service', 'Last Update', 'Code Last Update', 'Insertion Date', 'Code Insertion',  'Upload Photo', 'Receipt Photos'])

                    for service in current_month_services:                                                                    
                            new_df_record = {
                                'id': service.id,
                                'Drop-off Date': service.drop_off_date,
                                'Check-up Date': service.check_up_date,
                                'Next Check-up': service.next_check_up,
                                'Vehicle ID': service.vehicle_id,
                                'Mileage': service.mileage, 
                                'Service Cost': service.service_cost, 
                                'Service Description': service.service_description, 
                                'Paid': service.paid, 
                                'Billing Address': service.billing_address, 
                                'Payment-Method': service.payment_method,
                                'Full Name': service.full_name, 
                                'Phone Number': service.phone_number, 
                                'Email': service.email, 
                                'Tax Number': service.tax_number,
                                'Service State': service.service_state, 
                                'Date Confirm Completed Service': service.date_confirm_completed_service,
                                'Code Confirm Completed Service': service.code_confirm_completed_service, 
                                'Date Cancel Service': service.date_cancel_service, 
                                'Code Cancel Service': service.code_cancel_service,
                                'Last Update': service.last_update,
                                'Code Last Update': service.code_last_update,
                                'Insertion Date': service.insertion_date,
                                'Code Insertion': service.code_insertion,
                                'Upload Photo': service.upload_photo,
                                'Receipt Photos': service.photos
                            }

                            new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                            df = pd.concat([df, new_df_record], ignore_index=True)

                elif info == "year_services":
                    current_year_services = Service.query.filter(
                        extract('year', Service.insertion_date) == current_year,
                        Service.service_state != 'Cancelled').all()

                    df = pd.DataFrame(columns=['id', 'Drop-off Date', 'Check-up Date', 'Next Check-up', 'Vehicle ID', 'Mileage', 'Service Cost', 'Service Description', 'Paid', 'Billing Address', 'Payment-Method',
                                                      'Full Name', 'Phone Number', 'Email', 'Tax Number', 'Service State', 'Date Confirm Completed Service', 'Code Confirm Completed Service',
                                                       'Date Cancel Service', 'Code Cancel Service', 'Last Update', 'Code Last Update', 'Insertion Date', 'Code Insertion',  'Upload Photo', 'Receipt Photos'])

                    for service in current_year_services:                                                                    
                            new_df_record = {
                                'id': service.id,
                                'Drop-off Date': service.drop_off_date,
                                'Check-up Date': service.check_up_date,
                                'Next Check-up': service.next_check_up,
                                'Vehicle ID': service.vehicle_id,
                                'Mileage': service.mileage, 
                                'Service Cost': service.service_cost, 
                                'Service Description': service.service_description, 
                                'Paid': service.paid, 
                                'Billing Address': service.billing_address, 
                                'Payment-Method': service.payment_method,
                                'Full Name': service.full_name, 
                                'Phone Number': service.phone_number, 
                                'Email': service.email, 
                                'Tax Number': service.tax_number,
                                'Service State': service.service_state, 
                                'Date Confirm Completed Service': service.date_confirm_completed_service,
                                'Code Confirm Completed Service': service.code_confirm_completed_service, 
                                'Date Cancel Service': service.date_cancel_service, 
                                'Code Cancel Service': service.code_cancel_service,
                                'Last Update': service.last_update,
                                'Code Last Update': service.code_last_update,
                                'Insertion Date': service.insertion_date,
                                'Code Insertion': service.code_insertion,
                                'Upload Photo': service.upload_photo,
                                'Receipt Photos': service.photos
                            }

                            new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                            df = pd.concat([df, new_df_record], ignore_index=True)


                if len(df) > 0:
                    for widget in treeFrame.winfo_children():
                        widget.destroy()

                    treeScrolly = ttk.Scrollbar(treeFrame, orient="vertical")
                    treeScrolly.pack(side="right", fill="y")

                    treeScrollx = ttk.Scrollbar(treeFrame, orient="horizontal")
                    treeScrollx.pack(side="bottom", fill="x")

                    treeview = ttk.Treeview(treeFrame, show="headings",
                                            yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

                    treeScrolly.config(command=treeview.yview)
                    treeScrollx.config(command=treeview.xview)

                    def convert_to_datetime(date_string):
                        try:
                            return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                        except ValueError:
                            return date_string

                    column_list = df.columns.tolist()

                    if 'Next Check-up' in column_list:
                        df['Check-up Date'] = df['Check-up Date'].apply(convert_to_datetime)
                        df['Drop-off Date'] = df['Drop-off Date'].apply(convert_to_datetime)
                        df['Next Check-up'] = df['Next Check-up'].apply(convert_to_datetime)
                        df['Insertion Date'] = df['Insertion Date'].apply(convert_to_datetime)
                        photo_col = "Receipt Photos"
                        columns_to_int = ['Service Cost', 'Vehicle ID', 'Tax Number', 'Phone Number']
                    else:
                        df['Insertion Date'] = df['Insertion Date'].apply(convert_to_datetime)
                        photo_col = "Receipt Photos"
                        columns_to_int = ['Service Cost', 'Vehicle ID', 'Tax Number', 'Phone Number']

                    def grab_photo_path(e):
                        global photos
                        selected_items = treeview.selection()
                        if len(selected_items) > 0:
                            x = treeview.index(selected_items[0])


                            if df.at[x, photo_col] != 'nan':
                                paths = df.at[x, photo_col]
                                photos = paths.split(',')
                                verify_photo_button.config(state=NORMAL)
                            else:
                                verify_photo_button.config(state=DISABLED)

                    treeview["column"] = column_list
                    treeview["show"] = "headings"

                    for column in treeview["column"]:
                        treeview.heading(column, text=column)
                        treeview.column(column, anchor="center")

                    for column in columns_to_int:
                        try:
                            df[column] = df[column].fillna(0).astype('int64')
                            df[column] = df[column].replace(0, 'nan')
                        except ValueError:
                            pass             
                       
                    df_rows = df.to_numpy().tolist()
                    for row in df_rows:
                        treeview.insert("", "end", values=row)

                    for col in treeview["columns"]:
                        heading_width = tkFont.Font().measure(treeview.heading(col)["text"])

                        max_width = max(
                            tkFont.Font().measure(str(treeview.set(item, col)))
                            for item in treeview.get_children("")
                        )
                        
                        column_width = max(heading_width, max_width) + 20 
                        treeview.column(col, width=column_width, minwidth=heading_width)

                    treeview.column(photo_col, width=120, minwidth=120)

                    treeview.pack(expand=True, fill="both")

                    verify_photo_frame = tk.Frame(treeFrame)
                    verify_photo_frame.pack(pady=(15,5), expand=True, fill="both")
                    verify_photo_frame.configure(bg='#d9dada')

                    verify_photo_button = Button(verify_photo_frame, text="Verify Photos of Selected", fg="black",
                                                   bg='#d9dada', width=20, state=DISABLED, command=lambda: self.photo_viewer(self.root, photos, "View Mode"))
                    verify_photo_button.pack(side="right", padx=5)

                    treeview.bind("<ButtonRelease-1>", grab_photo_path)                                  
                else:
                    df_section_info = "0 items matched the search"
                    df_section_info_label = tk.Label(treeFrame, text=df_section_info, font=("Helvetica", 18),
                                                       fg="darkred", bg='#d9dada')
                    df_section_info_label.pack(ipady=(140))
                    pass

            except Exception as e:
                df_section_info = "Database table is empty"
                df_section_info_label = tk.Label(treeFrame, text=df_section_info, font=("Helvetica", 18),
                                                   fg="darkred", bg='#d9dada')
                df_section_info_label.pack(ipady=(140))
                pass



        treeFrame = tk.Frame(info_frame)
        treeFrame.pack()

        df_section_info = "Database table is empty"
        df_section_info_label = tk.Label(treeFrame, text=df_section_info, font=("Helvetica", 18),
                                           fg="darkred", bg='#d9dada')
        df_section_info_label.pack(ipady=(140))

        info_section_frame = tk.Frame(info_frame)
        info_section_frame.pack()
        info_section_frame.configure(bg='#d9dada')

        num_clients_label = tk.Label(info_section_frame, text="Number of clients:",
                                   font=("Helvetica", 10), fg="black", bg='#d9dada')
        num_clients_label.grid(row=0, column=0, pady=(10,5), padx=5, sticky=tk.E)
        num_clients_entry = tk.Entry(info_section_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        num_clients_entry.grid(row=0, column=1, pady=(10,5), padx=(5, 10), sticky=tk.W)

        num_vehicles_label = tk.Label(info_section_frame, text="Number of vehicles:",
                                   font=("Helvetica", 10), fg="black", bg='#d9dada')
        num_vehicles_label.grid(row=1, column=0, pady=5, padx=5, sticky=tk.E)
        num_vehicles_entry = tk.Entry(info_section_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        num_vehicles_entry.grid(row=1, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        num_services_label = tk.Label(info_section_frame, text="Total number of services:",
                                   font=("Helvetica", 10), fg="black", bg='#d9dada')
        num_services_label.grid(row=0, column=2, pady=5, padx=5, sticky=tk.E)
        num_services_entry = tk.Entry(info_section_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        num_services_entry.grid(row=0, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        num_services_month_label = tk.Label(info_section_frame, text="Number of current month services:",
                                   font=("Helvetica", 10), fg="black", bg='#d9dada')
        num_services_month_label.grid(row=1, column=2, pady=(10,5), padx=5, sticky=tk.E)
        num_services_month_entry = tk.Entry(info_section_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        num_services_month_entry.grid(row=1, column=3, pady=(10,5), padx=(5, 10), sticky=tk.W)

        num_services_year_label = tk.Label(info_section_frame, text="Number of current year services:",
                                   font=("Helvetica", 10), fg="black", bg='#d9dada')
        num_services_year_label.grid(row=2, column=2, pady=5, padx=5, sticky=tk.E)
        num_services_year_entry = tk.Entry(info_section_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        num_services_year_entry.grid(row=2, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        amount_services_cancelled_label = tk.Label(info_section_frame, text="Cancelled services:",
                                   font=("Helvetica", 10), fg="black", bg='#d9dada')
        amount_services_cancelled_label.grid(row=3, column=2, pady=5, padx=5, sticky=tk.E)
        amount_services_cancelled_entry = tk.Entry(info_section_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        amount_services_cancelled_entry.grid(row=3, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        amount_services_completed_label = tk.Label(info_section_frame, text="Completed services:",
                                   font=("Helvetica", 10), fg="black", bg='#d9dada')
        amount_services_completed_label.grid(row=4, column=2, pady=5, padx=5, sticky=tk.E)
        amount_services_completed_entry = tk.Entry(info_section_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        amount_services_completed_entry.grid(row=4, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        amount_services_in_progress_label = tk.Label(info_section_frame, text="Services in progress:",
                                   font=("Helvetica", 10), fg="black", bg='#d9dada')
        amount_services_in_progress_label.grid(row=5, column=2, pady=5, padx=5, sticky=tk.E)
        amount_services_in_progress_entry = tk.Entry(info_section_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        amount_services_in_progress_entry.grid(row=5, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        num_paid_services_label = tk.Label(info_section_frame, text="Number of paid services:",
                                   font=("Helvetica", 10), fg="black", bg='#d9dada')
        num_paid_services_label.grid(row=0, column=4, pady=5, padx=5, sticky=tk.E)
        num_paid_services_entry = tk.Entry(info_section_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        num_paid_services_entry.grid(row=0, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        num_not_paid_services_label = tk.Label(info_section_frame, text="Number of unpaid services:",
                                   font=("Helvetica", 10), fg="black", bg='#d9dada')
        num_not_paid_services_label.grid(row=1, column=4, pady=5, padx=5, sticky=tk.E)
        num_not_paid_services_entry = tk.Entry(info_section_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        num_not_paid_services_entry.grid(row=1, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        month_revenue_label = tk.Label(info_section_frame, text="Current month revenue:",
                                   font=("Helvetica", 10), fg="black", bg='#d9dada')
        month_revenue_label.grid(row=2, column=4, pady=5, padx=5, sticky=tk.E)
        month_revenue_entry = tk.Entry(info_section_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        month_revenue_entry.grid(row=2, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        year_revenue_label = tk.Label(info_section_frame, text="Current year revenue:",
                                   font=("Helvetica", 10), fg="black", bg='#d9dada')
        year_revenue_label.grid(row=3, column=4, pady=5, padx=5, sticky=tk.E)
        year_revenue_entry = tk.Entry(info_section_frame, bd=1, highlightbackground="black",  width=10, state="readonly", readonlybackground="white")
        year_revenue_entry.grid(row=3, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        # Function responsible to gather the data to populate the initial dashboard
        def refresh_data():
            services = Service.query.all()

            check_list = []
            client_list = []
            vehicle_list = []
            for service in services:
                print(service)
                if service.tax_number not in check_list:
                    check_list.append(service.tax_number)
                    client_list.append(service)
                if service.vehicle_id not in check_list:
                    check_list.append(service.vehicle_id)
                    vehicle_list.append(service)

            current_month = datetime.now().month
            current_year = datetime.now().year

            current_month_services = Service.query.filter(
                extract('month', Service.insertion_date) == current_month,
                extract('year', Service.insertion_date) == current_year,
                Service.service_state != 'Cancelled'
            ).all()

            current_month_paid = Service.query.filter(
                extract('month', Service.insertion_date) == current_month,
                extract('year', Service.insertion_date) == current_year,
                Service.paid == 'Yes'
            ).all()

            total_revenue_current_month = sum(service.service_cost for service in current_month_paid)

            current_year_services = Service.query.filter(
                extract('year', Service.insertion_date) == current_year,
                Service.service_state != 'Cancelled'
            ).all()

            current_year_paid = Service.query.filter(
                extract('year', Service.insertion_date) == current_year,
                Service.paid == 'Yes'
            ).all()

            total_revenue_current_year = sum(service.service_cost for service in current_year_paid)
            cancelled_services = Service.query.filter(Service.service_state == 'Cancelled').all()
            completed_services = Service.query.filter(Service.service_state == 'Completed').all()
            in_progress_services = Service.query.filter(Service.service_state == 'In progress').all()
            paid_services = Service.query.filter_by(paid="Yes").all()
            not_paid_services = Service.query.filter_by(paid="No").all()

            read_only = [num_clients_entry, num_vehicles_entry, month_revenue_entry, year_revenue_entry, amount_services_cancelled_entry,
            amount_services_completed_entry, amount_services_in_progress_entry, num_services_entry, num_services_month_entry, num_services_year_entry,
            num_paid_services_entry, num_not_paid_services_entry]

            for entry in read_only:
                entry.config(state=tk.NORMAL)
                entry.delete(0, END)

            num_clients_entry.insert(0, len(client_list))
            num_vehicles_entry.insert(0, len(vehicle_list))
            month_revenue_entry.insert(0, total_revenue_current_month)
            year_revenue_entry.insert(0, total_revenue_current_year)
            amount_services_cancelled_entry.insert(0, len(cancelled_services))
            amount_services_completed_entry.insert(0, len(completed_services))
            amount_services_in_progress_entry.insert(0, len(in_progress_services))
            num_not_paid_services_entry.insert(0, len(not_paid_services))
            num_services_entry.insert(0, len(services))
            num_paid_services_entry.insert(0, len(paid_services))
            num_services_year_entry.insert(0, len(current_year_services))
            num_services_month_entry.insert(0, len(current_month_services))

            for entry in read_only:
                entry.config(state="readonly")

        refresh_data_button = tk.Button(info_section_frame, text="Refresh Data", width=12, borderwidth=1, highlightbackground="black", fg="black", bg='#d9dada',
                                  command=refresh_data)
        refresh_data_button.grid(row=6, column=2, columnspan=2, pady=(10,5), padx=5)
        self.bind_hover_effects(refresh_data_button)

        refresh_data()
        show_last_services()

    # Frame that is presented to the user that allows to logon, also shown after the log out
    def show_non_authenticated_frame(self, error_message=None, success_message=None):
        button_text = "Add new user"
        button_command = self.new_employee
        add_user_button = tk.Button(self.root, text=button_text, command=button_command, fg="black", bg="#d9dada", borderwidth=1, highlightbackground="black")
        add_user_button.pack(side=tk.TOP, anchor=tk.NE, pady=(20, 0), padx=(0, 20))
        self.bind_hover_effects(add_user_button)

        label_text = "Auto Repair"
        label_font = ("Times New Roman", 30)
        label_logo = tk.Label(self.root, text=label_text, font=label_font, fg="black", background="#d9dada")
        label_logo.pack(expand=True, pady=(30, 20))

        username_label = tk.Label(self.root, text="Username:", fg="black", background="#d9dada")
        username_label.pack(side=tk.TOP, padx=10, pady=2)
        username_entry = Entry(self.root, width=35, bd=1, highlightbackground="black")
        username_entry.pack(side=tk.TOP, pady=2)

        password_label = tk.Label(self.root, text="Password:", fg="black", background="#d9dada")
        password_label.pack(side=tk.TOP, padx=10, pady=(10, 2))
        password_entry = Entry(self.root, show="*", width=35, bd=1, highlightbackground="black")
        password_entry.pack(side=tk.TOP, pady=2)

        # Function that allows the user to login
        def login():
            try:
                existing_user = Employee.query.filter(Employee.username.ilike(username_entry.get())).first()

                if existing_user:
                    user_password = existing_user.password
                    if bcrypt.check_password_hash(user_password, password_entry.get()):
                        authenticated_username = existing_user.username
                        self.show_main_window(authenticated=True, authenticated_username=authenticated_username,
                                              success_message="User logged in successfully!")
                    else:
                        self.show_main_window(authenticated=False, error_message="Incorrect Password")
                else:
                    self.show_main_window(authenticated=False, error_message="Invalid Username")
            except Exception as e:
                print(e)


        login_button = tk.Button(self.root, text="Login", command=login, width=15, fg="white", bg="#004d00", borderwidth=1, highlightbackground="black")
        login_button.pack(side=tk.TOP, pady=(20, 130))
        self.green_bind_hover_effects(login_button)


        error_label = tk.Label(self.root, text=error_message or "", foreground="red", background="#d9dada",
                               font=("Helvetica", 12))
        error_label.pack(side=tk.TOP, pady=(0, 10))

        if success_message:
            success_label = tk.Label(self.root, text=success_message, font=("Helvetica", 12),
                                     fg="green", bg="#d9dada")
            success_label.pack(side=tk.TOP, pady=(0, 10))
            self.root.after(3000, lambda: success_label.destroy())

    # Main window of the program, that will display the 'show_non_authenticated_frame' before the login and the 'show_authenticated_frame' after the login
    def show_main_window(self, authenticated=False, authenticated_username=None, success_message=None, error_message=None):
        for widget in self.root.winfo_children():
            widget.destroy()

        with self.flask_app.app_context():
            db.create_all()

        self.canvas.destroy()
        self.root.withdraw()
        self.root.overrideredirect(False)
        self.root.title("Auto Repair")
        self.root.resizable(1, 1)
        self.root.iconphoto(True, PhotoImage(file=resource_path('resources/ar.png')))
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.deiconify()

        # Check if the user is authenticated or not, the window content will be different for each situation
        if authenticated:
            self.show_authenticated_frame(authenticated_username, success_message)
        else:
            self.show_non_authenticated_frame(error_message, success_message)

# Check if this module is being run as the main program
if __name__ == '__main__':
    root = tk.Tk() # Create a Tkinter root window
    style = ttk.Style(root) # Create a style object for customizing widgets
    root.tk.call("source", resource_path("azure.tcl")) # Load custom theme from 'forest-dark.tcl' file
    root.tk.call("set_theme", "light")
    Arepair_app = Arepair(root, app) 
    root.mainloop() # Start the Tkinter event loop to display the GUI
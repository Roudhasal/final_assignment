import tkinter as tk  # Importing tkinter module to create graphical user interfaces (GUIs)
from tkinter import messagebox, simpledialog  # Importing additional tkinter features for message boxes and simple input dialogs
import pickle  # Importing pickle to store and retrieve user data
import os  # Importing os to interact with the operating system e.g check file existence
import re  # Importing regular expressions (for handling patterns in strings, though not used in this part)

# Define the main class for the ticket booking system
class TicketBookingSystem:
    def __init__(self):
        self.users_file = "users.pkl"  # Define the file name to store user data
        self.current_user = None  # Variable to hold the currently logged in user (if any)
        self.guest = Guest(self)  # Create a guest object that handles user sign up/login
        self.admin = Admin(self)  # Create an admin object for admin-specific tasks
        self.ticket = Ticket(self)  # Create a ticket object to handle ticket-related operations

    def create_main_menu(self):
        main_menu = tk.Tk()  # Create the main window of the application
        main_menu.title("Adventure Land Theme Park Ticket Booking System")  # Set the window title
        main_menu.geometry("600x400")  # Set the window size (width: 600px, height: 400px)
        main_menu.config(bg="#F4A261")  # Set a background color for the window

        # Title label at the top of the window
        title_label = tk.Label(main_menu, text="Adventure Land Ticketing System", 
                               font=("Helvetica", 24, "bold"), bg="#F4A261", fg="#264653")  # Set font and colors
        title_label.pack(pady=20)  # Pack the label and add some padding around it

        # Button to trigger the user sign up process
        sign_up_button = tk.Button(main_menu, text="Sign Up", width=20, height=2, font=("Arial", 14), 
                                   bg="#2A9D8F", fg="white", command=self.guest.sign_up)  # Button style and action
        sign_up_button.pack(pady=10)  # Pack the button and add some padding around it

        # Button to trigger the user login process
        login_button = tk.Button(main_menu, text="Login", width=20, height=2, font=("Arial", 14), 
                                 bg="#E76F51", fg="white", command=self.guest.login)  # Button style and action
        login_button.pack(pady=10)  # Pack the button and add some padding around it

        # Button to access the admin dashboard
        admin_button = tk.Button(main_menu, text="Admin Dashboard", width=20, height=2, font=("Arial", 14), 
                                 bg="#264653", fg="white", command=self.admin.admin_dashboard)  # Button style and action
        admin_button.pack(pady=10)  # Pack the button and add some padding around it

        # Button to exit the system and close the application
        exit_button = tk.Button(main_menu, text="Exit System", width=20, height=2, font=("Arial", 14), 
                                bg="#D9BF77", fg="white", command=main_menu.quit)  # Button style and action
        exit_button.pack(pady=10)  # Pack the button and add some padding around it

        main_menu.mainloop()  # Start the main event loop to keep the GUI running and responsive

class Admin:
    def __init__(self, system):
        self.system = system  # Save the reference to the main system object (TicketBookingSystem) for future use

    def admin_dashboard(self):
        # Create a new top-level window for the admin dashboard
        dashboard_window = tk.Toplevel()
        dashboard_window.title("Admin Dashboard")  # Set the title of the dashboard window
        dashboard_window.geometry("600x400")  # Set the size of the dashboard window (600px width, 400px height)
        dashboard_window.config(bg="#F4A261")  # Set the background color of the dashboard window

        # Label to display the dashboard heading
        label = tk.Label(dashboard_window, text="Admin Dashboard", font=("Helvetica", 18), bg="#F4A261", fg="#264653")
        label.pack(pady=20)  # Pack the label and add padding above and below the text

        # Button to allow the admin to view ticket sales
        sales_button = tk.Button(dashboard_window, text="View Ticket Sales", width=20, height=2, font=("Arial", 14), 
                                 bg="#2A9D8F", fg="white", command=self.view_ticket_sales)  # Button style and action
        sales_button.pack(pady=10)  # Pack the button and add padding around it

        # New button to allow the admin to view all users in the system
        view_users_button = tk.Button(dashboard_window, text="View All Users", width=20, height=2, font=("Arial", 14), 
                                      bg="yellow", fg="white", command=self.view_all_users)  # Button style and action
        view_users_button.pack(pady=10)  # Pack the button and add padding around it

        # Button to close the admin dashboard window and exit the dashboard
        exit_button = tk.Button(dashboard_window, text="Exit Dashboard", width=20, height=2, font=("Arial", 14), 
                                bg="#264653", fg="white", command=dashboard_window.destroy)  # Button style and action
        exit_button.pack(pady=10)  # Pack the button and add padding around it

    def view_all_users(self):
        # Step 1: Load users from 'users.pkl'
        if not self._file_exists('users.pkl'):  # Check if the file exists
            messagebox.showinfo("No Users Found", "No users found in the system.")  # Show info message if no file
            return  # Exit the function if the file doesn't exist

        try:
            with open('users.pkl', 'rb') as f:  # Open the file in read-binary mode
                users = []
                while True:  # Load all user data from the file
                    try:
                        user = pickle.load(f)  # Load one user at a time
                        users.append(user)  # Add user to the list
                    except EOFError:  # Stop when the end of the file is reached
                        break

            if not users or not users[0]:  # Check if the list is empty
                messagebox.showinfo("No Users Found", "No users found in the system.")  # Inform if no users
                return

            # Access the first element in the list, which holds the user data
            user_data = users[0]  # Assume user data is stored in the first element as a list of dictionaries

            # Step 2: Create a new window to show the list of users
            users_window = tk.Toplevel()  # Create a new top-level window
            users_window.title("View and Delete Users")  # Set the title of the window
            users_window.geometry("600x400")  # Set the size of the window
            users_window.config(bg="#F4A261")  # Set the background color

            label = tk.Label(users_window, text="Select a User to Delete", font=("Helvetica", 18), bg="#F4A261", fg="#264653")
            label.pack(pady=20)  # Add a label to the window with padding

            user_listbox = tk.Listbox(users_window, width=50, height=10, font=("Arial", 14))  # Create a listbox to display users
            user_listbox.pack(pady=20)  # Add padding around the listbox

            # Add each user's name and email to the listbox
            for idx, user in enumerate(user_data):
                print(f"Adding user {user['name']} - Email: {user['email']}")  # Debugging: Print user details
                user_listbox.insert(tk.END, f"Name: {user['name']}, Email: {user['email']}")  # Add to listbox

            # Step 3: Button to delete selected user
            def delete_user():
                selected_user_index = user_listbox.curselection()  # Get the index of the selected user
                if not selected_user_index:  # Check if no user is selected
                    messagebox.showerror("Error", "Please select a user to delete.")  # Show error message
                    return

                selected_user_index = selected_user_index[0]  # Extract the index
                selected_user = user_data[selected_user_index]  # Get the selected user details

                # Step 4: Remove the user from 'users.pkl'
                self.delete_user_from_users(selected_user['email'])

                # Step 5: Remove the user's purchase history
                self.delete_user_purchase_history(selected_user['email'])

                # Custom success pop-up message
                self.show_success_popup(f"User {selected_user['name']} with email {selected_user['email']} has been deleted.")

                users_window.destroy()  # Close the users window after deletion

            # Button to trigger the delete user function
            delete_button = tk.Button(users_window, text="Delete User", width=20, height=2, font=("Arial", 14), bg="#E63946", fg="white", command=delete_user)
            delete_button.pack(pady=20)  # Add padding for the delete button

        except Exception as e:  # Catch any unexpected errors
            messagebox.showerror("Error", f"An error occurred: {e}")  # Show error message
            print("Error occurred in view_all_users:", e)  # Print error details for debugging

    def delete_user_from_users(self, email):
        # Delete a user from 'users.pkl' using their email
        try:
            with open('users.pkl', 'rb') as f:  # Open the file in read-binary mode
                users = []
                while True:  # Load all user data
                    try:
                        user = pickle.load(f)  # Load one user at a time
                        users.append(user)
                    except EOFError:  # Stop when the end of the file is reached
                        break

            if not users or not users[0]:  # Check if no users are found
                messagebox.showerror("Error", "No users found in the system.")  # Show error message
                return

            user_data = users[0]  # Assume user data is in the first element as a list of dictionaries

            # Filter out the user with the matching email
            user_data = [user for user in user_data if user['email'] != email]

            # Save the updated list back to 'users.pkl'
            with open('users.pkl', 'wb') as f:  # Open the file in write-binary mode
                for user in user_data:  # Save each user back to the file
                    pickle.dump(user, f)

        except Exception as e:  # Catch any unexpected errors
            messagebox.showerror("Error", f"Failed to delete user from 'users.pkl': {e}")  # Show error message
            print("Error occurred in delete_user_from_users:", e)  # Print error details for debugging

    def delete_user_purchase_history(self, email):
        # Delete a user's purchase history using their email
        try:
            with open('purchase_history.pkl', 'rb') as f:  # Open the purchase history file in read-binary mode
                purchases = []
                while True:  # Load all purchase data
                    try:
                        purchase = pickle.load(f)  # Load one purchase at a time
                        purchases.append(purchase)
                    except EOFError:  # Stop when the end of the file is reached
                        break

            # Filter out purchases with the matching email
            purchases = [purchase for purchase in purchases if purchase['user_email'] != email]

            # Save the updated list back to 'purchase_history.pkl'
            with open('purchase_history.pkl', 'wb') as f:  # Open the file in write-binary mode
                for purchase in purchases:  # Save each purchase back to the file
                    pickle.dump(purchase, f)

        except Exception as e:  # Catch any unexpected errors
            messagebox.showerror("Error", f"Failed to delete purchase history from 'purchase_history.pkl': {e}")  # Show error message
            print("Error occurred in delete_user_purchase_history:", e)  # Print error details for debugging

        def show_success_popup(self, message):
            # Create a custom success pop-up window to display a success message
            success_popup = tk.Toplevel()  # Create a new top-level window for the success pop-up
            success_popup.title("Success!")  # Set the title of the success pop-up window
            success_popup.geometry("400x200")  # Set the size of the pop-up window
            success_popup.config(bg="#2A9D8F")  # Set the background color of the window

            label = tk.Label(success_popup, text=message, font=("Helvetica", 16), bg="#2A9D8F", fg="white")  # Create a label with the message
            label.pack(pady=40)  # Pack the label into the window with padding

            close_button = tk.Button(success_popup, text="Close", width=15, height=2, font=("Arial", 14), bg="#E76F51", fg="white", command=success_popup.destroy)  # Create a button to close the pop-up
            close_button.pack(pady=10)  # Pack the close button with some padding

    def _file_exists(self, file_name):
        # Helper function to check if a file exists in the filesystem
        return os.path.exists(file_name)  # Return True if the file exists, False otherwise

    def view_ticket_sales(self):
        # Define the available ticket types
        ticket_types = [
            "Single Day Pass",
            "Two-Day Pass",
            "Annual Membership",
            "Child Ticket",
            "Group Ticket (10+)",
            "VIP Experience Pass"
        ]
        
        # Initialize a dictionary to count the sales of each ticket type
        ticket_sales_count = {ticket: 0 for ticket in ticket_types}  # Initialize counts to 0 for each ticket type

        try:
            # Open and read the purchase history file ('purchase_history.pkl') to gather ticket sales data
            with open('purchase_history.pkl', 'rb') as f:  # Open the file in read-binary mode
                purchases = []  # List to hold all the purchase records
                while True:  # Loop to read all purchases
                    try:
                        purchase = pickle.load(f)  # Load one purchase record at a time
                        purchases.append(purchase)  # Append the purchase to the list
                        # Debugging: Print purchase data for understanding
                        print(purchase)  # Helps in checking the structure of the data
                    except EOFError:  # End of file reached
                        break  # Exit the loop when no more data to read

            # Count how many times each ticket type has been purchased
            for purchase in purchases:
                ticket_name = purchase.get('ticket', '')  # Get the ticket type from each purchase
                if ticket_name in ticket_sales_count:  # If the ticket type is one of the defined ticket types
                    ticket_sales_count[ticket_name] += 1  # Increment the count for that ticket type

            # Debugging: Print the ticket sales count to the terminal
            print("Ticket Sales Count:", ticket_sales_count)

            # Step 3: Display the ticket sales report in a new window
            self.show_ticket_sales_popup(ticket_sales_count)  # Show a pop-up with the sales report

        except Exception as e:  # Catch any errors during the process
            messagebox.showerror("Error", f"An error occurred: {e}")  # Show an error message
            print("Error occurred in view_ticket_sales:", e)  # Print error details for debugging

    def show_ticket_sales_popup(self, ticket_sales_count):
        # Create a custom pop-up window to display the ticket sales report
        sales_popup = tk.Toplevel()  # Create a new top-level window for the ticket sales report
        sales_popup.title("Ticket Sales Report")  # Set the title of the sales report window
        sales_popup.geometry("500x400")  # Set the size of the window
        sales_popup.config(bg="#2A9D8F")  # Set the background color of the window

        label = tk.Label(sales_popup, text="Ticket Sales Report", font=("Helvetica", 18), bg="#2A9D8F", fg="white")  # Create a label for the title
        label.pack(pady=20)  # Pack the label with padding

        # Loop through the sales count and display each ticket type with its sales count
        for ticket_type, count in ticket_sales_count.items():
            ticket_label = tk.Label(sales_popup, text=f"{ticket_type}: {count}", font=("Helvetica", 14), bg="#2A9D8F", fg="white")  # Create a label for each ticket type and its sales count
            ticket_label.pack(pady=5)  # Pack the label with some padding

        close_button = tk.Button(sales_popup, text="Close", width=15, height=2, font=("Arial", 14), bg="#E76F51", fg="white", command=sales_popup.destroy)  # Create a button to close the pop-up
        close_button.pack(pady=20)  # Pack the close button with padding

class Guest:
    def __init__(self, system):
        self.system = system  # Reference to the main system
        self.users_file = "users.pkl"  # File to store user data
        self.current_user = None  # Current user (none at the beginning)

    # Method for user sign-up process
    def sign_up(self):
        # Create a new window for user to sign up
        sign_up_window = tk.Toplevel()
        sign_up_window.title("Sign Up")  # Set the title of the window
        sign_up_window.geometry("500x400")  # Set window size
        sign_up_window.config(bg="#F4A261")  # Set background color

        # Add a label for the form title
        label = tk.Label(sign_up_window, text="Create an Account", font=("Helvetica", 18), bg="#F4A261", fg="#264653")
        label.pack(pady=20)  # Add padding around the label

        # Input fields for user details (Full Name, Email, Password, etc.)
        name_label = tk.Label(sign_up_window, text="Full Name:", font=("Arial", 12), bg="#F4A261", fg="#264653")
        name_label.pack(pady=5)
        name_entry = tk.Entry(sign_up_window, font=("Arial", 12))  # Text entry for full name
        name_entry.pack(pady=5)

        email_label = tk.Label(sign_up_window, text="Email:", font=("Arial", 12), bg="#F4A261", fg="#264653")
        email_label.pack(pady=5)
        email_entry = tk.Entry(sign_up_window, font=("Arial", 12))  # Text entry for email
        email_entry.pack(pady=5)

        password_label = tk.Label(sign_up_window, text="Password:", font=("Arial", 12), bg="#F4A261", fg="#264653")
        password_label.pack(pady=5)
        password_entry = tk.Entry(sign_up_window, font=("Arial", 12), show="*")  # Text entry for password (hidden characters)
        password_entry.pack(pady=5)

        confirm_password_label = tk.Label(sign_up_window, text="Confirm Password:", font=("Arial", 12), bg="#F4A261", fg="#264653")
        confirm_password_label.pack(pady=5)
        confirm_password_entry = tk.Entry(sign_up_window, font=("Arial", 12), show="*")  # Confirm password field
        confirm_password_entry.pack(pady=5)

        # Button to trigger user sign-up validation and save
        sign_up_button = tk.Button(sign_up_window, text="Sign Up", width=20, height=2, font=("Arial", 14), bg="#2A9D8F", fg="white", 
                                   command=lambda: self.validate_and_save_user(name_entry.get(), email_entry.get(), password_entry.get(), confirm_password_entry.get(), sign_up_window))
        sign_up_button.pack(pady=20)  # Button to submit the form

    # Method for user login process
    def login(self):
        # Create a new window for user login
        login_window = tk.Toplevel()
        login_window.title("Login")  # Set the title of the window
        login_window.geometry("400x300")  # Set window size
        login_window.config(bg="#F4A261")  # Set background color

        # Add a label for login form title
        label = tk.Label(login_window, text="Login", font=("Helvetica", 18), bg="#F4A261", fg="#264653")
        label.pack(pady=20)  # Add padding around the label

        # Input fields for user email and password
        email_label = tk.Label(login_window, text="Email:", font=("Arial", 12), bg="#F4A261", fg="#264653")
        email_label.pack(pady=5)
        email_entry = tk.Entry(login_window, font=("Arial", 12))  # Text entry for email
        email_entry.pack(pady=5)

        password_label = tk.Label(login_window, text="Password:", font=("Arial", 12), bg="#F4A261", fg="#264653")
        password_label.pack(pady=5)
        password_entry = tk.Entry(login_window, font=("Arial", 12), show="*")  # Text entry for password (hidden characters)
        password_entry.pack(pady=5)

        # Button to trigger login validation
        login_button = tk.Button(login_window, text="Login", width=20, height=2, font=("Arial", 14), bg="#2A9D8F", fg="white", 
                                 command=lambda: self.validate_login(email_entry.get(), password_entry.get(), login_window))
        login_button.pack(pady=20)  # Button to submit login form

    # Method to validate and save user during sign-up
    def validate_and_save_user(self, name, email, password, confirm_password, sign_up_window):
        # Validate user input and save user to a Pickle file
        if not name or not email or not password or not confirm_password:
            self.show_error_popup("All fields are required!")  # Show error if any field is empty
            return

        # Validate email format using regex
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.show_error_popup("Please enter a valid email address!")  # Show error for invalid email
            return

        # Check if passwords match
        if password != confirm_password:
            self.show_error_popup("Passwords do not match!")  # Show error for mismatched passwords
            return

        # Save user data into a dictionary
        user_data = {"name": name, "email": email, "password": password, "ticket_history": []}
        try:
            # Check if the users file exists, if so, load the data
            if os.path.exists(self.users_file):
                with open(self.users_file, "rb") as file:
                    users = pickle.load(file)
            else:
                users = []

            # Append the new user data and save it back to the file
            users.append(user_data)
            with open(self.users_file, "wb") as file:
                pickle.dump(users, file)

            messagebox.showinfo("Success", "Account created successfully!")  # Show success message
            sign_up_window.destroy()  # Close the sign-up window
        except Exception as e:
            self.show_error_popup(f"An error occurred while saving the account: {e}")  # Show error if there's an issue

    # Method to validate user login
    def validate_login(self, email, password, login_window):
        try:
            # Check if email and password are entered
            if not email or not password:
                self.show_error_popup("Please enter both email and password!")  # Show error if any field is empty
                return

            # Load users from file and validate login credentials
            with open(self.users_file, "rb") as file:
                users = pickle.load(file)

            # Check each user's credentials
            for user in users:
                if user["email"] == email and user["password"] == password:
                    self.current_user = user  # Set the current user
                    self.show_success_popup("Login successful!", login_window)  # Show success popup and pass login window
                    return

            self.show_error_popup("Invalid email or password!")  # Show error if credentials are incorrect
        except Exception as e:
            self.show_error_popup(f"An error occurred during login: {e}")  # Show error if there's an issue

    def show_success_popup(self, message, login_window):
        # Create a custom success popup
        success_popup = tk.Toplevel()
        success_popup.title("Success")
        success_popup.geometry("400x200")
        success_popup.config(bg="#F4A261")

        # Label with the success message
        success_label = tk.Label(success_popup, text=message, font=("Helvetica", 16, "bold"), bg="#F4A261", fg="white")
        success_label.pack(pady=40)

        # Close button for the success popup
        close_button = tk.Button(success_popup, text="Close", width=15, height=2, font=("Arial", 12), bg="#264653", fg="white",
                                command=lambda: self.close_success_popup(success_popup, login_window))
        close_button.pack(pady=10)

        success_popup.mainloop()

    def close_success_popup(self, success_popup, login_window):
        success_popup.destroy()  # Close the success popup
        login_window.destroy()  # Close the login window
        self.user_menu()  # Show user menu

        def show_error_popup(self, message):
        # Create a new window to show an error message
        error_popup = tk.Toplevel()
        error_popup.title("Error")  # Set window title to "Error"
        error_popup.geometry("400x200")  # Set window size
        error_popup.config(bg="#F4A261")  # Set background color

        # Display the error message in the popup
        error_label = tk.Label(error_popup, text=message, font=("Helvetica", 14), bg="#F4A261", fg="red")
        error_label.pack(pady=50)  # Add padding around the error label

        # Add a button to close the error popup
        close_button = tk.Button(error_popup, text="Close", width=15, height=2, font=("Arial", 12), bg="#E76F51", fg="white", command=error_popup.destroy)
        close_button.pack(pady=10)  # Add padding around the close button

    def user_menu(self):
        # Create a new window for the user's menu
        user_menu_window = tk.Toplevel()
        user_menu_window.title(f"Welcome {self.current_user['name']}")  # Set the window title with the user's name
        user_menu_window.geometry("600x400")  # Set window size
        user_menu_window.config(bg="#F4A261")  # Set background color

        # Add a label for the menu title
        label = tk.Label(user_menu_window, text="User Menu", font=("Helvetica", 18), bg="#F4A261", fg="#264653")
        label.pack(pady=20)  # Add padding around the label

        # Buttons for various user options
        view_profile_button = tk.Button(user_menu_window, text="View Profile Information", width=25, height=2, font=("Arial", 14), bg="#2A9D8F", fg="white", command=self.view_profile)
        view_profile_button.pack(pady=10)  # Button to view user profile

        update_profile_button = tk.Button(user_menu_window, text="Update Profile Information", width=25, height=2, font=("Arial", 14), bg="#E76F51", fg="white", command=self.update_profile)
        update_profile_button.pack(pady=10)  # Button to update user profile

        # Button to purchase a ticket
        purchase_ticket_button = tk.Button(user_menu_window, text="Purchase Ticket", width=25, height=2, font=("Arial", 14), bg="#264653", fg="white", 
                                            command=self.system.ticket.purchase_ticket)  # Call the purchase ticket method from the Ticket class
        purchase_ticket_button.pack(pady=10)  # Button for purchasing a ticket

        # Button to view ticket history
        view_history_button = tk.Button(user_menu_window, text="View Ticket History", width=25, height=2, font=("Arial", 14), bg="#D9BF77", fg="white", command=self.view_ticket_history)
        view_history_button.pack(pady=10)  # Button to view the user's ticket history

    def view_profile(self):
        # Create a new window to display user profile information
        profile_window = tk.Toplevel()
        profile_window.title("Profile Information")  # Set the window title
        profile_window.geometry("500x300")  # Set window size
        profile_window.config(bg="#F4A261")  # Set a beautiful background color

        # Add a title label for the profile information
        title_label = tk.Label(profile_window, text="Profile Information", font=("Helvetica", 20, "bold"), bg="#F4A261", fg="#264653")
        title_label.pack(pady=20)  # Add padding around the title label

        # Display user's name
        name_label = tk.Label(
            profile_window,
            text=f"Name: {self.current_user['name']}",  # Show the user's name
            font=("Arial", 16),
            bg="#F4A261",
            fg="#264653",
            anchor="w",  # Align text to the left
            justify="left",  # Justify text to the left
            padx=20  # Padding inside the label
        )
        name_label.pack(fill="both", pady=10)  # Fill the label and add padding

        # Display user's email
        email_label = tk.Label(
            profile_window,
            text=f"Email: {self.current_user['email']}",  # Show the user's email
            font=("Arial", 16),
            bg="#F4A261",
            fg="#264653",
            anchor="w",  # Align text to the left
            justify="left",  # Justify text to the left
            padx=20  # Padding inside the label
        )
        email_label.pack(fill="both", pady=10)  # Fill the label and add padding

        # Add a close button to close the profile window
        close_button = tk.Button(
            profile_window,
            text="Close",  # Button text
            font=("Arial", 14),
            bg="#E76F51",
            fg="white",
            width=15,
            command=profile_window.destroy  # Close the profile window when clicked
        )
        close_button.pack(pady=20)  # Add padding around the close button

    def update_profile(self):
        # Create a new window for updating the user's profile
        update_window = tk.Toplevel()
        update_window.title("Update Profile")  # Set the window title
        update_window.geometry("500x400")  # Set window size
        update_window.config(bg="#F4A261")  # Set a beautiful background color

        # Add a title label for updating the profile
        title_label = tk.Label(update_window, text="Update Profile", font=("Helvetica", 20, "bold"), bg="#F4A261", fg="#264653")
        title_label.pack(pady=20)  # Add padding around the title label

        # Input fields for updating the user's name, email, and password
        name_label = tk.Label(update_window, text="Full Name:", font=("Arial", 12), bg="#F4A261", fg="#264653")
        name_label.pack(pady=5)
        name_entry = tk.Entry(update_window, font=("Arial", 12))  # Input for name
        name_entry.insert(0, self.current_user["name"])  # Pre-fill the name field with the current name
        name_entry.pack(pady=5)

        email_label = tk.Label(update_window, text="Email:", font=("Arial", 12), bg="#F4A261", fg="#264653")
        email_label.pack(pady=5)
        email_entry = tk.Entry(update_window, font=("Arial", 12))  # Input for email
        email_entry.insert(0, self.current_user["email"])  # Pre-fill the email field with the current email
        email_entry.pack(pady=5)

        # Optionally, allow the user to update the password
        password_label = tk.Label(update_window, text="Password:", font=("Arial", 12), bg="#F4A261", fg="#264653")
        password_label.pack(pady=5)
        password_entry = tk.Entry(update_window, font=("Arial", 12), show="*")  # Input for password (hidden characters)
        password_entry.insert(0, self.current_user["password"])  # Pre-fill the password field with the current password
        password_entry.pack(pady=5)

        confirm_password_label = tk.Label(update_window, text="Confirm Password:", font=("Arial", 12), bg="#F4A261", fg="#264653")
        confirm_password_label.pack(pady=5)
        confirm_password_entry = tk.Entry(update_window, font=("Arial", 12), show="*")  # Input to confirm the password
        confirm_password_entry.insert(0, self.current_user["password"])  # Pre-fill with the current password
        confirm_password_entry.pack(pady=5)

        # Save button to apply changes to the profile
        save_button = tk.Button(update_window, text="Save Changes", width=20, height=2, font=("Arial", 14), bg="#2A9D8F", fg="white",
                                command=lambda: self.save_updated_profile(name_entry.get(), email_entry.get(), password_entry.get(),
                                                                            confirm_password_entry.get(), update_window))
        save_button.pack(pady=20)  # Add padding around the save button

        # Cancel button to close the update window without saving
        cancel_button = tk.Button(update_window, text="Cancel", width=20, height=2, font=("Arial", 14), bg="#E76F51", fg="white",
                                    command=update_window.destroy)  # Close the update window without saving
        cancel_button.pack(pady=10)  # Add padding around the cancel button

    def save_updated_profile(self, name, email, password, confirm_password, update_window):
        # Validate and save updated user information

        # Ensure all fields are filled out
        if not name or not email or not password or not confirm_password:
            self.show_error_popup("All fields are required!")  # Show error if any field is empty
            return

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.show_error_popup("Please enter a valid email address!")  # Show error if email format is invalid
            return

        # Ensure passwords match
        if password != confirm_password:
            self.show_error_popup("Passwords do not match!")  # Show error if passwords don't match
            return

        # Update the current user's profile with new information
        self.current_user["name"] = name
        self.current_user["email"] = email
        self.current_user["password"] = password

        # Save updated user information back to the users file
        try:
            # Load users from the pickle file
            with open(self.users_file, "rb") as file:
                users = pickle.load(file)

            # Find the current user and update their information
            for user in users:
                if user["email"] == self.current_user["email"]:  # Find the current user by email
                    user["name"] = name
                    user["email"] = email
                    user["password"] = password
                    break

            # Save the updated user data back to the file
            with open(self.users_file, "wb") as file:
                pickle.dump(users, file)

            messagebox.showinfo("Success", "Profile updated successfully!")  # Inform the user of the success
            update_window.destroy()  # Close the update window

        except Exception as e:
            # Handle errors during the file operations
            self.show_error_popup(f"An error occurred while saving the changes: {e}")

    def view_ticket_history(self):
        # Step 1: Open a modal to ask for the user's email
        email_modal = tk.Toplevel()
        email_modal.title("View Ticket History")
        email_modal.geometry("500x300")
        email_modal.config(bg="#F4A261")

        label_font = ("Helvetica", 18)
        entry_font = ("Helvetica", 16)

        # Ask for the user's email
        email_label = tk.Label(email_modal, text="Enter your email to view history:", bg="#F4A261", fg="white", font=label_font)
        email_label.pack(pady=20)

        email_entry = tk.Entry(email_modal, font=entry_font, width=30)
        email_entry.pack(pady=10)

        def fetch_history():
            # Fetch and display the purchase history based on email input
            email = email_entry.get()
            if not email:
                messagebox.showerror("Invalid Input", "Email is required.")  # Show error if email is empty
                return

            # Step 2: Load purchase history from the pickle file
            if not os.path.exists('purchase_history.pkl'):
                messagebox.showinfo("No Purchase History", "No purchase history found.")  # Show info if no purchase history exists
                email_modal.destroy()
                return

            try:
                # Load and filter purchases based on user email
                with open('purchase_history.pkl', 'rb') as f:
                    purchases = []
                    while True:
                        try:
                            purchase = pickle.load(f)
                            if purchase.get('user_email') == email:
                                purchases.append(purchase)
                        except EOFError:
                            break

                # Step 3: Show the purchase history in a formatted modal
                if purchases:
                    email_modal.destroy()
                    self.display_purchase_history(purchases)  # Display the filtered purchases
                else:
                    messagebox.showinfo("No History Found", "No purchases found for the provided email.")  # Inform the user if no purchases are found
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while fetching history: {e}")
                email_modal.destroy()

        submit_button = tk.Button(email_modal, text="Submit", bg="#457B9D", fg="white", font=("Helvetica", 16), command=fetch_history)
        submit_button.pack(pady=20)

        email_modal.wait_window()  # Wait for the modal to close before proceeding

    def display_purchase_history(self, purchases):
        # Step 4: Display the purchase history in a larger modal

        history_modal = tk.Toplevel()
        history_modal.title("Purchase History")
        history_modal.geometry("700x500")
        history_modal.config(bg="#F4A261")

        # Title label for the purchase history window
        title_label = tk.Label(history_modal, text="Your Purchase History", bg="#F4A261", fg="white", font=("Helvetica", 22, "bold"))
        title_label.pack(pady=20)

        # Create a scrollable frame for displaying purchase details
        history_frame = tk.Frame(history_modal, bg="#FFFFFF", bd=2, relief="groove")
        history_frame.pack(fill="both", expand=True, padx=20, pady=20)

        canvas = tk.Canvas(history_frame, bg="#FFFFFF")
        scrollbar = tk.Scrollbar(history_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FFFFFF")

        # Ensure the canvas adjusts when the scrollable frame changes size
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Format and display each purchase in the scrollable frame
        for idx, purchase in enumerate(purchases):
            frame = tk.Frame(scrollable_frame, bg="#F1F1F1", padx=10, pady=10, relief="ridge", bd=2)
            frame.pack(fill="x", padx=10, pady=5)

            payment_method = purchase.get('payment_method', 'Not Provided')  # Handle missing 'payment_method' field

            # Format and display the purchase details
            info = (
                f"Purchase {idx + 1}:\n"
                f"Ticket: {purchase['ticket']}\n"
                f"Visit Date: {purchase['visit_date']}\n"
                f"Persons: {purchase['num_persons']}\n"
                f"Total Price: ${purchase['total_price']}\n"
                f"Payment Method: {payment_method}\n"
                f"Email: {purchase['user_email']}\n"
            )

            # Display the formatted purchase information
            tk.Label(frame, text=info, bg="#F1F1F1", fg="#3D5A80", font=("Helvetica", 14), justify="left").pack(anchor="w")

        # Add a button to close the history modal
        close_button = tk.Button(history_modal, text="Close", bg="#E63946", fg="white", font=("Helvetica", 16), command=history_modal.destroy)
        close_button.pack(pady=20)

# Class to handle ticket-related operations, such as displaying ticket options and purchasing tickets
class Ticket:
    def __init__(self, system):
        # Initialize the Ticket object with the system and ticket options
        self.system = system
        
        # List of available ticket options, each represented as a TicketDetails object
        self.ticket_options = [
            TicketDetails("Single Day Pass", "Access to the park for one day", 275, "1 day", "None", "Valid only on selected date"),
            TicketDetails("Two-Day Pass", "Access to the park for two consecutive days", 480, "2 days", "10% discount for online purchase", "Cannot be split over multiple trips"),
            TicketDetails("Annual Membership", "Unlimited access for one year", 1840, "1 year", "15% discount on renewal", "Must be used by the same person"),
            TicketDetails("Child Ticket", "Discounted ticket for children (ages 3-12)", 185, "1 day", "None", "Valid only on selected date, must be accompanied by an adult"),
            TicketDetails("Group Ticket (10+)", "Special rate for groups of 10 or more", 220, "1 day", "20% off for groups of 20 or more", "Must be booked in advance"),
            TicketDetails("VIP Experience Pass", "Includes expedited access and reserved seating for shows", 550, "1 day", "None", "Limited availability, must be purchased in advance")
        ]
        
        # A dictionary to store current user data, including their ticket history
        self.current_user = {"ticket_history": []} 

    # Method to display the ticket purchase window
    def purchase_ticket(self):
        # Create a new top-level window for the ticket purchase
        ticket_window = tk.Toplevel()
        ticket_window.title("Purchase Ticket")  # Set the window title
        ticket_window.geometry("800x600")  # Set the window size
        ticket_window.config(bg="#F4A261")  # Set the background color

        # Title label for the window, explaining the purpose of the window
        title_label = tk.Label(
            ticket_window, 
            text="Select a Ticket Type", 
            font=("Calibri", 28, "bold"), 
            bg="#F4A261", 
            fg="#3D5A80"
        )
        title_label.pack(pady=30)  # Add padding around the title label

        # Create a canvas that will hold the list of ticket options
        canvas = tk.Canvas(ticket_window, bg="#F4A261", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)  # Place the canvas on the left side of the window
        # Add a vertical scrollbar to the canvas
        scrollbar = tk.Scrollbar(ticket_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")  # Position the scrollbar to the right side
        canvas.configure(yscrollcommand=scrollbar.set)  # Connect scrollbar to the canvas

        # Create a frame to hold the ticket details inside the canvas
        ticket_frame = tk.Frame(canvas, bg="#F4A261")
        canvas.create_window((0, 0), window=ticket_frame, anchor="nw")  # Place frame on the canvas

        # Configure columns for the ticket frame (two columns)
        ticket_frame.grid_columnconfigure(0, weight=1, uniform="equal")
        ticket_frame.grid_columnconfigure(1, weight=1, uniform="equal")

        # Calculate the number of rows needed to display all tickets (2 per row)
        num_rows = (len(self.ticket_options) + 1) // 2

        # Loop through the available tickets and create UI elements for each
        for index, ticket in enumerate(self.ticket_options):
            row = index // 2  # Determine the row for the ticket
            column = index % 2  # Determine the column for the ticket

            # Create a frame for each ticket with details
            details_frame = tk.Frame(ticket_frame, bg="#FFFFFF", padx=20, pady=15, relief="solid", bd=1)
            details_frame.grid(row=row, column=column, padx=20, pady=15, sticky="w")

            # Label displaying the ticket name
            ticket_name_label = tk.Label(
                details_frame, 
                text=f"Ticket: {ticket.name}", 
                font=("Calibri", 18, "bold"), 
                bg="#FFFFFF", 
                fg="#3D5A80", 
                anchor="w"
            )
            ticket_name_label.grid(row=0, column=0, sticky="w", columnspan=2, pady=(0, 10))

            # Label displaying the ticket description
            description_label = tk.Label(
                details_frame, 
                text=f"Description: {ticket.description}", 
                font=("Calibri", 12), 
                bg="#FFFFFF", 
                fg="#3D5A80", 
                wraplength=300, 
                anchor="w"
            )
            description_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 5))

            # Label displaying the ticket price
            price_label = tk.Label(
                details_frame, 
                text=f"Price: ${ticket.price}", 
                font=("Calibri", 14, "bold"), 
                bg="#FFFFFF", 
                fg="#E63946", 
                anchor="w"
            )
            price_label.grid(row=5, column=0, sticky="w", pady=(0, 10))

            # Button for purchasing the ticket, calling the open_purchase_modal method when clicked
            purchase_button = tk.Button(
                details_frame, 
                text="Purchase Now", 
                font=("Calibri", 14, "bold"), 
                bg="#457B9D", 
                fg="#FFFFFF", 
                activebackground="#1D3557", 
                activeforeground="#FFFFFF", 
                cursor="hand2", 
                relief="flat", 
                command=lambda ticket=ticket: self.open_purchase_modal(ticket)  # Lambda to pass ticket to method
            )
            purchase_button.grid(row=6, column=0, pady=10, ipadx=10, ipady=5, sticky="w")

        # Update the frame after adding all ticket options
        ticket_frame.update_idletasks()
        # Configure the canvas scroll region based on the size of the ticket frame
        canvas.config(scrollregion=canvas.bbox("all"))

    # Method to open a modal for processing ticket purchase
    def open_purchase_modal(self, ticket):
        # Create a new top-level window (modal) for the ticket purchase
        modal = tk.Toplevel()
        modal.title(f"Purchase {ticket.name}")  # Set the title to include the ticket name
        modal.geometry("600x600")  # Set the window size (larger size for better visibility)
        modal.config(bg="#F4A261")  # Set the background color for the modal

        # Define font styles for labels and input fields
        label_font = ("Helvetica", 18)  # Larger font for labels
        entry_font = ("Helvetica", 16)  # Larger font for input fields

        # Label for entering the visit date
        visit_date_label = tk.Label(modal, text="Enter Visit Date (YYYY-MM-DD):", bg="#F4A261", fg="white", font=label_font)
        visit_date_label.pack(pady=30)  # Add padding around the label

        # Input field for the visit date (in the format YYYY-MM-DD)
        visit_date_entry = tk.Entry(modal, font=entry_font, width=25)  # Larger input field for date
        visit_date_entry.pack(pady=20)  # Add padding around the input field

        # Label for entering the number of persons
        num_persons_label = tk.Label(modal, text="Enter Number of Persons:", bg="#F4A261", fg="white", font=label_font)
        num_persons_label.pack(pady=30)  # Add padding around the label

        # Input field for the number of persons (used to calculate total price)
        num_persons_entry = tk.Entry(modal, font=entry_font, width=25)  # Larger input field for number of persons
        num_persons_entry.pack(pady=20)  # Add padding around the input field

        # Function to process the purchase when the user clicks the "Confirm Purchase" button
        def process_purchase():
            # Get the values entered in the input fields
            visit_date = visit_date_entry.get()  # Visit date entered by the user
            try:
                num_persons = int(num_persons_entry.get())  # Convert the number of persons to an integer
            except ValueError:
                # If the input is not a valid integer, show an error message
                messagebox.showerror("Invalid Input", "Please enter a valid number of persons.")
                return

            # Calculate discount based on ticket type
            discount = 0
            if ticket.name == "Two-Day Pass":
                discount = 0.10  # 10% discount for Two-Day Pass
            elif ticket.name == "Annual Membership":
                discount = 0.15  # 15% discount for Annual Membership
            elif ticket.name == "Group Ticket (10+)":
                if num_persons >= 10:
                    discount = 0.20  # 20% discount for groups of 10 or more persons

            # Calculate the total price, discount amount, and final price after applying discount
            total_price = ticket.price * num_persons
            discount_amount = total_price * discount
            final_price = total_price - discount_amount

            # Ask the user for their email and payment method using another method
            email, payment_method = self.ask_for_email_and_payment_method()

            # Check if email and payment method are provided
            if not email or not payment_method:
                messagebox.showerror("Invalid Input", "Both email and payment method are required to complete the purchase.")
                return

            # Generate the invoice string showing the details of the purchase
            invoice = f"--- Invoice ---\nTicket: {ticket.name}\nVisit Date: {visit_date}\nPersons: {num_persons}\nPrice: ${ticket.price} x {num_persons} = ${total_price}\nDiscount: {discount*100}% = -${discount_amount}\nTotal: ${final_price}\n"

            # Create a new modal to show the purchase invoice
            invoice_modal = tk.Toplevel()
            invoice_modal.title("Purchase Invoice")  # Set the title of the invoice modal
            invoice_modal.geometry("600x400")  # Set the window size for the invoice modal
            invoice_modal.config(bg="#F4A261")  # Set the background color for the invoice modal

            # Label to display the generated invoice
            invoice_label = tk.Label(invoice_modal, text=invoice, bg="#F4A261", fg="#3D5A80", font=("Calibri", 14))
            invoice_label.pack(pady=20)  # Add padding around the invoice label

            # Save the purchase details into a dictionary
            purchase_details = {
                'ticket': ticket.name,
                'visit_date': visit_date,
                'num_persons': num_persons,
                'total_price': final_price,
                'user_email': email,
                'payment_method': payment_method  # Include payment method in the details
            }

            # Check if the pickle file for saving purchase history exists
            if not os.path.exists('purchase_history.pkl'):
                # If the file doesn't exist, create it as an empty file
                with open('purchase_history.pkl', 'wb') as f:
                    pass  # Creating an empty file if it doesn't exist

            # Save the purchase details to the pickle file (for persistent storage)
            try:
                with open('purchase_history.pkl', 'ab') as f:
                    pickle.dump(purchase_details, f)  # Append the purchase details to the file
                    print("Purchase saved to pickle file.")  # Log success to the console
            except Exception as e:
                # If an error occurs while saving, log the error message
                print(f"Error saving purchase to pickle: {e}")

            # Call a method to show a "purchase complete" modal to the user method assumed to be defined elsewhere
            self.show_purchase_complete_modal()

            # Close the modals after the purchase is processed
            modal.destroy()
            invoice_modal.destroy()

        # "Confirm Purchase" button that calls the process_purchase function when clicked
        purchase_button = tk.Button(modal, text="Confirm Purchase", bg="#457B9D", fg="#FFFFFF", font=("Helvetica", 16), command=process_purchase)
        purchase_button.pack(pady=30)  # Add padding around the button

    # Method to ask for the user's email and payment method
    def ask_for_email_and_payment_method(self):
        # Create a new modal window for email and payment method input
        email_modal = tk.Toplevel()
        email_modal.title("Enter Email and Payment Method")  # Set the title of the modal
        email_modal.geometry("500x350")  # Set the size of the modal window
        email_modal.config(bg="#F4A261")  # Set the background color

        # Define fonts for labels and input fields
        label_font = ("Helvetica", 18)
        entry_font = ("Helvetica", 16)

        # Email input section
        email_label = tk.Label(email_modal, text="Please enter your email address:", bg="#F4A261", fg="white", font=label_font)
        email_label.pack(pady=20)  # Add padding around the label

        # Input field for the user's email
        email_entry = tk.Entry(email_modal, font=entry_font, width=30)
        email_entry.pack(pady=10)  # Add padding around the email input field

        # Payment method selection section
        payment_label = tk.Label(email_modal, text="Select Payment Method:", bg="#F4A261", fg="white", font=label_font)
        payment_label.pack(pady=20)  # Add padding around the label

        # List of payment methods available for selection
        payment_methods = ["Credit Card", "Debit Card"]
        payment_method_var = tk.StringVar()  # Create a variable to store the selected payment method
        payment_method_var.set(payment_methods[0])  # Default to Credit Card

        # Dropdown menu for selecting payment method
        payment_dropdown = tk.OptionMenu(email_modal, payment_method_var, *payment_methods)
        payment_dropdown.config(font=("Helvetica", 16), width=20)
        payment_dropdown.pack(pady=10)  # Add padding around the dropdown menu

        # Function to handle the submission of email and payment method
        def submit_email_and_payment():
            email = email_entry.get()  # Get the entered email
            payment_method = payment_method_var.get()  # Get the selected payment method

            # Check if email and payment method are provided
            if not email or not payment_method:
                messagebox.showerror("Invalid Input", "Both email and payment method are required.")  # Show error if missing
                return

            # Store the user's email and selected payment method
            self.user_email = email
            self.payment_method = payment_method

            # Close the modal after submitting
            email_modal.destroy()

        # Submit button to confirm email and payment method
        submit_button = tk.Button(email_modal, text="Submit", bg="#457B9D", fg="white", font=("Helvetica", 16), command=submit_email_and_payment)
        submit_button.pack(pady=20)  # Add padding around the button

        # Wait for the modal to close before proceeding
        email_modal.wait_window()

        # Return the email and payment method after the modal is closed
        return self.user_email, self.payment_method

    # Method to show a confirmation modal after the purchase is completed
    def show_purchase_complete_modal(self):
        # Create a new modal window for the purchase completion message
        complete_modal = tk.Toplevel()
        complete_modal.title("Purchase Complete")  # Set the title of the modal
        complete_modal.geometry("400x300")  # Set the size of the modal window
        complete_modal.config(bg="#F4A261")  # Set the background color

        # Define fonts for the labels
        label_font = ("Helvetica", 18, "bold")
        message_font = ("Helvetica", 14)

        # Label showing the purchase completion message
        complete_label = tk.Label(complete_modal, text="Purchase Completed!", bg="#F4A261", fg="white", font=label_font)
        complete_label.pack(pady=40)  # Add padding around the label

        # Additional message about the successful purchase
        message_label = tk.Label(complete_modal, text="Your purchase was successful.\nInvoice has been saved.", bg="#457B9D", fg="white", font=message_font)
        message_label.pack(pady=20)  # Add padding around the message

        # "OK" button to close the modal
        ok_button = tk.Button(complete_modal, text="OK", bg="#1D3557", fg="white", font=("Helvetica", 16), command=complete_modal.destroy)
        ok_button.pack(pady=20)  # Add padding around the button

        # Wait for the modal to close before proceeding
        complete_modal.wait_window()
    
# Class to represent the details of a ticket
class TicketDetails:
    def __init__(self, name, description, price, validity, discount, restrictions):
        # Initialize the TicketDetails object with the given parameters
        self.name = name  # The name of the ticket e.g "Adult", "Child", etc
        self.description = description  # A brief description of the ticket type
        self.price = price  # The price of the ticket
        self.validity = validity  # The validity period of the ticket e.g "1 day", "1 year"
        self.discount = discount  # The discount applied to the ticket
        self.restrictions = restrictions  # Any restrictions associated with the ticket e.g "Non-refundable"

# Main entry point of the program
if __name__ == "__main__":
    # Creating an instance of the TicketBookingSystem 
    system = TicketBookingSystem()
    
    # Calling the method to create the main menu for the system
    system.create_main_menu()

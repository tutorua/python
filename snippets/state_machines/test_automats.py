from transitions import Machine
import sqlite3

# Create the database and the users table (if not exists)
def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    userId INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    didAcceptTerms BOOLEAN NOT NULL)''')
    conn.commit()
    conn.close()

# Function to load user from the database
def load_user(userId):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT name, didAcceptTerms FROM users WHERE userId=?", (userId,))
    user = c.fetchone()
    conn.close()
    if user:
        return {"status": "Success", "name": user[0], "didAcceptTerms": user[1]}
    else:
        return {"status": "Fail"}

# Function to get the terms and conditions
def get_terms():
    terms_document = "Latest terms and conditions document."
    return {"status": "Success", "terms": terms_document}

# Function to save user to the database
def save_user(userId, name, didAcceptTerms):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT OR REPLACE INTO users (userId, name, didAcceptTerms) VALUES (?, ?, ?)", 
                  (userId, name, didAcceptTerms))
        conn.commit()
        return {"status": "Success"}
    except sqlite3.Error as e:
        return {"status": "Fail", "error": str(e)}
    finally:
        conn.close()

# Class for the user login process
class UserLoginProcess:
    states = ['start', 'welcome', 'request_user_id', 'load_user', 'check_user', 'get_terms', 'display_terms', 'request_details', 'save_user', 'next_state']

    def __init__(self):
        self.machine = Machine(model=self, states=UserLoginProcess.states, initial='start')
        self.userId = None
        self.user_data = None
        self.name = None

        # Define the transitions between states
        self.machine.add_transition(trigger='start_process', source='start', dest='welcome', after='welcome_user')
        self.machine.add_transition(trigger='input_user_id', source='welcome', dest='request_user_id', after='request_user_id')
        self.machine.add_transition(trigger='load_user_data', source='request_user_id', dest='load_user', after='load_user')
        self.machine.add_transition(trigger='check_user_existence', source='load_user', dest='check_user', after='check_user')
        self.machine.add_transition(trigger='user_exists', source='check_user', dest='next_state', conditions='user_accepted_terms', after='next_state')
        self.machine.add_transition(trigger='user_needs_terms', source='check_user', dest='get_terms', conditions='user_not_accepted_terms')
        self.machine.add_transition(trigger='display_terms_to_user', source='get_terms', dest='display_terms', after='display_terms')
        self.machine.add_transition(trigger='request_user_details', source='check_user', dest='request_details', conditions='user_does_not_exist', after='request_details')
        self.machine.add_transition(trigger='get_terms_after_details', source='request_details', dest='get_terms', after='get_terms')
        self.machine.add_transition(trigger='save_user_data', source=['display_terms', 'request_details'], dest='save_user', after='save_user')
        self.machine.add_transition(trigger='proceed_to_next_state', source='save_user', dest='next_state', after='next_state')

    def welcome_user(self):
        # Display welcome message
        print("Welcome to our service! Let’s get you started.")
        self.input_user_id()

    def request_user_id(self):
        # Request the user to input their ID
        self.userId = int(input("Input your ID: "))
        self.load_user_data()

    def load_user(self):
        # Load the user's data from the database
        self.user_data = load_user(self.userId)
        self.check_user_existence()

    def check_user(self):
        # Check if the user exists in the system
        if self.user_data["status"] == "Success":
            self.user_data["userId"] = self.userId  # Add userId to the user data dictionary
            if self.user_data["didAcceptTerms"]:
                # If user has accepted terms, trigger user_exists
                self.user_exists()
            else:
                # If user has not accepted terms, trigger user_needs_terms
                self.user_needs_terms()
        else:
            # If user does not exist, request user details
            self.request_user_details()

    def user_accepted_terms(self):
        # Condition check if user has accepted terms
        return self.user_data["didAcceptTerms"]

    def user_not_accepted_terms(self):
        # Condition check if user has not accepted terms
        return not self.user_data["didAcceptTerms"]

    def user_does_not_exist(self):
        # Condition check if user does not exist
        return self.user_data["status"] == "Fail"

    def get_terms(self):
        # Get the latest terms and conditions
        self.terms = get_terms()
        self.display_terms_to_user()

    def display_terms(self):
        # Display the terms to the user and request acceptance
        print("Please read and accept the following terms:")
        print(self.terms["terms"])
        accept = input("Do you accept the terms? (yes/no): ")
        if accept.lower() == 'yes':
            self.user_data["didAcceptTerms"] = True
            self.save_user_data()
        else:
            print("Terms not accepted. Cannot proceed.")

    def request_details(self):
        # Request user's name and other details
        self.name = input("User not found. Please enter your name: ")
        self.user_data = {"userId": self.userId, "name": self.name, "didAcceptTerms": False}
        self.get_terms_after_details()

    def save_user(self):
        # Save the user data to the database
        save_result = save_user(self.userId, self.user_data["name"], self.user_data["didAcceptTerms"])
        if save_result["status"] == "Success":
            self.proceed_to_next_state()
        else:
            print("Failed to save user data. Error:", save_result["error"])

    def next_state(self):
        # Proceed to the next state
        print("Proceed to the next state.")

# Create an instance and start the process
create_database()
user_login_process = UserLoginProcess()
user_login_process.start_process()

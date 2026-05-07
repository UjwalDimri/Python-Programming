#   HOSTEL MANAGEMENT SYSTEM
#   Modules: Housekeeping & Maintenance
#   Author : UJWAL DIMRI 590022777
#  
#   LOGIN ROLES:
#     1. Student   Can raise Housekeeping / Maintenance requests
#                   and rate completed services
#     2. Warden    Can view all requests, mark as completed,
#                   and view summary reports


import pandas as pd
import numpy as np
import os
import getpass   # hides password while typing (shows blank)

#  FILE NAMES

HOUSEKEEPING_FILE = "housekeeping.csv"
MAINTENANCE_FILE  = "maintenance.csv"
USERS_FILE        = "users.csv"          # stores registered students

# Columns for service request CSVs
CSV_COLUMNS  = ["Name", "Room Number", "Issue", "Preferred Time", "Status", "Rating"]

# Columns for users CSV
USER_COLUMNS = ["Username", "Password", "Role", "Room Number"]


#  WARDEN CREDENTIALS  (hardcoded — only one warden account)

WARDEN_USERNAME = "warden"
WARDEN_PASSWORD = "warden123"


# ==============================================================
#  CLASS: AuthManager
#  Handles student registration and login for both roles.
# ==============================================================

class AuthManager:
    """
    Manages user accounts stored in users.csv.
    Students register and login here.
    Warden uses a fixed hardcoded account.
    """

    def __init__(self):
        # Create users.csv with headers if it doesn't exist
        if not os.path.exists(USERS_FILE):
            pd.DataFrame(columns=USER_COLUMNS).to_csv(USERS_FILE, index=False)

    def _load_users(self) -> pd.DataFrame:
        """Load users.csv into a DataFrame."""
        return pd.read_csv(USERS_FILE)

    def _save_users(self, df: pd.DataFrame):
        """Save updated users DataFrame back to CSV."""
        df.to_csv(USERS_FILE, index=False)

    
    #  REGISTER a new student account
    
    def register_student(self):
        """Lets a new student create a username + password account."""
        print("\n  ── Student Registration ──")

        username    = input("  Choose a Username   : ").strip()
        room_number = input("  Your Room Number    : ").strip()

        # Check if username is already taken
        df = self._load_users()
        if not df.empty and username in df["Username"].values:
            print("  Username already exists. Please choose another.")
            return False

        # getpass hides the password so it doesn't appear on screen
        password = getpass.getpass("  Choose a Password   : ")
        confirm  = getpass.getpass("  Confirm Password    : ")

        if password != confirm:
            print("  Passwords do not match. Try again.")
            return False

        # Save new student to users.csv
        new_user = pd.DataFrame([{
            "Username"   : username,
            "Password"   : password,      # plain text (fine for student project)
            "Role"       : "student",
            "Room Number": room_number
        }])
        df = pd.concat([df, new_user], ignore_index=True)
        self._save_users(df)

        print(f"  Account created successfully! Welcome, {username}.")
        return True

    
    #  LOGIN as Student
    #  Returns (username, room_number) on success, or (None, None)
   
    def login_student(self):
        """Verify student credentials from users.csv."""
        print("\n  ── Student Login ──")

        username = input("  Username : ").strip()
        password = getpass.getpass("  Password : ")

        df    = self._load_users()
        match = df[(df["Username"] == username) & (df["Password"] == password)]

        if match.empty:
            print("  Invalid username or password.")
            return None, None

        room_number = match.iloc[0]["Room Number"]
        print(f"  Welcome back, {username}!  (Room {room_number})")
        return username, room_number

    
    #  LOGIN as Warden
    #  Returns True on success, False otherwise
    
    
    def login_warden(self):
        """Verify warden credentials against the hardcoded account."""
        print("\n  ── Warden / Manager Login ──")

        username = input("  Username : ").strip()
        password = getpass.getpass("  Password : ")

        if username == WARDEN_USERNAME and password == WARDEN_PASSWORD:
            print("  Welcome, Warden! You have full management access.")
            return True
        else:
            print("  Invalid warden credentials.")
            return False



#  BASE CLASS: ServiceRequest
#  Common CRUD logic shared by HouseKeeping and Maintenance.
#  Demonstrates INHERITANCE — child classes use these methods.


class ServiceRequest:
    """
    Base class for all service request operations.
    HouseKeeping and Maintenance both inherit from this.
    """

    def __init__(self, csv_file: str, service_type: str):
        self.csv_file     = csv_file       # CSV to read/write data
        self.service_type = service_type   # "Housekeeping" or "Maintenance"
        self._initialize_csv()

    def _initialize_csv(self):
        """Create the CSV with correct headers if missing."""
        if not os.path.exists(self.csv_file):
            pd.DataFrame(columns=CSV_COLUMNS).to_csv(self.csv_file, index=False)

    def _load_data(self) -> pd.DataFrame:
        """Read CSV into DataFrame; handle empty rating cells."""
        df = pd.read_csv(self.csv_file)
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce").fillna(0)
        return df

    def _save_data(self, df: pd.DataFrame):
        """Write DataFrame back to disk."""
        df.to_csv(self.csv_file, index=False)

    # ── STUDENT ACTIONS ────────────────────────────────────────

    def add_request(self, student_name: str, room_number: str):
        """
        Student raises a new service request.
        Name and Room Number are pre-filled from login info.
        """
        print(f"\n  ── Add {self.service_type} Request ──")

        issue = input("  Describe the Issue     : ").strip()

        # Ask for preferred time slot
        print("\n  Preferred Timing:")
        print("    1. Morning   (7 AM  – 12 PM)")
        print("    2. Afternoon (12 PM –  5 PM)")
        print("    3. Evening   (5 PM  –  9 PM)")

        time_choice    = input("  Choose timing [1/2/3]  : ").strip()
        time_map       = {"1": "Morning", "2": "Afternoon", "3": "Evening"}
        preferred_time = time_map.get(time_choice, "Morning")  # default: Morning

        # Build the new row dictionary
        new_row = {
            "Name"          : student_name,
            "Room Number"   : room_number,
            "Issue"         : issue,
            "Preferred Time": preferred_time,
            "Status"        : "Pending",   # all new requests start Pending
            "Rating"        : 0            # no rating yet
        }

        df = self._load_data()
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self._save_data(df)

        print(f"\n  {self.service_type} request submitted!")
        print(f"  Preferred Time : {preferred_time}  |  Status : Pending")

    def view_my_requests(self, student_name: str):
        """Show only the logged-in student's own requests."""
        print(f"\n  ── My {self.service_type} Requests ──")
        df          = self._load_data()
        my_requests = df[df["Name"] == student_name]

        if my_requests.empty:
            print("  You have not submitted any requests yet.")
            return

        my_requests.index = my_requests.index + 1   # show 1-based index
        print(my_requests.to_string())
        print()

    def add_rating(self, student_name: str):
        """
        Student rates a completed service (1–5 stars).
        Only their own completed requests can be rated.
        """
        print(f"\n  ── Rate Your {self.service_type} Service ──")
        df = self._load_data()

        # Only this student's completed requests
        my_done = df[(df["Name"] == student_name) & (df["Status"] == "Completed")]

        if my_done.empty:
            print("  No completed requests available to rate.")
            return

        print("  Your Completed Requests:")
        my_done.index = my_done.index + 1
        print(my_done[["Room Number", "Issue", "Rating"]].to_string())

        try:
            row_num      = int(input("\n  Enter Row Number to rate: ").strip())
            actual_index = row_num - 1

            if actual_index < 0 or actual_index >= len(df):
                print("  Invalid row number.")
                return

            # Verify the row belongs to this student
            if df.loc[actual_index, "Name"] != student_name:
                print("  You can only rate your own requests.")
                return

            if df.loc[actual_index, "Status"] != "Completed":
                print("  This request is not completed yet.")
                return

            rating = float(input("  Enter Rating (1 to 5): ").strip())
            if not (1 <= rating <= 5):
                print("  Rating must be between 1 and 5.")
                return

            df.loc[actual_index, "Rating"] = rating
            self._save_data(df)
            print(f"  Thank you! Rating of {rating} stars saved.")

        except ValueError:
            print("  Please enter valid numbers only.")

    # ── WARDEN ACTIONS ─────────────────────────────────────────

    def view_all_requests(self):
        """Warden sees all requests from every student."""
        print(f"\n  ── All {self.service_type} Requests ──")
        df = self._load_data()

        if df.empty:
            print("  No requests found.")
            return

        df.index = df.index + 1
        print(df.to_string())
        print()

    def mark_completed(self):
        """Warden marks a pending request as Completed."""
        print(f"\n  ── Mark {self.service_type} as Completed ──")
        df      = self._load_data()
        pending = df[df["Status"] == "Pending"]

        if pending.empty:
            print("  No pending requests. All done!")
            return

        print("  Pending Requests:")
        pending.index = pending.index + 1
        print(pending[["Name", "Room Number", "Issue", "Preferred Time"]].to_string())

        try:
            row_num      = int(input("\n  Enter Row Number to mark complete: ").strip())
            actual_index = row_num - 1

            if actual_index < 0 or actual_index >= len(df):
                print("  Invalid row number.")
                return

            if df.loc[actual_index, "Status"] == "Completed":
                print("  Already marked as Completed.")
                return

            df.loc[actual_index, "Status"] = "Completed"
            self._save_data(df)
            print("  Request marked as Completed!")

        except ValueError:
            print("  Please enter a valid number.")

    def calculate_average_rating(self):
        """
        Compute rating statistics using NumPy.
        Shows mean, min, max, and standard deviation.
        """
        print(f"\n  ── {self.service_type} Rating Summary ──")
        df       = self._load_data()
        rated_df = df[df["Rating"] > 0]

        if rated_df.empty:
            print("  No ratings submitted yet.")
            return

        # Convert to NumPy array for numerical operations
        ratings = np.array(rated_df["Rating"], dtype=float)

        avg   = np.mean(ratings)
        mn    = np.min(ratings)
        mx    = np.max(ratings)
        std   = np.std(ratings)
        count = len(ratings)

        print(f"  Total Ratings    : {count}")
        print(f"  Average Rating   : {avg:.2f} / 5.00")
        print(f"  Lowest  Rating   : {mn:.1f}")
        print(f"  Highest Rating   : {mx:.1f}")
        print(f"  Std Deviation    : {std:.2f}")

        # Quick visual star representation
        stars = "★" * int(round(avg)) + "☆" * (5 - int(round(avg)))
        print(f"  Stars            : {stars}")



#  CHILD CLASS: HouseKeeping   (inherits ServiceRequest)


class HouseKeeping(ServiceRequest):
    def __init__(self):
        super().__init__(csv_file=HOUSEKEEPING_FILE, service_type="Housekeeping")

    def student_menu(self, username: str, room_number: str):
        """Sub-menu shown to a student inside Housekeeping module."""
        while True:
            print("\n" + "="*45)
            print("    HOUSEKEEPING MODULE  (Student)")
            print("="*45)
            print("  1. Raise New Request")
            print("  2. View My Requests")
            print("  3. Rate a Completed Service")
            print("  0. Back")
            print("-"*45)
            choice = input("  Choose: ").strip()

            if   choice == "1": self.add_request(username, room_number)
            elif choice == "2": self.view_my_requests(username)
            elif choice == "3": self.add_rating(username)
            elif choice == "0": break
            else: print("  Invalid option.")

    def warden_menu(self):
        """Sub-menu shown to the warden inside Housekeeping module."""
        while True:
            print("\n" + "="*45)
            print("    HOUSEKEEPING MODULE  (Warden)")
            print("="*45)
            print("  1. View All Requests")
            print("  2. Mark Request as Completed")
            print("  3. View Rating Summary")
            print("  0. Back")
            print("-"*45)
            choice = input("  Choose: ").strip()

            if   choice == "1": self.view_all_requests()
            elif choice == "2": self.mark_completed()
            elif choice == "3": self.calculate_average_rating()
            elif choice == "0": break
            else: print("  Invalid option.")



#  CHILD CLASS: Maintenance   (inherits ServiceRequest)


class Maintenance(ServiceRequest):
    def __init__(self):
        super().__init__(csv_file=MAINTENANCE_FILE, service_type="Maintenance")

    def student_menu(self, username: str, room_number: str):
        """Sub-menu shown to a student inside Maintenance module."""
        while True:
            print("\n" + "="*45)
            print("    MAINTENANCE MODULE  (Student)")
            print("="*45)
            print("  1. Raise New Request")
            print("  2. View My Requests")
            print("  3. Rate a Completed Service")
            print("  0. Back")
            print("-"*45)
            choice = input("  Choose: ").strip()

            if   choice == "1": self.add_request(username, room_number)
            elif choice == "2": self.view_my_requests(username)
            elif choice == "3": self.add_rating(username)
            elif choice == "0": break
            else: print("  Invalid option.")

    def warden_menu(self):
        """Sub-menu shown to the warden inside Maintenance module."""
        while True:
            print("\n" + "="*45)
            print("    MAINTENANCE MODULE  (Warden)")
            print("="*45)
            print("  1. View All Requests")
            print("  2. Mark Request as Completed")
            print("  3. View Rating Summary")
            print("  0. Back")
            print("-"*45)
            choice = input("  Choose: ").strip()

            if   choice == "1": self.view_all_requests()
            elif choice == "2": self.mark_completed()
            elif choice == "3": self.calculate_average_rating()
            elif choice == "0": break
            else: print("  Invalid option.")



#  CLASS: ReportGenerator  (Warden only)
#  Combined analysis of both modules using Pandas + NumPy


class ReportGenerator:
    """Generates a full hostel services report for the warden."""

    def generate_summary(self):
        print("\n" + "="*50)
        print("    HOSTEL SERVICES — FULL REPORT")
        print("="*50)

        sections = [
            ("Housekeeping", HOUSEKEEPING_FILE),
            ("Maintenance",  MAINTENANCE_FILE),
        ]

        for label, file in sections:
            print(f"\n  [{label}]")
            print("  " + "-"*40)

            if not os.path.exists(file):
                print("  Data file not found.")
                continue

            df = pd.read_csv(file)
            df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce").fillna(0)

            if df.empty:
                print("  No records yet.")
                continue

            total     = len(df)
            pending   = len(df[df["Status"] == "Pending"])
            completed = len(df[df["Status"] == "Completed"])

            print(f"  Total Requests   : {total}")
            print(f"  Pending          : {pending}")
            print(f"  Completed        : {completed}")

            # Time preference breakdown (Pandas value_counts)
            if "Preferred Time" in df.columns:
                print("  Time Preferences :")
                for slot, cnt in df["Preferred Time"].value_counts().items():
                    print(f"    {slot:12s} -> {cnt} request(s)")

            # Rating statistics (NumPy)
            rated = df[df["Rating"] > 0]["Rating"].values
            if len(rated) > 0:
                r = np.array(rated, dtype=float)
                print(f"  Avg Rating       : {np.mean(r):.2f} / 5.00")
                print(f"  Std Deviation    : {np.std(r):.2f}")
            else:
                print("  Avg Rating       : No ratings yet")

        print("\n" + "="*50)

#  PORTAL FUNCTIONS


def student_portal(auth: AuthManager, hk: HouseKeeping, mt: Maintenance):
    """
    Student portal entry — register or login,
    then access housekeeping and maintenance modules.
    """
    while True:
        print("\n" + "="*45)
        print("    STUDENT PORTAL")
        print("="*45)
        print("  1. Login")
        print("  2. Register New Account")
        print("  0. Back to Main Menu")
        print("-"*45)

        choice = input("  Choose: ").strip()

        if choice == "1":
            username, room_number = auth.login_student()
            if username:
                # Login successful — go to student dashboard
                student_dashboard(username, room_number, hk, mt)

        elif choice == "2":
            auth.register_student()

        elif choice == "0":
            break

        else:
            print("  Invalid option.")


def student_dashboard(username: str, room_number: str,
                      hk: HouseKeeping, mt: Maintenance):
    """
    Dashboard a student sees after logging in.
    Access Housekeeping or Maintenance module.
    """
    while True:
        print("\n" + "="*45)
        print(f"    Welcome, {username}  |  Room {room_number}")
        print("="*45)
        print("  1. Housekeeping Module")
        print("  2. Maintenance Module")
        print("  0. Logout")
        print("-"*45)

        choice = input("  Choose: ").strip()

        if   choice == "1": hk.student_menu(username, room_number)
        elif choice == "2": mt.student_menu(username, room_number)
        elif choice == "0":
            print(f"  Logged out. Goodbye, {username}!")
            break
        else:
            print("  Invalid option.")


def warden_portal(auth: AuthManager, hk: HouseKeeping,
                  mt: Maintenance, reporter: ReportGenerator):
    """
    Warden portal — login with fixed credentials.
    Then access full management dashboard.
    """
    success = auth.login_warden()
    if not success:
        return  # wrong credentials — go back

    # Warden dashboard
    while True:
        print("\n" + "="*45)
        print("    WARDEN / MANAGER DASHBOARD")
        print("="*45)
        print("  1. Housekeeping Module")
        print("  2. Maintenance Module")
        print("  3. Full Summary Report")
        print("  0. Logout")
        print("-"*45)

        choice = input("  Choose: ").strip()

        if   choice == "1": hk.warden_menu()
        elif choice == "2": mt.warden_menu()
        elif choice == "3": reporter.generate_summary()
        elif choice == "0":
            print("  Warden logged out. Goodbye!")
            break
        else:
            print("  Invalid option.")


#  MAIN  →  Program entry point

def main():
    # Instantiate all module objects
    auth     = AuthManager()
    hk       = HouseKeeping()
    mt       = Maintenance()
    reporter = ReportGenerator()

    print("\n" + "*"*50)
    print("    HOSTEL MANAGEMENT SYSTEM")
    print("    Python | OOP | Pandas | NumPy")
    print("*"*50)

    # Top-level: choose role
    while True:
        print("\n" + "="*45)
        print("    SELECT YOUR ROLE")
        print("="*45)
        print("  1. Student Login / Register")
        print("  2. Warden / Manager Login")
        print("  0. Exit")
        print("-"*45)

        choice = input("  Choose: ").strip()

        if   choice == "1": student_portal(auth, hk, mt)
        elif choice == "2": warden_portal(auth, hk, mt, reporter)
        elif choice == "0":
            print("\n  Thank you for using Hostel Management System!")
            print("  Goodbye!\n")
            break
        else:
            print("  Please choose a valid option (0, 1, or 2).")


# Run only when executed directly, not when imported
if __name__ == "__main__":
    main()

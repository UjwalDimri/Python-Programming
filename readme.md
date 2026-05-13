# Hostel Management System 🏨

A Python-based **Hostel Management System** developed using **Object-Oriented Programming (OOP), Pandas, NumPy, and CSV file handling**.  
This project provides a role-based system for **Students** and **Wardens** to manage hostel housekeeping and maintenance requests efficiently.

---

## 📌 Project Overview

The system was designed to solve real hostel problems such as:

- Unscheduled housekeeping visits
- Lack of privacy for students
- No centralized request tracking
- No feedback/rating mechanism

Students can:
- Register/Login
- Raise housekeeping or maintenance requests
- Choose preferred service timings
- Track request status
- Rate completed services

Wardens can:
- View all requests
- Mark requests as completed
- Analyze ratings and reports

The project uses:
- **Python**
- **Pandas**
- **NumPy**
- **CSV files**
- **OOP Concepts** (Inheritance, Classes, Methods)

---

# 🚀 Features

## 👨‍🎓 Student Features
- Student Registration & Login
- Raise Housekeeping Requests
- Raise Maintenance Requests
- Choose Preferred Time Slot
- View Personal Requests
- Rate Completed Services

## 👨‍💼 Warden Features
- Secure Warden Login
- View All Requests
- Mark Requests as Completed
- View Rating Statistics
- Generate Summary Reports

## 📊 Analytics Features
- Average Rating
- Highest & Lowest Rating
- Standard Deviation
- Service Summary Reports using NumPy

---

# 🛠 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core Programming |
| Pandas | CSV Data Handling |
| NumPy | Rating Calculations |
| OOP | System Design |
| CSV Files | Persistent Storage |
| getpass | Hidden Password Input |

---

# 📂 Project Structure

```bash
Hostel-Management-System/
│
├── hostel_management.py      # Main Python Program
├── users.csv                 # Stores student accounts
├── housekeeping.csv          # Housekeeping requests
├── maintenance.csv           # Maintenance requests
└── README.md

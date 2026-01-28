#  STUDENT ATTENDANCE SYSTEM (CONSOLE EDITION)

> **Course:** Software Engineering
> **Version:** 1.0.0
> **Team:** Group 08

---

## 1. INTRODUCTION

**Student Attendance System** is a student attendance management system built on a Command Line Interface (CLI). The project is designed to solve the problem of attendance fraud and optimize the classroom management process at universities.

The system operates based on a **Session-based Authentication Code** mechanism, ensuring that students can only mark attendance when they are physically present in class during the time window authorized by the lecturer.

### Technological Highlights
* **MVC Architecture (Model-View-Controller):** Clear separation between Data, Business Logic, and User Interface.
* **Clean Architecture:** Strictly adheres to Design Patterns and the Software Requirements Specification (SRS).
* **Containerization:** Fully packaged with **Docker**, ensuring consistent performance across all environments (Windows/Linux/MacOS).
* **Database:** Uses SQLite with a normalized design (3NF) to ensure data integrity.

---

## 2. DESIGN MAPPING

The system implementation is strictly mapped to the following design documents:

### 2.1. Use Case Diagram (Functionality)
The system applies Role-Based Access Control (RBAC) for 3 user actors:

| Actor | Use Cases | Detailed Description |
| :--- | :--- | :--- |
| **Admin** | **Manage Users** | Add, delete, and modify Student/Lecturer accounts. |
| | **Manage Classes** | Create subjects, open course classes, assign lecturers. |
| | **System Config** | Configure system parameters. |
| | **View Report** | View institution-wide statistical reports. |
| **Lecturer** | **Create Session** | Create an attendance session and generate a Code (Random 6 digits). |
| | **View Schedule** | View personal teaching schedule. |
| **Student** | **Mark Attendance** | Enter the Code to mark attendance. |
| | **View Schedule** | View personal class schedule. |
| **All** | **Authentication** | Login, Logout, Forgot Password. |

### 2.2. Data Flow Diagram (DFD)
The attendance process complies with **DFD Level 2 - Process 4.0**:
1.  **Input:** Student enters `AuthCode`.
2.  **Validation:** The system checks:
    * Does the Code exist in an currently open `AttendanceSession`?
    * Is the student enrolled in the `Student_Class` list?
3.  **Process:** If valid -> Record data into `AttendanceRecord`.
4.  **Output:** Success/Failure notification.

### 2.3. Class Diagram (Data Structure)
Source code in the `src/models/` directory maps 1-to-1 with the Class Diagram:
* **User:** Parent class (UserID, Email, Password, Role).
* **Student / Lecturer / Admin:** Subclasses inheriting from User.
* **Academic:** Subject, Class, Schedule.
* **Attendance:** AttendanceSession, AttendanceRecord.

---

## 3. INSTALLATION & RUNNING

###  Important Note
Since this is a Console Application (CLI) that requires interactive keyboard input, you **must** use the `docker-compose run` command instead of `docker-compose up`.

### Method 1: Using Docker (Recommended)
This is the fastest method, requiring no manual Python or library installation.

1.  **Open Terminal** at the project root directory.
2.  **Build and Run:**
    ```bash
    docker-compose run --rm app
    ```
    *(`--rm` automatically removes the container after the program exits)*

3.  **Cleanup (if needed):**
    ```bash
    docker-compose down
    ```

### Method 2: Manual Setup
For development environments or systems without Docker.

1.  **Requirement:** Python 3.8 or higher.
2.  **Create Virtual Environment:**
    ```bash
    # Linux/MacOS
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run Application:**
    ```bash
    python main.py
    ```

---

## 4. USER GUIDE

### Default Credentials
Upon the first run, the system automatically creates an Admin account for you to set up the system:

* **Role:** Admin
* **Username:** `admin`
* **Password:** `123456`

### Testing Flow

1.  **Step 1 (Admin):** Login as Admin -> Create Subject -> Create Class -> Create Lecturer & Student accounts.
2.  **Step 2 (Lecturer):** Login as Lecturer -> Select "Create Attendance Session" -> Receive Code (e.g., `123456`).
3.  **Step 3 (Student):** Login as Student -> Select "Mark Attendance" -> Enter Code `123456`.
4.  **Step 4 (Admin/Lecturer):** View Report to verify attendance results.

---
**Copyright © 2026 - Group 08.**
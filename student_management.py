import sqlite3

# Connect to the database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create the students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL
)
""")
conn.commit()


def add_student():
    try:
        roll_no = int(input("Enter Roll Number: "))
        name = input("Enter Student Name: ").strip()
        department = input("Enter Department: ").strip()

        if not name or not department:
            print("Name and department cannot be empty!")
            return

        cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?)",
            (roll_no, name, department)
        )
        conn.commit()
        print("Student added successfully!")

    except ValueError:
        print("Roll number must be a number!")
    except sqlite3.IntegrityError:
        print("This roll number already exists!")


def view_students():
    cursor.execute("SELECT * FROM students ORDER BY roll_no")
    students = cursor.fetchall()

    if not students:
        print("No student records found.")
        return

    print("\n--- Student Records ---")
    for student in students:
        print(
            f"Roll No: {student[0]} | "
            f"Name: {student[1]} | "
            f"Department: {student[2]}"
        )


def search_student():
    try:
        roll_no = int(input("Enter Roll Number to Search: "))
        cursor.execute(
            "SELECT * FROM students WHERE roll_no = ?",
            (roll_no,)
        )
        student = cursor.fetchone()

        if student:
            print("\nStudent Found!")
            print(f"Roll Number: {student[0]}")
            print(f"Name: {student[1]}")
            print(f"Department: {student[2]}")
        else:
            print("Student not found!")

    except ValueError:
        print("Roll number must be a number!")


def update_student():
    try:
        roll_no = int(input("Enter Roll Number to Update: "))

        cursor.execute(
            "SELECT * FROM students WHERE roll_no = ?",
            (roll_no,)
        )

        if not cursor.fetchone():
            print("Student not found!")
            return

        name = input("Enter New Name: ").strip()
        department = input("Enter New Department: ").strip()

        if not name or not department:
            print("Name and department cannot be empty!")
            return

        cursor.execute(
            """UPDATE students
               SET name = ?, department = ?
               WHERE roll_no = ?""",
            (name, department, roll_no)
        )
        conn.commit()
        print("Student updated successfully!")

    except ValueError:
        print("Roll number must be a number!")


def delete_student():
    try:
        roll_no = int(input("Enter Roll Number to Delete: "))

        cursor.execute(
            "DELETE FROM students WHERE roll_no = ?",
            (roll_no,)
        )
        conn.commit()

        if cursor.rowcount > 0:
            print("Student deleted successfully!")
        else:
            print("Student not found!")

    except ValueError:
        print("Roll number must be a number!")


def main():
    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("Thank you for using Student Management System!")
            break
        else:
            print("Invalid choice! Please enter a number from 1 to 6.")


if __name__ == "__main__":
    try:
        main()
    finally:
        conn.close()
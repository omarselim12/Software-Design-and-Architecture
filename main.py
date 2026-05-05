"""
Student Course Registration System
Design Patterns Assignment
Patterns used: Singleton, Prototype, Factory Method
Language: Python
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from copy import deepcopy
from datetime import datetime
from typing import Dict, List


# ============================================================
# 1) SINGLETON PATTERN
# Ensures that the whole system uses one shared logger instance.
# ============================================================

class SystemLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemLogger, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        self.logs.append(log_message)
        print(log_message)

    def show_logs(self) -> None:
        print("\n--- SYSTEM LOGS ---")
        for log in self.logs:
            print(log)


# ============================================================
# 2) PROTOTYPE PATTERN
# Allows the system to clone existing course templates and modify
# the copy instead of creating each course section from scratch.
# ============================================================

class CoursePrototype:
    def __init__(self, code: str, title: str, credit_hours: int, topics: List[str]):
        self.code = code
        self.title = title
        self.credit_hours = credit_hours
        self.topics = topics
        self.section = None
        self.instructor = None
        self.capacity = 30

    def clone(self) -> "CoursePrototype":
        return deepcopy(self)

    def customize_section(self, section: str, instructor: str, capacity: int) -> None:
        self.section = section
        self.instructor = instructor
        self.capacity = capacity

    def display(self) -> None:
        print(
            f"Course: {self.code} - {self.title} | "
            f"Section: {self.section} | Instructor: {self.instructor} | "
            f"Capacity: {self.capacity} | Topics: {', '.join(self.topics)}"
        )


# ============================================================
# 3) FACTORY METHOD PATTERN
# Creates different user account objects without making the client
# code depend directly on concrete user classes.
# ============================================================

class User(ABC):
    def __init__(self, name: str, user_id: str):
        self.name = name
        self.user_id = user_id

    @abstractmethod
    def get_role(self) -> str:
        pass

    def display_info(self) -> None:
        print(f"{self.get_role()} Account -> Name: {self.name}, ID: {self.user_id}")


class Student(User):
    def get_role(self) -> str:
        return "Student"


class Instructor(User):
    def get_role(self) -> str:
        return "Instructor"


class Admin(User):
    def get_role(self) -> str:
        return "Admin"


class UserFactory(ABC):
    @abstractmethod
    def create_user(self, name: str, user_id: str) -> User:
        pass

    def register_user(self, name: str, user_id: str) -> User:
        user = self.create_user(name, user_id)
        SystemLogger().log(f"Created {user.get_role()} account for {name}.")
        return user


class StudentFactory(UserFactory):
    def create_user(self, name: str, user_id: str) -> User:
        return Student(name, user_id)


class InstructorFactory(UserFactory):
    def create_user(self, name: str, user_id: str) -> User:
        return Instructor(name, user_id)


class AdminFactory(UserFactory):
    def create_user(self, name: str, user_id: str) -> User:
        return Admin(name, user_id)


# ============================================================
# Course Registration System
# ============================================================

class CourseRegistrationSystem:
    def __init__(self):
        self.logger = SystemLogger()
        self.users: Dict[str, User] = {}
        self.courses: List[CoursePrototype] = []

    def add_user(self, user: User) -> None:
        self.users[user.user_id] = user
        self.logger.log(f"User {user.name} added to the registration system.")

    def add_course_section(self, course: CoursePrototype) -> None:
        self.courses.append(course)
        self.logger.log(f"Course section {course.code}-{course.section} added.")

    def show_users(self) -> None:
        print("\n--- REGISTERED USERS ---")
        for user in self.users.values():
            user.display_info()

    def show_courses(self) -> None:
        print("\n--- AVAILABLE COURSE SECTIONS ---")
        for course in self.courses:
            course.display()


# ============================================================
# Client Code
# ============================================================

def main() -> None:
    system = CourseRegistrationSystem()

    # Factory Method usage
    student_factory = StudentFactory()
    instructor_factory = InstructorFactory()
    admin_factory = AdminFactory()

    student = student_factory.register_user("Ahmed Ali", "S1001")
    instructor = instructor_factory.register_user("Dr. Mona Hassan", "I2001")
    admin = admin_factory.register_user("System Admin", "A3001")

    system.add_user(student)
    system.add_user(instructor)
    system.add_user(admin)

    # Prototype usage
    software_design_template = CoursePrototype(
        code="SDA301",
        title="Software Design and Architecture",
        credit_hours=3,
        topics=["Clean Code", "Design Patterns", "Software Architecture"]
    )

    section_a = software_design_template.clone()
    section_a.customize_section("A", "Dr. Mona Hassan", 35)

    section_b = software_design_template.clone()
    section_b.customize_section("B", "Dr. Karim Nabil", 30)

    system.add_course_section(section_a)
    system.add_course_section(section_b)

    # Output
    system.show_users()
    system.show_courses()

    # Singleton verification
    logger_one = SystemLogger()
    logger_two = SystemLogger()
    print("\nSingleton test: logger_one is logger_two ->", logger_one is logger_two)

    system.logger.show_logs()


if __name__ == "__main__":
    main()

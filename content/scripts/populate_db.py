from content.models import (
    Courses,
    Lecture,
    Homework,
    TeacherProfile,
    StudentProfile,
    HomeWorkSubmission,
    Grade,
    GradeComment,
)
from access.models import User
from django.db import transaction
import random
from decimal import Decimal


def run():

    with transaction.atomic():

        # ----------------- TEACHERS -----------------
        teachers_data = [
            ("tch1", "tch1pass", "G. Saldadze"),
            ("tch2", "tch2pass", "E. Jones"),
            ("tch3", "tch3pass", "J. Black"),
            ("tch4", "tch4pass", "M. White"),
            ("tch5", "tch5pass", "A. Smith"),
            ("tch6", "tch6pass", "L. Brown"),
            ("tch7", "tch7pass", "C. Green"),
            ("tch8", "tch8pass", "D. Grey"),
            ("tch9", "tch9pass", "F. Blue"),
            ("tch10", "tch10pass", "K. Yellow"),
            ("tch11", "tch11pass", "S. Black"),
            ("tch12", "tch12pass", "T. White"),
            ("tch13", "tch13pass", "R. Red"),
            ("tch14", "tch14pass", "P. Purple"),
            ("tch15", "tch15pass", "O. Orange"),
        ]

        for username, password, name in teachers_data:
            User.objects.create_user(
                username=username, password=password, role=User.Roles.TEACHER, name=name
            )

        # ----------------- STUDENTS -----------------
        students_data = [
            ("std1", "std1pass", "G. Saldadze"),
            ("std2", "std2pass", "A. Doe"),
            ("std3", "std3pass", "B. James"),
            ("std4", "std4pass", "C. Vascez"),
            ("std5", "std5pass", "D. Khatiashvili"),
            ("std6", "std6pass", "E. Kore"),
            ("std7", "std7pass", "F. Wilson"),
            ("std8", "std8pass", "G. Moore"),
            ("std9", "std9pass", "H. Taylor"),
            ("std10", "std10pass", "I. Anderson"),
            ("std11", "std11pass", "J. Thomas"),
            ("std12", "std12pass", "K. Jackson"),
            ("std13", "std13pass", "L. White"),
            ("std14", "std14pass", "M. Harris"),
            ("std15", "std15pass", "N. Martin"),
            ("std16", "std16pass", "O. Lee"),
            ("std17", "std17pass", "P. Walker"),
            ("std18", "std18pass", "Q. Hall"),
            ("std19", "std19pass", "R. Allen"),
            ("std20", "std20pass", "S. Young"),
            ("std21", "std21pass", "T. Hernandez"),
            ("std22", "std22pass", "U. King"),
            ("std23", "std23pass", "V. Wright"),
            ("std24", "std24pass", "W. Lopez"),
            ("std25", "std25pass", "X. Hill"),
            ("std26", "std26pass", "Y. Scott"),
            ("std27", "std27pass", "Z. Green"),
            ("std28", "std28pass", "A. Adams"),
            ("std29", "std29pass", "B. Baker"),
            ("std30", "std30pass", "C. Nelson"),
        ]

        for username, password, name in students_data:
            User.objects.create_user(
                username=username, password=password, role=User.Roles.STUDENT, name=name
            )

        # Get all teacher and student profiles
        teachers = list(TeacherProfile.objects.all())
        students = list(StudentProfile.objects.all())

        # ----------------- COURSES -----------------
        courses_data = [
            {
                "name": "Python Development Course",
                "teacher": teachers[0],
                "helpers": [teachers[1], teachers[2]],
                "students": students[:10],
                "available": True,
            },
            {
                "name": "JavaScript Development Course",
                "teacher": teachers[1],
                "helpers": [teachers[0], teachers[3]],
                "students": students[5:15],
                "available": True,
            },
            {
                "name": "DevOps Course",
                "teacher": teachers[2],
                "helpers": [teachers[4], teachers[5]],
                "students": students[10:20],
                "available": True,
            },
            {
                "name": "Data Science with Python",
                "teacher": teachers[3],
                "helpers": [teachers[6]],
                "students": students[15:25],
                "available": True,
            },
            {
                "name": "Web Development Fundamentals",
                "teacher": teachers[4],
                "helpers": [teachers[7], teachers[8]],
                "students": students[20:30],
                "available": True,
            },
            {
                "name": "Advanced Algorithms",
                "teacher": teachers[5],
                "helpers": [teachers[9]],
                "students": students[0:8] + students[25:30],
                "available": True,
            },
            {
                "name": "Mobile App Development",
                "teacher": teachers[6],
                "helpers": [teachers[10]],
                "students": students[5:12] + students[20:25],
                "available": False,  # Not available
            },
        ]

        courses = []
        for course_data in courses_data:
            course = Courses.objects.create(
                name=course_data["name"],
                teacher=course_data["teacher"],
                available=course_data["available"],
            )
            course.helpers.set(course_data["helpers"])
            course.student.set(course_data["students"])
            courses.append(course)

        # ----------------- LECTURES -----------------
        lectures_data = [
            # Python Development Course lectures
            {"course": courses[0], "topic": "Introduction to Python"},
            {"course": courses[0], "topic": "Python Data Structures"},
            {"course": courses[0], "topic": "Object-Oriented Programming in Python"},
            {"course": courses[0], "topic": "Python Modules and Packages"},
            {"course": courses[0], "topic": "File Handling in Python"},
            {"course": courses[0], "topic": "Error Handling and Exceptions"},
            {"course": courses[0], "topic": "Working with APIs in Python"},
            {"course": courses[0], "topic": "Introduction to Django Framework"},
            {"course": courses[0], "topic": "Django Models and ORM"},
            {"course": courses[0], "topic": "Django Views and Templates"},
            # JavaScript Development Course lectures
            {"course": courses[1], "topic": "JavaScript Fundamentals"},
            {"course": courses[1], "topic": "DOM Manipulation"},
            {"course": courses[1], "topic": "JavaScript ES6 Features"},
            {"course": courses[1], "topic": "Asynchronous JavaScript"},
            {"course": courses[1], "topic": "JavaScript Design Patterns"},
            {"course": courses[1], "topic": "Introduction to Node.js"},
            {"course": courses[1], "topic": "Express.js Framework"},
            {"course": courses[1], "topic": "Working with Databases in Node.js"},
            {"course": courses[1], "topic": "RESTful API Development"},
            {"course": courses[1], "topic": "Authentication and Authorization"},
            # DevOps Course lectures
            {"course": courses[2], "topic": "Introduction to DevOps"},
            {"course": courses[2], "topic": "Version Control with Git"},
            {
                "course": courses[2],
                "topic": "Continuous Integration/Continuous Deployment",
            },
            {"course": courses[2], "topic": "Containerization with Docker"},
            {"course": courses[2], "topic": "Orchestration with Kubernetes"},
            {"course": courses[2], "topic": "Infrastructure as Code with Terraform"},
            {"course": courses[2], "topic": "Monitoring and Logging"},
            {"course": courses[2], "topic": "Cloud Platforms Overview"},
            # Other courses lectures
            {"course": courses[3], "topic": "Introduction to Data Science"},
            {"course": courses[3], "topic": "Data Analysis with Pandas"},
            {
                "course": courses[3],
                "topic": "Data Visualization with Matplotlib and Seaborn",
            },
            {"course": courses[4], "topic": "HTML5 and CSS3 Fundamentals"},
            {"course": courses[4], "topic": "Responsive Web Design"},
            {"course": courses[4], "topic": "Introduction to Bootstrap"},
            {"course": courses[5], "topic": "Algorithm Analysis and Complexity"},
            {"course": courses[5], "topic": "Sorting and Searching Algorithms"},
            {"course": courses[5], "topic": "Graph Algorithms"},
            {"course": courses[6], "topic": "Introduction to Mobile Development"},
            {"course": courses[6], "topic": "React Native Fundamentals"},
        ]

        lectures = []
        for lecture_data in lectures_data:
            lecture = Lecture.objects.create(
                course=lecture_data["course"], topic=lecture_data["topic"]
            )
            lectures.append(lecture)

        # ----------------- HOMEWORK -----------------
        homework_data = [
            # Python course homework
            {
                "lecture": lectures[0],
                "title": "Python Basics Exercise",
                "description": "Write a program that takes user input and performs basic operations.",
            },
            {
                "lecture": lectures[1],
                "title": "Data Structures Implementation",
                "description": "Implement common data structures like stacks, queues, and linked lists in Python.",
            },
            {
                "lecture": lectures[2],
                "title": "OOP Banking System",
                "description": "Create a banking system using classes for accounts, customers, and transactions.",
            },
            {
                "lecture": lectures[3],
                "title": "Package Management Exercise",
                "description": "Create a Python package with multiple modules and demonstrate its usage.",
            },
            {
                "lecture": lectures[4],
                "title": "File Processing Task",
                "description": "Write a program that reads from a CSV file, processes the data, and writes to a new file.",
            },
            {
                "lecture": lectures[5],
                "title": "Exception Handling Practice",
                "description": "Create a program that demonstrates proper exception handling techniques.",
            },
            {
                "lecture": lectures[6],
                "title": "API Integration Project",
                "description": "Build a program that fetches data from a public API and processes it.",
            },
            {
                "lecture": lectures[7],
                "title": "Django Setup Task",
                "description": "Set up a basic Django project with a simple view.",
            },
            {
                "lecture": lectures[8],
                "title": "Django Models Exercise",
                "description": "Create models for a blog application with posts, comments, and categories.",
            },
            {
                "lecture": lectures[9],
                "title": "Django Templates Assignment",
                "description": "Create templates for the blog application with proper template inheritance.",
            },
            # JavaScript course homework
            {
                "lecture": lectures[10],
                "title": "JavaScript Basics",
                "description": "Complete exercises on variables, data types, and basic operations.",
            },
            {
                "lecture": lectures[11],
                "title": "DOM Manipulation Project",
                "description": "Create an interactive web page with JavaScript DOM manipulation.",
            },
            {
                "lecture": lectures[12],
                "title": "ES6 Features Implementation",
                "description": "Rewrite older JavaScript code using ES6 features like arrow functions, destructuring, etc.",
            },
            {
                "lecture": lectures[13],
                "title": "Async JavaScript Exercise",
                "description": "Create a program that uses Promises and async/await for asynchronous operations.",
            },
            {
                "lecture": lectures[14],
                "title": "Design Patterns Implementation",
                "description": "Implement common JavaScript design patterns in a sample application.",
            },
            {
                "lecture": lectures[15],
                "title": "Node.js Basics",
                "description": "Create a simple Node.js server that responds to HTTP requests.",
            },
            {
                "lecture": lectures[16],
                "title": "Express.js REST API",
                "description": "Build a RESTful API using Express.js with CRUD operations.",
            },
            {
                "lecture": lectures[17],
                "title": "Database Integration",
                "description": "Connect your Express.js application to a database and perform operations.",
            },
            {
                "lecture": lectures[18],
                "title": "API Authentication",
                "description": "Implement JWT authentication for your REST API.",
            },
            # DevOps course homework
            {
                "lecture": lectures[20],
                "title": "Git Workflow Exercise",
                "description": "Practice Git branching, merging, and conflict resolution.",
            },
            {
                "lecture": lectures[21],
                "title": "CI/CD Pipeline Setup",
                "description": "Set up a basic CI/CD pipeline for a sample application.",
            },
            {
                "lecture": lectures[22],
                "title": "Docker Containerization",
                "description": "Dockerize a simple web application.",
            },
            {
                "lecture": lectures[23],
                "title": "Kubernetes Deployment",
                "description": "Deploy your Dockerized application to a Kubernetes cluster.",
            },
            {
                "lecture": lectures[24],
                "title": "Terraform Infrastructure",
                "description": "Use Terraform to define and provision cloud infrastructure.",
            },
            # Other courses homework
            {
                "lecture": lectures[28],
                "title": "Pandas Data Analysis",
                "description": "Perform data analysis on a dataset using Pandas.",
            },
            {
                "lecture": lectures[29],
                "title": "Data Visualization Project",
                "description": "Create meaningful visualizations from a dataset.",
            },
            {
                "lecture": lectures[30],
                "title": "Responsive Web Design",
                "description": "Create a responsive web page using HTML and CSS.",
            },
            {
                "lecture": lectures[32],
                "title": "Algorithm Implementation",
                "description": "Implement and analyze sorting algorithms.",
            },
        ]

        homeworks = []
        for hw_data in homework_data:
            homework = Homework.objects.create(
                lecture=hw_data["lecture"],
                title=hw_data["title"],
                description=hw_data["description"],
            )
            homeworks.append(homework)

        # ----------------- HOMEWORK SUBMISSIONS -----------------
        submission_statuses = [
            HomeWorkSubmission.Status.SUBMITED,
            HomeWorkSubmission.Status.GRADED,
            HomeWorkSubmission.Status.RESUBMITED,
        ]

        submission_texts = [
            "I've completed the assignment as requested.",
            "Here is my submission. Please let me know if you need anything else.",
            "I faced some challenges but managed to complete the task.",
            "This was an interesting assignment. I learned a lot.",
            "I followed all the instructions carefully. Hope it meets expectations.",
            "I enjoyed working on this homework. Looking forward to feedback.",
            "I've attached my solution. Please review.",
            "I implemented the required functionality with some additional features.",
            "This assignment helped me understand the concepts better.",
            "I've tested my solution and it works as expected.",
        ]

        # Create submissions for a subset of students and homeworks
        for homework in homeworks:
            # Get students enrolled in this course
            course_students = homework.lecture.course.student.all()

            # Create submissions for a random subset of students (60-80%)
            num_submissions = random.randint(
                int(len(course_students) * 0.6), int(len(course_students) * 0.8)
            )

            selected_students = random.sample(list(course_students), num_submissions)

            for student in selected_students:
                status = random.choice(submission_statuses)
                submission = HomeWorkSubmission.objects.create(
                    homework=homework,
                    student=student,
                    text_submission=random.choice(submission_texts),
                    status=status,
                )

                # Create grades for some submissions
                if status == HomeWorkSubmission.Status.GRADED:
                    points = Decimal(random.uniform(60, 100)).quantize(Decimal("0.01"))
                    grade = Grade.objects.create(
                        submission=submission,
                        points=points,
                        graded=True,
                        feedback=f"Good work overall. Score: {points}/100",
                    )

                    # Add comments for some grades
                    if random.random() < 0.3:  # 30% chance of having comments
                        commenters = random.sample(teachers, random.randint(1, 2))
                        for commenter in commenters:
                            GradeComment.objects.create(
                                grade=grade,
                                author=commenter.user,
                                text=random.choice(
                                    [
                                        "Well structured code but could use more comments.",
                                        "Excellent implementation of the required functionality.",
                                        "Some edge cases were not handled properly.",
                                        "Very creative solution to the problem.",
                                        "Good understanding of the concepts demonstrated.",
                                        "Could benefit from better error handling.",
                                        "Clean and efficient code. Well done!",
                                        "Consider refactoring for better performance.",
                                        "All requirements were met satisfactorily.",
                                        "Great work! Keep it up.",
                                    ]
                                ),
                            )

        print("Database populated successfully")

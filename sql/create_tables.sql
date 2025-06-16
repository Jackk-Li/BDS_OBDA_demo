-- Create university demo database
CREATE DATABASE IF NOT EXISTS university_demo CHARACTER SET utf8mb4;
USE university_demo;

-- Employee table (managed by HR department)
DROP TABLE IF EXISTS teaching_records;
DROP TABLE IF EXISTS graduate_students;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    department VARCHAR(50),
    position VARCHAR(50),
    salary DECIMAL(10,2)
);

-- Teaching records table (managed by academic affairs department)
CREATE TABLE teaching_records (
    record_id INT PRIMARY KEY,
    emp_id INT,
    course_code VARCHAR(20),
    course_name VARCHAR(100),
    semester VARCHAR(20),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);

-- Student table (managed by student registration department)
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    major VARCHAR(50),
    year INT,
    advisor_id INT,
    FOREIGN KEY (advisor_id) REFERENCES employees(emp_id)
);

-- Graduate students table (managed by graduate school)
CREATE TABLE graduate_students (
    student_id INT PRIMARY KEY,
    thesis_title VARCHAR(200),
    defense_date DATE,
    research_area VARCHAR(100),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Insert sample data
INSERT INTO employees VALUES 
(1, 'Alice Wang', 'alice@uni.edu', 'Computer Science', 'Professor', 120000),
(2, 'Bob Chen', 'bob@uni.edu', 'Computer Science', 'Associate Professor', 90000),
(3, 'Carol Liu', 'carol@uni.edu', 'Mathematics', 'Professor', 115000),
(4, 'David Zhang', 'david@uni.edu', 'Computer Science', 'Lecturer', 70000),
(5, 'Emma Li', 'emma@uni.edu', 'Administration', 'Staff', 50000);

INSERT INTO teaching_records VALUES
(1, 1, 'CS101', 'Introduction to Programming', '2024 Fall'),
(2, 1, 'CS501', 'Advanced Algorithms', '2024 Fall'),
(3, 2, 'CS201', 'Data Structures', '2024 Fall'),
(4, 3, 'MATH101', 'Calculus I', '2024 Fall'),
(5, 4, 'CS101', 'Introduction to Programming', '2024 Fall');

INSERT INTO students VALUES
(101, 'Frank Zhou', 'frank@stu.uni.edu', 'Computer Science', 2022, 1),
(102, 'Grace Ma', 'grace@stu.uni.edu', 'Computer Science', 2023, 2),
(103, 'Henry Wu', 'henry@stu.uni.edu', 'Mathematics', 2022, 3),
(104, 'Ivy Chen', 'ivy@stu.uni.edu', 'Computer Science', 2021, 1);

INSERT INTO graduate_students VALUES
(104, 'Machine Learning for Healthcare', '2024-06-15', 'Artificial Intelligence');

-- Create some views for validation
CREATE OR REPLACE VIEW v_all_people AS
SELECT emp_id as id, name, email, 'employee' as type FROM employees
UNION ALL
SELECT student_id as id, name, email, 'student' as type FROM students;

CREATE OR REPLACE VIEW v_academic_staff AS
SELECT * FROM employees 
WHERE position IN ('Professor', 'Associate Professor', 'Lecturer');

CREATE OR REPLACE VIEW v_teachers AS
SELECT DISTINCT e.* 
FROM employees e
JOIN teaching_records t ON e.emp_id = t.emp_id;

-- Display data statistics
SELECT 'Employees' as table_name, COUNT(*) as count FROM employees
UNION ALL
SELECT 'Students', COUNT(*) FROM students
UNION ALL
SELECT 'Graduate Students', COUNT(*) FROM graduate_students
UNION ALL
SELECT 'Teaching Records', COUNT(*) FROM teaching_records;

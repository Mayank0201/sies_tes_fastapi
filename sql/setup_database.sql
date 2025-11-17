CREATE DATABASE sies_tes;
USE sies_tes;

CREATE TABLE streams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO streams (name) VALUES 
('Arts'),
('Science'),
('Commerce');

desc streams;
select * from streams;

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    stream_id INT,
    FOREIGN KEY (stream_id) REFERENCES streams(id)
);

INSERT INTO courses (course_name, stream_id) VALUES
('B.A.M.M.C. (Bachelor of Arts in Mass Media and Communication)', 1),

('B.Sc. in Computer Science', 2),
('B.Sc. in Information Technology', 2),
('B.Sc. in Packaging Technology', 2),
('B.Sc. in Environmental Science', 2),
('B.Sc. in Data Science', 2),

('B.Com. (Bachelor of Commerce)', 3),
('B.Com. (Accounting & Finance)', 3),
('B.Com. (Banking & Insurance)', 3),
('B.Com. (Financial Markets)', 3),
('B.M.S. (Bachelor of Management Studies)', 3),
('B.Com. (Management Accounting with Finance)', 3),
('B.Com. (Entrepreneurship)', 3);

-- Postgraduate Courses
INSERT INTO courses (course_name, stream_id) VALUES
('M.Sc. in Computer Science', 2),
('M.Sc. in Information Technology', 2),
('M.Sc. in Environmental Science', 2),

('M.A. in Business Economics', 1),
('M.A. in Journalism and Mass Communication', 1),

('M.Com. (Advanced Accountancy)', 3),
('M.Com. in Business Management', 3);

desc courses;
select * from courses;

CREATE TABLE classes (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(50) NOT NULL,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL
);

INSERT INTO classes (class_name, course_id) VALUES
-- B.A.M.M.C.
('FYBMM', 1), ('SYBMM', 1), ('TYBMM', 1),

-- B.Sc. in Information Technology
('FYBSCIT', 3), ('SYBSCIT', 3), ('TYBSCIT', 3),

-- B.Sc. in Computer Science
('FYBSCCS', 2), ('SYBSCCS', 2), ('TYBSCCS', 2),

-- B.Sc. in Packaging Technology
('FYBSCPT', 4), ('SYBSCPT', 4), ('TYBSCPT', 4),

-- B.Sc. in Environmental Science
('FYBSCES', 5), ('SYBSCES', 5), ('TYBSCES', 5),

-- B.Sc. in Data Science
('FYBSCDS', 6), ('SYBSCDS', 6), ('TYBSCDS', 6),

-- B.Com. (Bachelor of Commerce)
('FYBCOM', 7), ('SYBCOM', 7), ('TYBCOM', 7),

-- B.Com. (Accounting & Finance)
('FYBAF', 8), ('SYBAF', 8), ('TYBAF', 8),

-- B.Com. (Banking & Insurance)
('FYBBI', 9), ('SYBBI', 9), ('TYBBI', 9),

-- B.Com. (Financial Markets)
('FYBFM', 10), ('SYBFM', 10), ('TYBFM', 10),

-- B.M.S. (Bachelor of Management Studies)
('FYBMS', 11), ('SYBMS', 11), ('TYBMS', 11),

-- B.Com. (Management Accounting with Finance)
('FYBMAF', 12), ('SYBMAF', 12), ('TYBMAF', 12),

-- B.Com. (Entrepreneurship)
('FYBE', 13), ('SYBE', 13), ('TYBE', 13),

-- M.A. in Business Economics
('PART1MABE', 14), ('PART2MABE', 14),

-- M.A. in Journalism and Mass Communication
('PART1MAJMC', 15), ('PART2MAJMC', 15),

-- M.Sc. in Information Technology
('PART1MSCIT', 16), ('PART2MSCIT', 16),

-- M.Sc. in Computer Science
('PART1MSCCS', 17), ('PART2MSCCS', 17),

-- M.Sc. in Environmental Science
('PART1MSCES', 18), ('PART2MSCES', 18),

-- M.Com. (Advanced Accountancy)
('PART1MCOMAA', 19), ('PART2MCOMAA', 19),

-- M.Com. in Business Management
('PART1MCOMBM', 20), ('PART2MCOMBM', 20);

desc classes;
select * from classes;

CREATE TABLE subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL
);

CREATE TABLE teachers (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE teacher_subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT NOT NULL,
    subject_id INT NOT NULL,
    class_id INT NOT NULL,
    teaching_type ENUM('Theory', 'Practical') NOT NULL DEFAULT 'Theory',
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE
);

INSERT INTO subjects (subject_name)
VALUES
('Database Systems'), 
('Database Systems Practical'), 
('Computer Networks'), 
('Computer Networks Practical'), 
('Operating Systems'), 
('Operating Systems Practical'), 
('Software Engineering'), 
('Web Development'), 
('Web Development Practical'),
('Data Structures'), 
('Data Structures Practical'),
('Artificial Intelligence'),
('Artificial Intelligence Practical'),
('Information and Cybersecurity'),
('Information and Cybersecurity Practical'),
('Linux Server Administration'),
('Linux Server Administration Practical'),
('Science of Language Processing'),
('Statistical Methods'),
('Statistical Methods Practical');

INSERT INTO teachers (name)
VALUES
('Dr. Anu Thomas'), 
('Ms. Sameera Ibrahim'), 
('Ms. Minal Sarode'), 
('Ms. Rashmi Prabha'), 
('Dr. Meghna Bhatia'), 
('Ms. Arti Bansode'), 
('Ms. Shaima Thange'),
('Dr. Sheeja K'), 
('Dr. Aditya Jinturkar'), 
('Dr. Rajeshri Shinkar'), 
('Dr. Pallavi Awate'), 
('Ms. Flosia Simon'), 
('Ms. Fatema Kothari'), 
('Dr. Trupti Wani'),
('Ms. Shrutika Jadhav'),
('Ms. Dipti Patil');

INSERT INTO teacher_subjects (teacher_id, subject_id, class_id, teaching_type)
VALUES
(1, 1, 6, 'Theory'), 
(1, 2, 6, 'Practical'), 
(2, 2, 6, 'Practical'), 
(3, 3, 6, 'Theory'),
(3, 4, 6, 'Practical'), 
(4, 5, 6, 'Theory'), 
(5, 6, 6, 'Theory'), 
(5, 7, 6, 'Practical'), 
(6, 8, 6, 'Theory'), 
(6, 9, 6, 'Practical'), 
(7, 10, 6, 'Theory'), 
(7, 11, 6, 'Practical'),
(8, 12, 9, 'Theory'), 
(8, 13, 9, 'Practical'),
(10, 14, 9, 'Theory'),  
(10, 15, 9, 'Practical'),
(9, 16, 9, 'Theory'),  
(9, 17, 9, 'Practical'),
(12, 18, 9, 'Theory'),  
(11, 19, 9, 'Theory'),   
(11, 20, 9, 'Practical');

CREATE TABLE students (
    student_id int PRIMARY KEY auto_increment,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(10) UNIQUE NOT NULL,
    class_id INT,
    password VARCHAR(255) NOT NULL,
    admission_year INT NOT NULL,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE SET NULL
);

desc students;
select * from students;

CREATE TABLE eligibility (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    is_eligible BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

desc eligibility;
select * from eligibility;

CREATE TABLE questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    question_text VARCHAR(255) NOT NULL,
    class_id INT, -- optional (if some questions differ by class)
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE
);

desc questions;
select * from questions;

CREATE TABLE feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    teacher_subject_id INT NOT NULL,
    question_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_subject_id) REFERENCES teacher_subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
);


desc feedback;
select * from feedback;

create table admins (
    admin_id int auto_increment primary key,
    admin_name varchar(100) not null,
    admin_password varchar(255) not null,
    admin_email varchar(255) not null
);

alter table admins
add column course_id int,
add foreign key (course_id) references courses(course_id);

desc admins;
select * from admins;

show tables;
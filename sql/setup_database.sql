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

-- You can switch it with your subject to see if it is working
INSERT INTO subjects (subject_id, subject_name)
VALUES (1, 'Artificial Intelligence'), (2, 'Artificial Intelligence Practical'), (3, 'Data Storage Techniques'), (4, 'Data Storage Techniques Practical'), (5, 'Cryptography in Ancient India'), (6, 'Information and Network Security'), (7, 'Information and Network Security Practical'), (8, 'Java Script and Allied Technologies - I'), (9, 'Java Script and Allied Technologies - I Practical'), (10,'Decision Making Techniques'), (11,'Decision Making Techniques Practical');

desc subjects;
select * from subjects;

CREATE TABLE class_subjects (
    class_id INT NOT NULL,
    subject_id INT NOT NULL,
    PRIMARY KEY (class_id, subject_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

-- This has to be done manually in Database, but we have to make it dynamically for the admin.
insert into class_subjects(class_id, subject_id) values (6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),(6,10),(6,11);

desc class_subjects;
select * from class_subjects;

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

CREATE TABLE teachers (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

INSERT INTO teachers (teacher_id, name)
VALUES (1,'Dr. Anu Thomas'), (2, 'Ms. Sameera Ibrahim'), (3, 'Ms. Minal Sarode'), (4, 'Ms. Rashmi Prabha'), (5, 'Dr. Meghna Bhatia'), (6, 'Ms. Arti Bansode'), (7, 'Ms. Shaima Thange');

desc teachers;
select * from teachers;

CREATE TABLE teacher_subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT NOT NULL,
    subject_id INT NOT NULL, -- Changed to INT to match the subjects table
    class_id INT NOT NULL,
    teaching_type ENUM('Theory', 'Practical') NOT NULL DEFAULT 'Theory',
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE, 
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE
);

insert into teacher_subjects (teacher_id, subject_id, class_id, teaching_type) values 
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
(7, 11, 6, 'Practical');

desc teacher_subjects;
select * from teacher_subjects;

CREATE TABLE subjects_cs (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL
); 
INSERT INTO subjects_cs (subject_name) 
VALUES 
('Artificial Intelligence'), 
('Artificial Intelligence Practical'), 
('Information and Cybersecurity'), 
('Information and Cybersecurity Practical'), 
('Linux Server Administration'), 
('Linux Server Administration Practical'), 
('Science of Language Processing'), 
('Statistical Methods'), 
('Statistical Methods Practical'); 

select * from subjects_cs; 

CREATE TABLE class_subjects_cs (
    class_id INT NOT NULL, 
    subject_id INT NOT NULL, 
    PRIMARY KEY (class_id, subject_id), 
    FOREIGN KEY (class_id) REFERENCES classes(class_id), 
    FOREIGN KEY (subject_id) REFERENCES subjects_cs(subject_id)
); 

insert into class_subjects_cs(class_id, subject_id) 
values 
(9,1), (9,2), (9,3), (9,4), (9,5), (9,6), (9,7), (9,8), (9,9);

CREATE TABLE teachers_cs(
    teacher_id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(100) NOT NULL
); 

INSERT INTO teachers_cs (teacher_id, name) 
VALUES 
(1, 'Dr. Sheeja K'), 
(2, 'Dr. Aditya Jinturkar'), 
(3, 'Dr. Rajeshri Shinkar'), 
(4, 'Dr. Pallavi Awate'), 
(5, 'Ms. Flosia Simon'), 
(6, 'Ms. Fatema Kothari'), 
(7, 'Dr. Trupti Wani'),
(8, 'Ms. Shrutika Jadhav'),
(9, 'Ms. Dipti Patil'); 

CREATE TABLE teacher_subjects_cs(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    teacher_id INT NOT NULL, 
    subject_id INT NOT NULL,
    class_id INT NOT NULL, 
    teaching_type ENUM('Theory', 'Practical') NOT NULL DEFAULT 'Theory', 
    FOREIGN KEY (teacher_id) REFERENCES teachers_cs(teacher_id) ON DELETE CASCADE, 
    FOREIGN KEY (subject_id) REFERENCES subjects_cs(subject_id) ON DELETE CASCADE, 
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE
); 

insert into teacher_subjects_cs(id, teacher_id, subject_id, class_id, teaching_type) 
values 
(1, 3, 1, 9, 'Theory'), 
(2, 3, 2, 9, 'Practical'), 
(3, 6, 3, 9, 'Theory'), 
(4, 6, 4, 9, 'Practical'), 
(5, 2, 5, 9, 'Theory'), 
(6, 2, 6, 9, 'Practical'), 
(7, 5, 7, 9, 'Theory'), 
(8, 1, 8, 9, 'Theory'), 
(9, 1, 9, 9, 'Practical');

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

desc admins;
select * from admins;

show tables;

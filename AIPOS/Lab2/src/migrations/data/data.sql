INSERT INTO system_metadata (administrator_id, trade_union_contribution, income_tax, minimum_salary, pension_contribution)
VALUES (1, 1000, 2000, 5000, 3000);

INSERT INTO category (coefficient, change_date)
VALUES (1.5, '2023-01-01'),
       (2.0, '2023-02-01'),
       (1.8, '2023-03-01'),
       (1.2, '2023-04-01'),
       (1.7, '2023-05-01'),
       (1.3, '2023-06-01'),
       (1.9, '2023-07-01'),
       (1.4, '2023-08-01'),
       (1.6, '2023-09-01'),
       (1.1, '2023-10-01');

INSERT INTO position (name, category_id)
VALUES ('Manager', 1),
       ('Assistant', 2),
       ('Supervisor', 1),
       ('Clerk', 3),
       ('Technician', 2),
       ('Analyst', 1),
       ('Engineer', 2),
       ('Coordinator', 3),
       ('Developer', 2),
       ('Designer', 1);

INSERT INTO employee (full_name)
VALUES ('John Doe'),
       ('Jane Smith'),
       ('Michael Johnson'),
       ('Emily Davis'),
       ('Robert Brown'),
       ('Laura Wilson'),
       ('David Thompson'),
       ('Sarah Anderson'),
       ('Daniel Lee'),
       ('Olivia Martin');


INSERT INTO employee_position (employee_id, position_id)
VALUES (1, 1),
       (2, 2),
       (3, 3),
       (4, 4),
       (5, 5),
       (6, 6),
       (7, 7),
       (8, 8),
       (9, 9),
       (10, 10);

INSERT INTO payment_history (employee_id, month, earnings, payments, deductions)
VALUES (1, 'January', 10000, 9000, 1000),
       (2, 'January', 8000, 7500, 500),
       (3, 'January', 6000, 5500, 500),
       (4, 'January', 7000, 6500, 500),
       (5, 'January', 9000, 8500, 500),
       (6, 'January', 12000, 11000, 1000),
       (7, 'January', 10000, 9500, 500),
       (8, 'January', 11000, 10500, 500),
       (9, 'January', 9500, 9000, 500),
       (10, 'January', 8500, 8000, 500);

INSERT INTO administrator (full_name, hashed_password)
VALUES ('johndoe', 'EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW');


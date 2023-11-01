-- Setup database environment stuff

SET client_min_messages TO 'warning';
DROP DATABASE IF EXISTS salary_calculation;
DROP USER IF EXISTS kitanoyoru;
RESET client_min_messages;

SET sepgsql.debug_audit = true;
SET client_min_messages = LOG;


CREATE DATABASE salary_calculation;

CREATE USER kitanoyoru;

CREATE SCHEMA salary_calculation_schema;

GRANT ALL ON SCHEMA salary_calculation_schema TO kitanoyoru;

SET search_path = salary_calculation_schema, public;


-- Tables

CREATE TABLE IF NOT EXISTS Category
(
    ID          SERIAL PRIMARY KEY,
    Coefficient REAL NOT NULL,
    ChangeDate  DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS Position
(
    ID          SERIAL PRIMARY KEY,
    Name        VARCHAR(30) NOT NULL,
    Category_ID INTEGER,

    CONSTRAINT FK_Position_Category FOREIGN KEY (Category_ID) REFERENCES Category (ID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Employee
(
    ID       SERIAL PRIMARY KEY,
    FullName VARCHAR(15) NOT NULL,
    Position VARCHAR(30) NOT NULL,
    Category INTEGER     NOT NULL
);

CREATE TABLE IF NOT EXISTS Employee_Position
(
    Employee_ID INTEGER,
    Position_ID INTEGER,

    CONSTRAINT PK_Employee_Position PRIMARY KEY (Employee_ID, Position_ID),

    CONSTRAINT FK_Employee_Position_Employee FOREIGN KEY (Employee_ID) REFERENCES Employee (ID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Employee_Position_Position FOREIGN KEY (Position_ID) REFERENCES Position (ID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Payment_History
(
    ID          SERIAL PRIMARY KEY,
    Employee_ID INTEGER,
    Month       VARCHAR(12) NOT NULL,
    Earnings    BIGINT      NOT NULL,
    Payments    BIGINT      NOT NULL,
    Deductions  BIGINT      NOT NULL,

    CONSTRAINT FK_Payment_History_Employee FOREIGN KEY (Employee_ID) REFERENCES Employee (ID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS System_Metadata
(
    ID                       SERIAL PRIMARY KEY,
    Trade_Union_Contribution BIGINT NOT NULL,
    Income_Tax               BIGINT NOT NULL,
    Minimum_Salary           BIGINT NOT NULL,
    Pension_Contribution     BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS Administrator
(
    ID                 SERIAL PRIMARY KEY,
    FullName           VARCHAR(15) NOT NULL,
    System_Metadata_ID INTEGER,

    CONSTRAINT FK_Administrator_System_Metadata FOREIGN KEY (System_Metadata_ID) REFERENCES System_Metadata (ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Triggers

CREATE OR REPLACE FUNCTION check_system_metadata_count()
    RETURNS TRIGGER AS
$$
DECLARE
    metadata_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO metadata_count FROM System_Metadata;
    IF metadata_count > 1 THEN
        RAISE EXCEPTION 'Only one entry is allowed in System_Metadata table';
    END IF;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER trigger_check_system_metadata_count
    BEFORE INSERT OR UPDATE
    ON System_Metadata
    FOR EACH ROW
EXECUTE FUNCTION check_system_metadata_count();

CREATE OR REPLACE FUNCTION check_administrator_count()
    RETURNS TRIGGER AS
$$
DECLARE
    administrator_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO administrator_count FROM System_Metadata;
    IF administrator_count > 1 THEN
        RAISE EXCEPTION 'Only one entry is allowed in Administrator table';
    END IF;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER trigger_check_administrator_count
    BEFORE INSERT OR UPDATE
    ON Administrator 
    FOR EACH ROW
EXECUTE FUNCTION check_administrator_count();


CREATE OR REPLACE FUNCTION check_category_count()
    RETURNS TRIGGER AS
$$
DECLARE
    category_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO category_count FROM Category;
    IF category_count > 18 THEN
        RAISE EXCEPTION 'Only 18 entries is allowed in Category table';
    END IF;
    RETURN NEW;
END;
$$
    LANGUAGE plpgsql;

CREATE TRIGGER trigger_check_category_count
    BEFORE INSERT OR UPDATE
    ON Category
    FOR EACH ROW
EXECUTE FUNCTION check_category_count();


-- Views

CREATE VIEW get_categories_by_current_date AS
SELECT *
FROM Category
WHERE ChangeDate = CURRENT_DATE;

CREATE VIEW get_employees_with_min_salary_for_month AS 
    SELECT e.*
    FROM Employee AS e
             INNER JOIN (SELECT ph.Employee_ID
                         FROM Payment_History AS ph
                         WHERE ph.Month = mont
                         GROUP BY ph.Employee_ID
                         ORDER BY SUM(ph.Earnings) DESC
                         LIMIT 1) AS top_employee ON e.ID = top_employee.Employee_ID;

CREATE VIEW PROCEDURE get_employee_payment_for_month AS 
    SELECT *
    FROM Payment_History
    WHERE Employee_ID = employee_i
      AND Month = mont;
---

-- Functions

CREATE OR REPLACE FUNCTION add_employee(
    full_name VARCHAR(50),
    positio VARCHAR(10),
    categor INTEGER
)
    RETURNS INTEGER AS
$$
DECLARE
    inserted_id INTEGER;
BEGIN
    INSERT INTO Employee (FullName, Position, Category)
    VALUES (full_name, positio, categor)
    RETURNING ID INTO inserted_id;

    RETURN inserted_id;
END;
$$
    LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_employee(employee_id INTEGER)
    RETURNS INTEGER AS
$$
DECLARE
    deleted_id INTEGER;
BEGIN
    DELETE
    FROM Employee
    WHERE ID = employee_id
    RETURNING ID INTO deleted_id;

    RETURN deleted_id;
END;
$$
    LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_employee(
    employee_id INTEGER,
    full_name VARCHAR(15),
    positio VARCHAR(10),
    categor INTEGER
)
    RETURNS INTEGER AS
$$
DECLARE
    updated_id INTEGER;
BEGIN
    UPDATE Employee
    SET FullName = full_name,
        Position = positio,
        Category = categor
    WHERE ID = employee_id
    RETURNING ID INTO updated_id;

    RETURN updated_id;
END;
$$
    LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION add_category(
    coefficien REAL,
    change_date DATE DEFAULT CURRENT_DATE
)
    RETURNS INTEGER AS
$$
DECLARE
    inserted_id INTEGER;
BEGIN
    INSERT INTO Category (Coefficient, ChangeDate)
    VALUES (coefficien, change_date)
    RETURNING ID INTO inserted_id;

    RETURN inserted_id;
END;
$$
    LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_category(category_id INTEGER)
    RETURNS INTEGER AS
$$
DECLARE
    deleted_id INTEGER;
BEGIN
    DELETE
    FROM Category
    WHERE ID = category_id
    RETURNING ID INTO deleted_id;

    RETURN deleted_id;
END;
$$
    LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_category(
    category_id INTEGER,
    coefficient REAL,
    change_date DATE DEFAULT CURRENT_DATE
)
    RETURNS INTEGER AS
$$
DECLARE
    updated_id INTEGER;
BEGIN
    UPDATE Category
    SET Coefficient = coefficient,
        ChangeDate  = change_date
    WHERE ID = category_id
    RETURNING ID INTO updated_id;

    RETURN updated_id;
END;
$$
    LANGUAGE plpgsql;



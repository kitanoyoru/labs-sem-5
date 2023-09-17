-- Задание 2--

SET synchronous_commit = on;

CREATE TYPE ГородEnum AS ENUM ('Москва', 'Таллинн', 'Минск', 'Киев', 'Вильнюс', 'Псков', 'Саратов');
CREATE TYPE ЦветEnum AS ENUM ('Красный', 'Зеленая', 'Черный');



CREATE TABLE Поставщики_S
(
    П      VARCHAR(2) PRIMARY KEY,
    ИмяП   VARCHAR(10) NOT NULL,
    Статус SMALLSERIAL NOT NULL,
    Город  ГородEnum   NOT NULL
);

CREATE OR REPLACE FUNCTION check_primary_key_for_Поставщики_S()
    RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.П !~ '^П' THEN
        RAISE EXCEPTION 'Primary key must start with letter П!';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_primary_key_trigger_Поставщики_S
    BEFORE INSERT
    ON Поставщики_S
    FOR EACH ROW
EXECUTE FUNCTION check_primary_key_for_Поставщики_S();



CREATE TABLE Детали_P
(
    Д      VARCHAR(2) PRIMARY KEY,
    ИмяД   VARCHAR(10) NOT NULL,
    Цвет   ЦветEnum    NOT NULL,
    Размер SMALLSERIAL NOT NULL,
    Город  ГородEnum
);
CREATE OR REPLACE FUNCTION check_primary_key_for_Детали_P()
    RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.Д !~ '^Д' THEN
        RAISE EXCEPTION 'Primary key must start with letter П!';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_primary_key_trigger_Детали_P
    BEFORE INSERT
    ON Детали_P
    FOR EACH ROW
EXECUTE FUNCTION check_primary_key_for_Детали_P();



CREATE TABLE Проекты_J
(
    ПР    VARCHAR(50) PRIMARY KEY,
    ИмяПР VARCHAR(4) NOT NULL,
    Город ГородEnum  NOT NULL
);
CREATE OR REPLACE FUNCTION check_primary_key_for_Проекты_J()
    RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.ПР !~ '^ПР' THEN
        RAISE EXCEPTION 'Primary key must start with letter ПР!';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_primary_key_trigger_Проекты_J
    BEFORE INSERT
    ON Проекты_J
    FOR EACH ROW
EXECUTE FUNCTION check_primary_key_for_Проекты_J();



CREATE TABLE Количество_Деталей
(
    П  VARCHAR(50),
    Д  VARCHAR(50),
    ПР VARCHAR(50),
    S  VARCHAR(50),

    PRIMARY KEY (П, Д, ПР),

    FOREIGN KEY (П) REFERENCES Поставщики_S (П),
    FOREIGN KEY (Д) REFERENCES Детали_P (Д),
    FOREIGN KEY (ПР) REFERENCES Проекты_J (ПР)
);

BEGIN;
INSERT INTO Поставщики_S(П, ИмяП, Статус, Город)
VALUES ('П1', 'Петров', '20', 'Москва'),
       ('П2', 'Синицин', '10', 'Таллинн'),
       ('П3', 'Федоров', '30', 'Таллинн'),
       ('П4', 'Чаянов', '20', 'Минск'),
       ('П5', 'Крюков', '30', 'Киев');
COMMIT;

BEGIN;
INSERT INTO Детали_P(Д, ИмяД, Цвет, Размер, Город)
VALUES ('Д1', 'Болт', 'Красный', '12', 'Москва'),
       ('Д2', 'Гайка', 'Зеленая', '17', 'Минск'),
       ('Д3', 'Диск', 'Черный', '17', 'Вильнюс'),
       ('Д4', 'Диск', 'Черный', '14', 'Москва'),
       ('Д5', 'Корпус', 'Красный', '12', 'Минск'),
       ('Д6', 'Крышки', 'Красный', '19', 'Москва');
COMMIT;

BEGIN;
INSERT INTO Проекты_J(ПР, ИмяПР, Город)
VALUES ('ПР1', 'ИПР1', 'Минск'),
       ('ПР2', 'ИПР2', 'Таллинн'),
       ('ПР3', 'ИПР3', 'Псков'),
       ('ПР4', 'ИПР4', 'Псков'),
       ('ПР5', 'ИПР5', 'Москва'),
       ('ПР6', 'ИПР6', 'Саратов'),
       ('ПР7', 'ИПР7', 'Москва');
COMMIT;

BEGIN;
INSERT INTO Количество_Деталей(П, Д, ПР, S)
VALUES ('П1', 'Д1', 'ПР1', '200'),
       ('П1', 'Д1', 'ПР2', '700'),
       ('П2', 'Д3', 'ПР1', '400'),
       ('П2', 'Д2', 'ПР2', '200'),
       ('П2', 'Д3', 'ПР3', '200'),
       ('П2', 'Д3', 'ПР4', '500'),
       ('П2', 'Д3', 'ПР5', '600'),
       ('П2', 'Д3', 'ПР6', '400'),
       ('П2', 'Д3', 'ПР7', '800'),
       ('П2', 'Д5', 'ПР2', '100'),
       ('П3', 'Д3', 'ПР1', '200'),
       ('П3', 'Д4', 'ПР2', '500'),
       ('П4', 'Д6', 'ПР3', '300'),
       ('П4', 'Д6', 'ПР7', '300'),
       ('П5', 'Д2', 'ПР2', '200'),
       ('П5', 'Д2', 'ПР4', '100'),
       ('П5', 'Д5', 'ПР5', '500'),
       ('П5', 'Д5', 'ПР7', '100'),
       ('П5', 'Д6', 'ПР2', '200'),
       ('П5', 'Д1', 'ПР2', '100'),
       ('П5', 'Д3', 'ПР4', '200'),
       ('П5', 'Д4', 'ПР4', '800'),
       ('П5', 'Д5', 'ПР4', '400'),
       ('П5', 'Д6', 'ПР4', '500');
COMMIT;



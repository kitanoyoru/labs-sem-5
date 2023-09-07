CREATE TABLE ПРЕПОДАВАТЕЛЬ
(
    ЛичныйНомер     VARCHAR(50) PRIMARY KEY,
    Фамилия         VARCHAR(50),
    Должность       VARCHAR(50),
    Кафедра         VARCHAR(50),
    Специальность   VARCHAR(50),
    ТелефонДомашний VARCHAR(50)
);

CREATE TABLE ПРЕДМЕТ
(
    КодовыйНомерПредмета VARCHAR(50) PRIMARY KEY,
    НазваниеПредмета     VARCHAR(50),
    КоличествоЧасов      VARCHAR(50),
    Специальность        VARCHAR(50),
    Семестр              VARCHAR(50)
);


CREATE TABLE СТУДЕНЧЕСКАЯ_ГРУППА
(
    КодовыйНомерГруппы VARCHAR(50) PRIMARY KEY,
    НазваниеГруппы     VARCHAR(50),
    КоличествоЧеловек  VARCHAR(50),
    Специальность      VARCHAR(50),
    ФамилияСтаросты    VARCHAR(50)
);

CREATE TABLE ПРЕПОДАВАТЕЛЬ_ПРЕПОДАЕТ_ПРЕДМЕТЫ_В_ГРУППАХ
(
    КодовыйНомерГруппы   VARCHAR(50),
    КодовыйНомерПредмета VARCHAR(50),
    ЛичныйНомер          VARCHAR(50),
    НомерАудитории       VARCHAR(50),

    FOREIGN KEY (КодовыйНомерГруппы) REFERENCES СТУДЕНЧЕСКАЯ_ГРУППА (КодовыйНомерГруппы),
    FOREIGN KEY (КодовыйНомерПредмета) REFERENCES ПРЕДМЕТ (КодовыйНомерПредмета),
    FOREIGN KEY (ЛичныйНомер) REFERENCES ПРЕПОДАВАТЕЛЬ (ЛичныйНомер)
);

INSERT INTO ПРЕПОДАВАТЕЛЬ (ЛичныйНомер, Фамилия, Должность, Кафедра, Специальность, ТелефонДомашний)
VALUES ('221Л', 'Фролов', 'Доцент', 'ЭВМ', 'АСОИ, ЭВМ', '487'),
       ('222Л', 'Костин', 'Доцент', 'ЭВМ', 'ЭВМ', '543'),
       ('225Л', 'Бойко', 'Профессор', 'АСУ', 'АСОИ, ЭВМ', '112'),
       ('430Л', 'Глазов', 'Ассистент', 'ТФ', 'СД', '421'),
       ('110Л', 'Петров', 'Ассистент', 'Экономики', 'Международная экономика', '324');

INSERT INTO ПРЕДМЕТ (КодовыйНомерПредмета, НазваниеПредмета, КоличествоЧасов, Специальность, Семестр)
VALUES ('12П', 'Мини ЭВМ', '36', 'ЭВМ', '1'),
       ('14П', 'ПЭВМ', '72', 'ЭВМ', '1'),
       ('17П', 'СУБД ПК', '48', 'АСОИ', '4'),
       ('18П', 'ВКСС', '52', 'АСОИ', '6'),
       ('34П', 'Физика', '30', 'СД', '6'),
       ('22П', 'Аудит', '24', 'Бухучета', '3');

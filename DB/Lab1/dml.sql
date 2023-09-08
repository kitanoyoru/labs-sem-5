-- Вариант 11 --

-- 22 --

SELECT a."ПР"
FROM "Количество_Деталей" AS a
WHERE a."П" = 'П1'
  AND CAST(a.s AS INTEGER) > 0;

-- 21 --

SELECT a."Д"
FROM "Количество_Деталей" AS a
         INNER JOIN "Проекты_j" AS b ON a."ПР" = b."ПР"
    AND b."Город" = 'Минск';

-- 29 --

SELECT a."ПР"
FROM "Количество_Деталей" AS a
WHERE a."П" = 'П1'
GROUP BY a."ПР"
HAVING count(*) = 1;

-- 4 --

SELECT *
FROM "Количество_Деталей" AS a
WHERE CAST(a.s AS INTEGER) BETWEEN 350 AND 750;

-- 7 --
SELECT a."П", a."Д", a."ПР"
FROM "Количество_Деталей" AS a
         INNER JOIN "Поставщики_s" AS b ON a."П" = b."П"
         INNER JOIN "Детали_p" AS c ON a."Д" = c."Д"
         INNER JOIN "Проекты_j" AS d ON a."ПР" = d."ПР"
WHERE b."Город" <> c."Город"
  AND c."Город" <> d."Город"
  AND b."Город" <> d."Город";

-- 11 --
SELECT b."Город", d."Город"
FROM "Количество_Деталей" AS a
         INNER JOIN "Поставщики_s" AS b ON a."П" = b."П"
         INNER JOIN "Проекты_j" AS d ON a."ПР" = d."ПР";

-- 15 --
SELECT COUNT(*)
FROM "Количество_Деталей" AS a
WHERE a."П" = 'П1';

-- 33 --
SELECT b."Город"
FROM "Количество_Деталей" AS a
         INNER JOIN "Поставщики_s" AS b ON a."П" = b."П"
         INNER JOIN "Детали_p" AS c ON a."Д" = c."Д"
         INNER JOIN "Проекты_j" AS d ON a."ПР" = d."ПР"
WHERE b."Город" = c."Город"
  AND c."Город" = d."Город";

-- 25 --
SELECT a."ПР"
FROM "Количество_Деталей" AS a
         INNER JOIN "Проекты_j" AS d ON a."ПР" = d."ПР"
WHERE d."Город" IN (SELECT MIN(c."Город")
                    FROM "Проекты_j" AS c);



-- Вариант 12 --

-- 21 --

SELECT a."Д"
FROM "Количество_Деталей" AS a
         INNER JOIN "Проекты_j" AS b ON a."ПР" = b."ПР"
    AND b."Город" = 'Минск';

-- 22 --

SELECT a."ПР"
FROM "Количество_Деталей" AS a
WHERE a."П" = 'П1'
  AND CAST(a.s AS INTEGER) > 0;

-- 30 --

SELECT a."Д"
FROM "Количество_Деталей" AS a
         INNER JOIN "Проекты_j" AS b ON a."ПР" = b."ПР"
    AND b."Город" = 'Минск';

-- 3 --
SELECT a."П"
FROM "Количество_Деталей" AS a
WHERE a."ПР" = 'ПР1';

-- 8 -- not solved
SELECT DISTINCT ON (b."Город", c."Город", d."Город") a."П", a."Д", a."ПР", b."Город", c."Город", d."Город"
FROM "Количество_Деталей" AS a,
     "Поставщики_s" AS b,
     "Детали_p" AS c,
     "Проекты_j" as d;

-- 12 --
SELECT a."Д"
FROM "Количество_Деталей" AS a
         INNER JOIN "Поставщики_s" AS b ON a."П" = b."П"
         INNER JOIN "Проекты_j" AS d ON a."ПР" = d."ПР"
WHERE b."Город" = d."Город";

-- 16 --
SELECT SUM(CAST(a.s AS INTEGER))
FROM "Количество_Деталей" AS a
WHERE a."П" = 'П1';

-- 32 --
SELECT b."ПР"
FROM "Количество_Деталей" AS b
WHERE b."Д" IN (SELECT a."Д"
                FROM "Количество_Деталей" AS a
                WHERE a."П" = 'П1');

-- 26 -- not solved
SELECT AVG(CAST(a.s AS INTEGER))
FROM "Количество_Деталей" AS a
WHERE a."Д" = 'Д1';

SELECT a."ПР"
FROM "Количество_Деталей" AS a
WHERE a."Д" = 'Д1'
  AND AVG(CAST(a.s AS INTEGER)) > (SELECT MAX(CAST(b.s AS INTEGER))
                                   FROM "Количество_Деталей" AS b
                                   WHERE b."ПР" = 'ПР1');

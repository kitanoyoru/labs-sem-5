-- Вариант 12 --

-- 21 --

SELECT cd."Д"
FROM "Количество_Деталей" AS cd
         LEFT JOIN "Проекты_j" AS pj ON cd."ПР" = pj."ПР"
WHERE pj."Город" = 'Минск';

-- 22 --

SELECT "ПР"
FROM "Количество_Деталей"
WHERE "П" = 'П1'
  AND "s"::INTEGER > 0;

-- 30 --

SELECT a."Д"
FROM "Количество_Деталей" AS a
         INNER JOIN "Проекты_j" AS b ON a."ПР" = b."ПР"
    AND b."Город" = 'Псков';

-- 3 --

SELECT a."П"
FROM "Количество_Деталей" AS a
WHERE a."ПР" = 'ПР1';

-- 8 --

SELECT DISTINCT a."П", a."Д", a."ПР"
FROM "Количество_Деталей" AS a
         INNER JOIN "Поставщики_s" AS b ON a."П" = b."П"
         INNER JOIN "Детали_p" AS c ON a."Д" = c."Д"
         INNER JOIN "Проекты_j" AS d ON a."ПР" = d."ПР"
WHERE b."Город" <> c."Город"
  AND c."Город" <> d."Город"
  AND b."Город" <> d."Город";

-- 12 --

SELECT a."Д"
FROM "Количество_Деталей" AS a
         INNER JOIN "Поставщики_s" AS b ON a."П" = b."П"
         INNER JOIN "Проекты_j" AS d ON a."ПР" = d."ПР"
WHERE b."Город" = d."Город";

-- 16 --

SELECT SUM(CAST("s" AS INTEGER))
FROM "Количество_Деталей"
WHERE "П" = 'П1';

-- 32 --

WITH temp AS (
    SELECT ARRAY_AGG(DISTINCT b."Д") AS v
    FROM "Количество_Деталей" AS b
    WHERE b."П" = 'П1'
)

SELECT a."ПР"
FROM "Количество_Деталей" AS a
GROUP BY a."ПР"
HAVING ARRAY_AGG(a."Д") @> (SELECT v FROM temp)
ORDER BY a."ПР";

-- 26 --

WITH q1 AS (SELECT a."ПР", AVG(CAST(a.s AS INTEGER)) AS average
            FROM "Количество_Деталей" AS a
            WHERE a."Д" = 'Д3'
            GROUP BY a."ПР"),
     q2 AS (SELECT MAX(CAST(a.s AS INTEGER)) AS maximum
            FROM "Количество_Деталей" AS a
            WHERE a."ПР" = 'ПР1')
SELECT DISTINCT b."ПР"
FROM "Количество_Деталей" AS b
         JOIN q1 ON b."ПР" = q1."ПР"
         JOIN q2 ON q1.average > q2.maximum;

-- 17 -- 

SELECT "Д", "ПР", SUM(CAST("s" AS INTEGER))
FROM "Количество_Деталей"
GROUP BY "Д", "ПР";


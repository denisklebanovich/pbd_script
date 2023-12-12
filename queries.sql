WITH ApplicationsPerMajorPerYear AS (
   SELECT
       m."name" AS major_name,
       m."number_of_places" AS total_places,
       TO_DATE(ra."year"::text, 'YYYY') AS application_year,
       COUNT(ra."pk_id") AS total_applications
   FROM
       "majors" m
   JOIN
       "recruitment_applications" ra ON m."pk_id" = ra."fk_major"
   GROUP BY
       m."name", m."number_of_places", TO_DATE(ra."year"::text, 'YYYY')
)

SELECT
   major_name,
   total_places,
   EXTRACT(YEAR FROM application_year) AS application_year,
   ROUND(total_applications::numeric / total_places, 2) AS applications_per_place
FROM
   ApplicationsPerMajorPerYear
ORDER BY
   major_name, application_year;

SELECT
   m.name,
   ROUND(AVG(th.round_1)::numeric, 2) AS average_on_first_round,
   ROUND(AVG(th.round_2)::numeric, 2) AS average_on_second_round,
   ROUND(AVG(th.round_3)::numeric, 2) AS average_on_third_round
FROM
   majors m
JOIN
   thresholds th ON th.fk_major = m.pk_id
GROUP BY m.name
ORDER BY m.name;

WITH CorrelationCoefficients AS (
  SELECT
      m.name,
      CORR(th.recrutation_year, th.round_1) AS correlation_between_prog_and_year,
      AVG(th.round_1) AS avg_prog
  FROM
      thresholds th
  JOIN
      majors m on m.pk_id = th.fk_major
  GROUP BY
      m.name
)
SELECT
  cc.name,
  ROUND((cc.avg_prog * (1 + cc.correlation_between_prog_and_year))::numeric, 2) AS potential_threshold_in_next_year
FROM
  CorrelationCoefficients cc
ORDER BY
   cc.name

;
SELECT
   can.surname,
   can.name,
   m.name AS major,
   ra.round,
   ra.year,
   CASE
       WHEN red.pk_id IS NULL
       THEN sum((sr.points - et.minimum_points_score) / (et.maximum_points_score - et.minimum_points_score)
       * smia.factor * 100)
       ELSE sum(smia.factor * 100)
   END AS recrutation_points

FROM
   candidates can
INNER JOIN
   recruitment_applications ra on can.pk_id = ra.fk_candidate
INNER JOIN
   majors m on ra.fk_major = m.pk_id

INNER JOIN
   major_algorithms ma on m.fk_algorithm = ma.pk_name
INNER JOIN
   subjects_mentioned_in_algorithm smia on ma.pk_name = smia.fk_algorithm

INNER JOIN
   exams e on can.pk_id = e.fk_candidate
INNER JOIN
   exam_types et on e.fk_exam_type = et.pk_name
INNER JOIN
   subject_results sr on e.pk_id = sr.fk_exam

LEFT JOIN
   subjects s on smia.fk_subject = s.pk_name and sr.fk_subject = s.pk_name
LEFT JOIN
   recruitment_exemption_documents red on can.pk_id = red.fk_candidate

WHERE date_part('Year', e.date) <= ra.year

GROUP BY
   can.surname,
   can.name,
   m.name,
   ra.round,
   ra.year,
   red.pk_id;

SELECT
   s.pk_name,
   avg((sr.points - et.minimum_points_score) / (et.maximum_points_score - et.minimum_points_score) * 100)

FROM
   candidates can
INNER JOIN
   exams e on can.pk_id = e.fk_candidate
INNER JOIN
   exam_types et on e.fk_exam_type = et.pk_name
INNER JOIN
   subject_results sr on e.pk_id = sr.fk_exam
RIGHT JOIN
   subjects s on sr.fk_subject = s.pk_name
GROUP BY
   s.pk_name
;

SELECT
   n.pk_name,
avg(fdd.average_mark) AS average_mark,
avg(fdd.thesis_mark) AS average_thesis_mark
FROM
   candidates can
INNER JOIN
   first_degree_diplomas fdd on can.pk_id = fdd.fk_candidate
INNER JOIN
   nationalities n on can.fk_nationality = n.pk_name
GROUP BY
   n.pk_name

;

SELECT
   d.name,
   avg(new.round_1)
FROM
   (SELECT t.fk_major, t.round_1 FROM thresholds t UNION ALL
   SELECT t.fk_major, t.round_2 FROM thresholds t UNION ALL
   SELECT t.fk_major, t.round_3 FROM thresholds t) AS new
INNER JOIN
   majors m on m.pk_id = new.fk_major
LEFT JOIN
   departments d on m.fk_department = d.pk_number
GROUP BY
   d.name
;


SELECT m.name AS major_name,
      COUNT(ra.pk_id) AS total_applications,
      COUNT(deff.pk_id) AS fee_exempt_applications,
      (COUNT(deff.pk_id) * 100.0 / COUNT(ra.pk_id)) AS fee_exempt_percentage
FROM majors m
        JOIN recruitment_applications ra ON m.pk_id = ra.fk_major
        LEFT JOIN documents_exempting_from_fees deff ON ra.fk_candidate = deff.fk_candidate
GROUP BY m.name;


SELECT c.name, c.surname, e.date, et.pk_name AS exam_type, sr.points
FROM candidates c
        JOIN exams e ON c.pk_id = e.fk_candidate
        JOIN exam_types et ON e.fk_exam_type = et.pk_name
        JOIN subject_results sr ON e.pk_id = sr.fk_exam
WHERE sr.points > (et.maximum_points_score * 0.75);


SELECT rw.name, rw.surname, COUNT(DISTINCT d.pk_number) AS department_number
FROM recruitment_workers rw
        JOIN recruitment_workers_majors rwm ON rw.pk_id = rwm.fk_recruitment_worker
        JOIN majors m ON rwm.fk_major = m.pk_id
        JOIN departments d ON m.fk_department = d.pk_number
GROUP BY rw.name, rw.surname
HAVING COUNT(DISTINCT d.pk_number) > 1;


SELECT
   d.name,
   count(c.pk_id)
FROM departments d
INNER JOIN majors m on d.pk_number = m.fk_department
INNER JOIN recruitment_applications ra on m.pk_id = ra.fk_major
INNER JOIN candidates c on c.pk_id = ra.fk_candidate
LEFT JOIN documents_exempting_from_fees deff on c.pk_id = deff.pk_id
INNER JOIN nationalities n on c.fk_nationality = n.pk_name
WHERE n.studies_fee_free=false and deff isnull
GROUP BY d.name;

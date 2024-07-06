SELECT * FROM vacancies
WHERE (name ILIKE %s OR %s = '')
  AND (area_name ILIKE %s OR %s = '')
  AND (salary_from >= %s OR %s IS NULL)
  AND (salary_to <= %s OR %s IS NULL);
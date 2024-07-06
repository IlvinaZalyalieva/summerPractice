INSERT INTO vacancies (
    name, area_name, salary_currency, salary_from, salary_to,
    employer_name, employer_id, snippet_requirement,
    snippet_responsibility, created_at, published_at
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
DROP TABLE IF EXISTS vacancies;
CREATE TABLE vacancies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    area_name VARCHAR(255),
    salary_currency VARCHAR(3),
    salary_from INTEGER,
    salary_to INTEGER,
    employer_name VARCHAR(255),
    employer_id INTEGER,
    snippet_requirement TEXT,
    snippet_responsibility TEXT,
    created_at DATE,
    published_at DATE
);
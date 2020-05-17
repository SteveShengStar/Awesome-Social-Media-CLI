use ProjectTest;

CREATE TABLE employees (
  id         INT PRIMARY KEY NOT NULL,
  name       VARCHAR(100) NOT NULL,
  manager_id INT NULL,
  INDEX (manager_id),
	FOREIGN KEY (manager_id) REFERENCES employees (id)
);

INSERT INTO employees VALUES
(333, "Yasmina", NULL),  # Yasmina is the CEO (manager_id is NULL)
(198, "John", 333),      # John has ID 198 and reports to 333 (Yasmina)
(692, "Tarek", 333),
(29, "Pedro", 198),
(4610, "Sarah", 29),
(72, "Pierre", 29),
(123, "Adil", 692);


WITH RECURSIVE cte AS
(
  SELECT 1 AS n, 1 AS p, -1 AS q
  UNION ALL
  SELECT n + 1, q * 2, p * 2 FROM cte WHERE n < 5
)
SELECT * FROM cte;

WITH RECURSIVE employee_paths (id, name, path) AS
(
  SELECT id, name, CAST(id AS CHAR(200))
    FROM employees
    WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, CONCAT(ep.path, ',', e.id)
    FROM employee_paths AS ep JOIN employees AS e
      ON ep.id = e.manager_id
)
SELECT * FROM employee_paths ORDER BY path;


-- Traversing through all parents
WITH RECURSIVE employee_paths (id, name, path, eid) AS
(
  SELECT id, name, CAST(id AS CHAR(200)), manager_id
    FROM employees
    WHERE id = 4610
  UNION ALL
  SELECT e.id, e.name, CONCAT(ep.path, ',', e.id), e.manager_id
    FROM employee_paths AS ep JOIN employees AS e
      ON ep.eid = e.id
)
SELECT * FROM employee_paths ORDER BY path;

-- Finding out all child entries
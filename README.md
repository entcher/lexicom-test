### 1. B-Tree index + LIKE
CREATE INDEX idx_short_names_name ON short_names (name);
CREATE INDEX idx_full_names_name ON full_names (name);

UPDATE full_names f
SET f.status = s.status
FROM short_names s
WHERE f.name LIKE s.name || '%'; 

### 2. GIN index + LIKE
CREATE INDEX idx_full_names_trgm ON full_names USING gin (name gin_trgm_ops);
CREATE INDEX idx_short_names_trgm ON short_names USING gin (name gin_trgm_ops);

UPDATE full_names f
SET f.status = s.status
FROM short_names s
WHERE f.name LIKE s.name || '%'; 

### 3. Функциональный индекс + Regex
CREATE INDEX idx_full_names_regex ON full_names ((regexp_replace(name, '\.[^.]+$', '')));

UPDATE full_names f
SET f.status = s.status
FROM short_names s
WHERE regexp_replace(f.name, '\.[^.]+$', '') = s.name;

### 4. Функциональный индекс + split_part
CREATE INDEX idx_full_names_split ON full_names (split_part(name, '.', 1));

UPDATE full_names f
SET f.status = s.status
FROM short_names s
WHERE split_part(f.name, '.', 1) = s.name;

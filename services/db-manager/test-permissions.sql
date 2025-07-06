-- Test des permissions pour backend_user
\c hypertube-db backend_user;

-- Devrait réussir
SELECT * FROM users_user LIMIT 1;
INSERT INTO users_user (username, email, password) VALUES ('test', 'test@test.com', 'test');
UPDATE users_user SET email = 'updated@test.com' WHERE username = 'test';
DELETE FROM users_user WHERE username = 'test';

-- Devrait échouer
SELECT * FROM movies_movie LIMIT 1;
INSERT INTO movies_movie (title) VALUES ('test');

-- Test des permissions pour backend_movies
\c hypertube-db backend_movies;

-- Devrait réussir
SELECT * FROM movies_movie LIMIT 1;
INSERT INTO movies_movie (title) VALUES ('test');
UPDATE movies_movie SET title = 'updated' WHERE title = 'test';
DELETE FROM movies_movie WHERE title = 'test';

-- Devrait échouer
SELECT * FROM users_user LIMIT 1;
INSERT INTO users_user (username, email, password) VALUES ('test', 'test@test.com', 'test'); 
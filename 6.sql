-- Query the average rating of all movies released in 2012

SELECT AVG(rating) FROM ratings
    WHERE (SELECT id FROM movies WHERE year = 2012);
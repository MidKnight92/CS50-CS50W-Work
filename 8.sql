-- Query the name s of all people who starred in Toy Story
SELECT name FROM people
    INNER JOIN stars ON (people.id = stars.person_id)
    INNER JOIN movies ON (stars.movie_id = movies.id)
    WHERE title = 'Toy Story';
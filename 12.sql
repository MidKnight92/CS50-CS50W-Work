-- Query the titles of all movies in which both Johnny Depp and Helena Bonham starred

SELECT movies.title FROM people
    JOIN stars ON (people.id = stars.person_id)
    JOIN movies ON (stars.movie_id = movies.id)
    WHERE people.name = "Johnny Depp"
INTERSECT
    SELECT movies.title FROM people
    JOIN stars ON (people.id = stars.person_id)
    JOIN movies ON (stars.movie_id = movies.id)
    WHERE people.name = "Helena Bonham Carter";
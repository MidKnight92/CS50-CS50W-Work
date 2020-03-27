-- Query to the list the names of all people who starred in a movie in which Kevin Bacon also Starred
-- Your query should output a table with a single column for the name of each person.
-- There may be multiple people named Kevin Bacon in the database. Be sure to only select the Kevin Bacon born in 1958.
-- Kevin Bacon himself should not be included in the resulting list.

SELECT DISTINCT name FROM people
    JOIN stars ON (people.id = stars.person_id)
    JOIN movies ON (stars.movie_id = movies.id)
    WHERE movies.title IN
        (SELECT DISTINCT movies.title FROM people
        JOIN stars ON people.id = stars.person_id
        JOIN movies ON stars.movie_id = movies.id
        WHERE name = 'Kevin Bacon' AND birth = 1958)
    AND people.name != 'Kevin Bacon';
-- Query all movies released in 2010 and their rating, in descending order by rating. For Movies with the same rating, order thenm alphabetically by title

SELECT title, rating FROM movies
    JOIN ratings ON movies.id = ratings.movie_id
    WHERE year = 2010 AND rating
    ORDER BY rating DESC, title ASC;
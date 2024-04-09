# Database-Project: Movie Review Application

## Group members:
Andrew McFerrin, Landon Pyko, Kai Achen

## Introduction:
  The mini-world for our project is a Movie Review Application. Each user is uniquely identified by their username. On their account they can store their favorite movie. From their account, they can review a movie. In the review, they give the movie a rating, along with any additional comments they have about the movie. Each movie is uniquely identified by its title, release year, and director together. A movie has additional information stored, such as its budget and its box office earnings. A movie is played at multiple theaters, and a theater shows multiple movies. The theater stores the number of tickets sold for each movie that is shown. Every theater is uniquely identified by its address. Other information about the theater includes its name and date of opening.


## Requirements analysis: 
### Data:
- Entities: Movies, theaters, users, and reviews. 
- Attributes of movies: title, release year, director, box office earnings, and budget. 
- Attributes of theaters: address, name, and date opened. 
- Attributes of users: username, age, and favorite movie. 
- Attributes of reviews: username, title, release year, director, rating and comments.
### Constraints:
- Usernames are unique. 
- Users can only have one favorite movie. 
- User age must be greater than 0
- Theater must have opened before movie released to play it
- Review comments are comprised of a maximum of 250 characters
- Movie Rating must be a decimal between  0 and 10 
### Operations (Bold use join):
- **Find all reviews of movies that turned a profit (box office earnings - budget)**
- **Find the amount of money contributed to a movie’s box office by a theater**
- **Find director of a user’s favorite movie**
- Find all movies reviewed by a user(s)
- Find all movies that played in a theater
- Find all users whose favorite movie is blank
- Find all movies made by given director
- Find average rating of a movie

## Logical design:
- Theater(Address, Name, Date_opened)
- Movie(Title, Year_released, Director, Box_office_earnings, Budget)
- User(Username, Favorite_movie, Age)
- Reviews(Username, Title, Year_released, Director, Rating, Comments)
- Plays(Theater, Title, Year_released, Director, Tickets_sold)

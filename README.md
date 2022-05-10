# CSE330
# Final Project

Rajat Nepal | 490732 | RajatNepal

Chelsea Yuan | 490370 | chelsealyuan

---------------------------------------


This website gives users a movie recommendation using a cosing similarity algorithm. Users can choose which movies they like/dislike. They can also comment on a movie's page.


---------------------------------------



TODO LIST:

- ~~Rubric Turned in on Time (5 points)~~

 - Framework/Languages: Django/Python (20 points)

 - Functionality (63 points)
    - General Website Functionality: (28 points)
        - 10 Users can register, login, and logout
        - 3 Each Movie has its own page with a description and link to more info about movie
        - 4 Users can add comments to a movie's page, visibile to everyone
        - 3 Users can edit and delete their own comments
        - 4 Admin User can delete, but not edit everyone's comments
        - 4 Admin user can edit movie descriptions/links to movie page
    
    - Recommending System: (35 points)
        - 10 Users can submit a form indicating which movies they have watched and whether they liked them
        - 5 Users can edit the above form and get updated results
        - 5 Home page with most popular movie (based on analysis of everyone's submissions, not cosine similarity)
        - 10 Users will get a movie soulmate (another user using cosine similarity algorithm) with contact info
        - 5 Users will get recommended a movie by cosine similarity and a link to that movie's page
        - ~~10 Databse contains users, movies, comments, etc to maintain above functionality~~
    - Best Practices: (7 points)
        - 3 Code is readable and well formatted
        - 2 All pages pass the html validator
        - ~~2 storing passwords are salted and hashed~~
  
    - Creative Portion (0 points)

# CSE330
# Final Project

Rajat Nepal | 490732 | RajatNepal

Chelsea Yuan | 490370 | chelsealyuan

---------------------------------------


This website gives users a movie recommendation using a cosine similarity algorithm. Users can choose which movies they like/dislike. They can also comment on a movie's page.


---------------------------------------

 - Framework/Languages: Django/Python

 - Functionality 
    - General Website Functionality:
        - Users can register, login, and logout
        - Each Movie has its own page with a description and link to more info about movie
        - Users can add comments to a movie's page, visibile to everyone
        - Users can edit and delete their own comments
        - Admin User can delete, but not edit everyone's comments
        - Admin user can edit movie descriptions/links to movie page
    
    - Recommending System: 
        - Users can submit a form indicating which movies they have watched and whether they liked them
        - Users can edit the above form and get updated results
        - Home page with most popular movie (based on analysis of everyone's submissions, not cosine similarity)
        - Users will get a movie soulmate (another user using cosine similarity algorithm) with contact info
        - Users will get recommended a movie by cosine similarity and a link to that movie's page
        - Databse contains users, movies, comments, etc to maintain above functionality
    - Best Practices: 
        - Code is readable and well formatted
        - All pages pass the html validator
        - storing passwords are salted and hashed

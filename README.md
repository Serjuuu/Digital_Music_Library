# Digital_Music_Library
  A full-stack web application which allows users to manage and search for artists, albums, and songs.It consists of a backend API built with Flask and a frontend user interface built with React.
  ## The technologies used
    For the backend part:
      1. Flask: A micro web framework for Python used to build the RESTful API.
      2. Flask-CORS: A Flask extension for handling Cross-Origin Resource Sharing (CORS), making the API accessible from the frontend.
      3. Flask-PyMongo: A Flask extension that simplifies using MongoDB with Flask applications.
      4. PyMongo: A Python library for interacting with MongoDB.
      
    For database:
      1. MongoDB Compass: A NoSQL database used to store data for artists, albums, and songs.

    For the frontend part:
      1. React: A JavaScript library for building user interfaces, particularly single-page applications.
      2. Axios: A promise-based HTTP client for the browser and Node.js used to make HTTP requests to the backend API.

    For desing and styling:
      1. CSS modules: A CSS file where all class and animation names are scoped locally by default.

  ## The environment and development
    1. Node.js: A JavaScript runtime used to run the React development server and build the frontend.
    2. npm (Node Package Manager): Used for managing frontend dependencies.
    
  ## The programming languages used
    1. Python
    2. JavaScript

  ## Project structure
    1. Backend: Handles API routes, interacts with MongoDB, and includes logic for handling CRUD operations.
    2. Frontend: React components handle user interactions, manage state, and display data fetched from the backend API.

  ## Testing
    1. Postman: Used for testing the CRUD operations and checking the status code for the HTTP.

  All the code was written in Microsoft Visual Studio Code.

  ## How to run the project
    1. Cloning the Git repository, to be able to have the project saved on the computer.
    2. Install Python dependencies where the file app.py is located:
      - pip install Flask Flask-Cors Flask-PyMongo;
    3. Create and activate a virtual environment:
      - python -m venv venv
        source venv/bin/activate;
    4. Set up MongoDB, in my case i named my database musiclibrary containing three collections ( artists , albums and songs) and also make sure it is connected to a port ( localhost:27017 ).
    5. Importing the data form import_data.py into the MongoDB database
    5. Run the Flask application from the terminal:
      - python app.py;
    6. For the frontend part, open a terminal and create a new directory for your frontend project:
      - npx create-react-app frontend
      - cd frontend;
    7. Install Axios for making HTTP requests:
      - npm install axios;
    8. Start App.js from the directory you created at step 6 and run from the terminal at that path:
      - npm start;
    
      

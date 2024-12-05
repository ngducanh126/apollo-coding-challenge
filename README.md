# 0. Problem Statement

  

We want to develop a service that provides CRUD API access for managing vehicle records stored in a database. Vehicles are uniquely identified by their VIN (case-insensitive) and include attributes such as manufacturer name, description, horsepower, model name, model year, purchase price, and fuel type. The API must support the following endpoints:

-   GET /vehicle: Retrieve all vehicle records.
    
-   POST /vehicle: Add a new vehicle.
    
-   GET /vehicle/{vin}: Retrieve a specific vehicle by VIN.
    
-   PUT /vehicle/{vin}: Update an existing vehicle by VIN.
    
-   DELETE /vehicle/{vin}: Delete a vehicle by VIN.
    

The service must handle invalid or malformed requests with appropriate error responses (400 Bad Request, 422 Unprocessable Entity) and ensure data integrity with validations such as unique VINs and properly formatted attributes.

  

# 1. Overview of the project and how to set things up
    

  

## Overview:

**A quick note  : the server is initally empty. After you start the server, you should run: " python apollo-coding-challenge/vehicle-api-server/fire_into_database.py " to feed data into the database and play around with the API.**

This project focuses on building both **REST API and GraphQL** servers for managing vehicle records in a database. While the problem statement primarily leans toward a REST API approach, I also developed a GraphQL API server to explore its flexibility and efficiency in handling data operations. Both servers use **Python Flask** for the backend and **SQLite** for data storage. Key features include robust validation, error handling, logging, rate limiting, and security best practices.

On the client side, I developed a React application and implemented Data Science scripts to explore and experiment with the API.

  



  

**The main code files can be found at apollo-coding-challenge/vehicle-api-server/app:**

-   db.py: creates the database schema
    
-   server.py : code for REST API server
    
-   graphql_server.py : code for the graphql server.
    

  

**Tests can be found at apollo-coding-challenge/vehicle-api-server/tests/**

I developed a comprehensive testing suite to ensure the functionality, reliability, and security of the REST API endpoints. These tests use Python's unittest framework and an in-memory SQLite database to keep the testing environment isolated and efficient. More detail abot the test suite is covered in part 2.

  

**In addition, here are important files at apollo-coding-challenge/vehicle-api-server:**

-   restAPI_run.py : to run the Rest API server
    
-   graphql_run.py: to run the GraphQL server
    
-   fire_into_database.py: after running the REST server, we can run this script to feed data into the database by using the REST endpoints.
    

  

**The client side code can be found at apollo-coding-challenge/use-cases.** We will cover this more later in part 2 of the README.

  
  

## Setting things up:

  

### REST API Server

**A quick note  : the server is initally empty. After you start the server, you should run: " python apollo-coding-challenge/vehicle-api-server/fire_into_database.py " to feed data into the database and play around with the API.**



First, clone the repository to your local machine:
- git clone [https://github.com/ngducanh126/apollo-coding-challenge.git](https://github.com/ngducanh126/apollo-coding-challenge.git)


Make sure you have Python installed. Run this script to check:
- python --version

If this returns an error, you have not installed Python. Please install it.
  

Navigate to **apollo-coding-challenge** (the home directory).

  

Create a virtual environment: 
- python -m venv venv

  

Activate the virtual environment:

-   Windows:  venv\Scripts\activate
    
-   macOS/Linux: source venv/bin/activate
    
**Note that every following commands (except for the React App) should be done within this virtual environment, which you just did above**
  

Now go to **apollo-coding-challenge/vehicle-api-server**  and install the required dependencies: 
- pip install -r requirements.txt

If you enter any errors, updating pip should likely fit it:
- python -m pip install --upgrade pip
  

Start the REST API server in **apollo-coding-challenge/vehicle-api-server:**
- python restAPI_run.py

  

The REST API server will be up and running at port 5000. You can access it in your browser at: [http://127.0.0.1:5000/vehicle](http://127.0.0.1:5000/vehicle)

  

You can also run the script **fire_data_into_database.py** to feed some data and play around with the api. In apollo-coding-challenge/vehicle-api-server run: 
- python fire_data_into_database.py

  

### GraphQL server Setup

**A quick note  : the server is initally empty. After you start the server, you should run: " python apollo-coding-challenge/vehicle-api-server/fire_into_database.py " to feed data into the database and play around with the API.**


Activate the virtual environment you created during the REST API setup. Make sure you are at **apollo-coding-challenge** directory (the home directory).

-   Windows: venv\Scripts\activate
    
-   macOS/Linux: source venv/bin/activate
    

**Note that every following commands (except the React App ) should be done within this virtual environment, which you just did above**

Now start the GraphQL API server. Go to **apollo-coding-challenge/vehicle-api-server** . Then run:
- python graphql_run.py

  

The GraphQL server will be up and running at port 5001. You can access and test queries at: http://127.0.0.1:5001/graphql

  

### Running tests for the APIs Servers:

Make sure you are at **apollo-coding-challenge/vehicle-api-server**

For the REST server run:
- pytest tests/test_vehicle_api.py
    
For the GraphQL server run: 
- pytest tests/graphql_test.py
    

  
  

### Starting the React application:

**A quick note  : the server is initally empty. After you start the server, you should run: " python apollo-coding-challenge/vehicle-api-server/fire_into_database.py " to feed data into the database and play around with the API.**

Navigate to apollo-coding-challenge/uses-cases/Web-App/vehicle-web-app:
    
Make sure you have npm installed by running:
- npm --version


If there was an error, npm is not installed. Please install Node.js and this will give you npm.


Use npm or yarn to install the required dependencies:
- npm install
    
Start the Development Server: 
- npm start


 Open your browser and go to http://localhost:3000 to view the app
    
I suggest you run the file **vehicle-api-server/fire_into_database.py** so that there is data for us to play around with in the React app.
    

  

### Data Science Stuffs

**A quick note  : the server is initally empty. After you start the server, you should run: " python apollo-coding-challenge/vehicle-api-server/fire_into_database.py " to feed data into the database and play around with the API.**

Make sure there is data in the database first. You can do this by running the file **vehicle-api-server/fire_into_database.py**

Again, activate the virtual environment you created earlier. Go to **apollo-coding-challenge** directory (the home directory) and activate the virtual environment:

-   Windows: venv\Scripts\activate
    
-   macOS/Linux: source venv/bin/activate

**Note that every following commands should be done within this virtual environment, which you just did above**

Now navigate to **apollo-coding-challenge/uses-cases/Web-App/Data-Science**
    
Run : 
- pip install -r requirements.txt


If you enter any errors, updating pip should likely fit it:
- python -m pip install --upgrade pip
  

Run : 
- python extract_load_transform.py
   
This file grabs data from the database via our REST endpoints and cleans the data and stores it in Data-Storage/processed/vehicles_cleaned.csv
    

    

Navigate to **apollo-coding-challenge/uses-cases/Web-App/Data-Science/AI-Models** and run: 
- python predict_purchase_price.py
    This is an AI model that predicts the price of a vehicle using various historical input from the database

In addition, navigate to apollo-coding-challenge/uses-cases/Web-App/Data-Science/Data-Analytics and run: 
- python analytics.py
    This file utilizes the pandas library to process and analyze the dataset. It extracts valuable information and presents it in a clear format.

  
  

# 2. A more in-depth look at the Project

**A quick note  : the server is initally empty. After you start the server, you should run: " python apollo-coding-challenge/vehicle-api-server/fire_into_database.py " to feed data into the database and play around with the API.**

## REST API server

My project focuses on building a RESTful web service that provides CRUD operations to manage vehicle records in a database. It uses Flask for the backend and SQLite for data storage. I aimed for best REST API principles as well as validation, scalability, and error handling.

The goal is to create an efficient system to manage vehicle data with the following features:

Database Schema:
    

-   The table vehicles is created to store vehicles, uniquely identified by their VIN (case-insensitive). Code can be found at vehicle-api-server/app/db.py
    
-   Key attributes include manufacturer_name, description, horse_power, model_name, model_year, purchase_price, and fuel_type.
    

API Endpoints:
    

-   GET /vehicle: Retrieves all vehicles.
    
-   POST /vehicle: Adds a new vehicle with proper validation.
    
-   GET /vehicle/{vin}: Fetches details for a specific vehicle.
    
-   PUT /vehicle/{vin}: Updates an existing vehicle's data.
    
-   DELETE /vehicle/{vin}: Deletes a vehicle from the database.
    

Error Handling:
    

-   400 Bad Request: Invalid JSON input.
    
-   422 Unprocessable Entity: Validation errors (e.g., missing or malformed fields).
    
-   409 Conflict: Duplicate VIN when trying to create a new vehicle.
    

Logging, Rate Limiting, and Security Practices

1.  Logging:I applied logging with timestamps and levels (DEBUG, INFO, ERROR) for clarity. The output is directed to both the console and the file app.lo for easy debugging.
    

  

2.  API Rate Limiting: I implemented rate limiting via Flask-Limiter, restricting requests based on client IP. The goal is prevent abuse and manage traffic load - a common practice in the industry.
    
3.  Security Best Practices:
    

-   SQL injection: I implemented parameterized queries to handle user inputs securely, preventing SQL injection by ensuring inputs are treated as data rather than executable code.
    
-   CORS: Only trusted origins (e.g., http://localhost:3000) are allowed. CORS also allowed me to develop my React Application on the client side to play around with the REST API server. More information about the React app is covered later.
    
-   Data Integrity: VINs are case-insensitively unique, and database queries are scoped to avoid exposure or misuse.
    

  

## Testing the REST API

I developed a comprehensive testing suite to ensure the functionality, reliability, and security of the REST API endpoints. These tests use Python's unittest framework and an in-memory SQLite database to keep the testing environment isolated and efficient.

#### My Approach to Testing

-   I configured an in-memory SQLite database to simulate real-world operations while ensuring no impact on the actual database.
    
-   Using Flask’s test client, I simulated HTTP requests to verify the behavior of each endpoint under various scenarios.
    
-   Each test case is carefully designed to cover common use cases, edge cases, and potential error scenarios.
    

  

## GraphQL

In addition to building a REST API, I implemented a GraphQL API as an optional enhancement to offer more flexible and efficient data querying and mutation. I used Strawberry as the GraphQL library, and I also integrated the GraphQL endpoint into the Flask application.

----------

#### Key Features of the GraphQL API

**1.  Schema Design:**
    

The schema defines a Vehicle type with attributes such as vin, manufacturer_name, description, horse_power, model_name, model_year, purchase_price, and fuel_type.
   
It includes both Query and Mutation classes to handle fetching and modifying data.
    

**2.  Resolvers**
    


Queries:
   

-   vehicles: this retrieves a list of all vehicles from the database.
   
-   vehicle(vin: str): this fetches a specific vehicle by its VIN.
   

Mutations:
   

-   create_vehicle: this adds a new vehicle to the database.
   
-   update_vehicle: this updates an existing vehicle's attributes.
   
-   delete_vehicle: this deletes a vehicle by its VIN.
   

The Resolvers also have effective error handling and proper validation.
   

**3.  GraphQL Endpoint:**
   

The /graphql endpoint is added to the Flask app using GraphQLView.
   

**4.  Key Advantages over rest: While the problem statement seems to point towards developing a REST API server, I developed the GraphQL server for some advantages:**
   

Flexible Data Retrieval: Clients can fetch only the fields they need and this reduces over-fetching or under-fetching compared to REST.
   
Nested Queries: this actually enables querying hierarchical data in a single request. It is especially useful when we have many data schemas related to one another (although in this case we only have the vehicle schema).
   
Combined Operations: Multiple related queries or mutations can be executed at the same time.
    

## Testing our GraphQL

I developed a dedicated testing suite to ensure the GraphQL API is functional, reliable, and adheres to best practices. The tests focus on validating the flexibility and accuracy of GraphQL queries and mutations while ensuring proper error handling and data integrity.

#### My Approach to Testing

-   I utilized Flask’s test client to simulate GraphQL queries and mutations in a controlled environment.
    
-   The tests leverage an in-memory SQLite database to mimic real-world interactions without affecting the actual data.
    
-   Each test case covers key scenarios, including successful operations, edge cases, and error handling for invalid inputs.
    

  

## React App (client side)

#### Key Pages and Features

**1.  Home Page:**
    

The starting point of the application.
    Introduces users to the Vehicle Management System with a welcoming message and a call-to-action button to view the list of vehicles.

   [ <img width="959" alt="home" src="https://github.com/user-attachments/assets/cfc85f5f-1137-47e0-8586-20b4d64754f1">](https://github.com/ngducanh126/apollo-coding-challenge/issues/1#issue-2713259650)


**2.  Vehicles List Page:**
    

Displays a comprehensive list of vehicles retrieved from the API.
   
Allows users to navigate to the add, edit, or analytics pages for more specific tasks.

![image](https://github.com/user-attachments/assets/28c6d11b-17c2-4b36-846e-d96fe1267da4)

    

**3.  Analytics Page:**
    

Provides detailed insights into the stored vehicle data, including:
    

-   Total number of vehicles.
    
-   Most common manufacturer.
    
-   Average purchase price.
    
-   Fuel type distribution visualized with a pie chart.
    
-   Average horsepower by manufacturer and purchase price by year visualized as bar charts.
    

-   Lazy Loading: The analytics page is configured for lazy loading to optimize performance. It loads only when the user navigates to it and this reduces initial load time

-   ![image](https://github.com/user-attachments/assets/d583f722-12dc-4d58-986c-a28ee2ca8001)
-   ![image](https://github.com/user-attachments/assets/e0165b46-de6a-420a-b833-35d594b11de2)




**4.  Add Vehicle Page:**
    

A form-based page for adding new vehicles to the database.
    
Validates inputs and handles server errors gracefully, providing feedback to the user.

![image](https://github.com/user-attachments/assets/284cad34-27e2-4e82-b8cb-b28e9d67707d)

    

**5.  Edit Vehicle Page:**
    

Allows users to modify existing vehicle records.
    
Ensures updated data is submitted securely and displays validation errors when necessary.

![image](https://github.com/user-attachments/assets/e37b43a9-fb72-415b-aa30-03e47b3f315b)

    

#### Initial Data Population

To facilitate testing and demonstration, the fire_data_into_database.py script was executed on the server side to feed data into the database with sample vehicle records.

#### Integration with the API

The app interacts with the backend API endpoints (/vehicle, /vehicle/{vin}) for data retrieval, submission, and updates.

  

## Data Science Mini-project (client side)

The Data Science module in this project is structured to analyze, clean, and model the vehicle data for insights and predictions. The pipeline is divided into three key scripts that cover data extraction, transformation, analysis, and predictive modeling.

  

- extract_load_transform.py: This file grabs data from the database via our REST endpoints and cleans the data and stores it in Data-Storage/processed directory

  

- analytics.py: This file utilizes the pandas library to process and analyze the dataset. It extracts valuable information and presents it in a clear format.

  

- predict_purchase_price.py: This is an AI model that predicts the price of a car using various historical input from the database

# 3. Looking ahead: things I would implement further for the REST API if I have more time

  

**Pagination**

Right now, the /vehicle REST endpoint returns all records, which could slow things down as the dataset grows. I plan to add pagination with page and limit parameters  and this will make responses faster and more efficient.

**Filter and sorting as query parameters**

This can give the client more flexibility to grab data.

**API versioning**


This supports backward compatability and ensures the client code that is using older versions of the API don't break.


**Cybersecurity Upgrades**

I want to strengthen security by:

Adding token-based authentication (like OAuth2 or JWT) and role-based access control. For example only admins can delete vehicles.

Improving input validation to block SQL injection and similar attacks.

  

**Caching**

To speed up repetitive queries (e.g., GET /vehicle), I’ll integrate caching with tools like Redis or Memcached as these will reduce database load and improve response times.

  
  

**Database Optimization**

I plan to improve database performance by adding indexes on commonly queried fields, partitioning large datasets, and optimizing SQL queries.

  

**Database Migration**

Schema updates are manual right now and this is not flexible at all. I’ll use tools like Flask-Migrate to automate migrations.

  

**Scaling the System**

Some things I would like to explore and learn more in order to scale the system

-   Add load balancing for better traffic distribution.
    
-   Use read replicas for database scalability and sharding for very large datasets.
    
-   Containerize the app with Docker and manage scaling with Kubernetes.

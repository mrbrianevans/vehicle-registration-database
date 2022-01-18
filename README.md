# Vehicle registration database
This is a project for a university module titled "Database Technologies for Business Analytics".

## Database
A MongoDB document database is used to store records.

The `_id` field of each document in the `vehicle` collection is the vehicle license plate registration.

`mongoengine` is used as an object mapper to interact with the database from Python.

## Running the project
A prerequisite is a MongoDB database running on localhost.

Clone the git repository into a new directory. 

Install required dependencies with `pip install -r requirements.txt`.

Run `python main.py` to load the data into MongoDB, and perform some CRUD operations on it.

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

## Loading data
To load data into the database, create a file called `registrations.py` which contains a list 
of vehicle registration numbers like this:
```python
registrations = ['abc 123', 'def 456']
```
Run `get_data.py` to fetch the data for those registrations from the DVLA API and save it to the CSV.

To access the DVLA API, an API key is required. Set the environment variable `VES_KEY` to your API key.

Visit https://developer-portal.driver-vehicle-licensing.api.gov.uk/apis/vehicle-enquiry-service/vehicle-enquiry-service-description.html#vehicle-enquiry-service-api
for API documentation.

Once data is saved in `data.csv`, it can be inserted into MongoDB by running the `main.py` script.

import csv
import os
import requests
import json

from registrations import registrations  # data in registrations.py file

url = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
api_key = os.environ.get('VES_KEY')

if not api_key: raise SystemError('Environment variable VES_KEY not set. Add API key and try again')

def get_details(plate: str):
    payload = json.dumps({'registrationNumber': plate})
    req_headers = {'x-api-key': api_key, 'Content-Type': 'application/json'}
    r = requests.post(url, headers=req_headers, data=payload)
    # license_plate, brand, colour, manufactured_year, v5c_date, fuel_type, cyclinder_capacity
    # registrationNumber,make,colour,yearOfManufacture,dateOfLastV5CIssued,fuelType, engineCapacity
    if not r.ok: return
    j = r.json()
    car = dict()
    car['registration_number'] = plate
    car['brand'] = j['make'].capitalize()
    car['colour'] = j['colour'].capitalize()
    car['manufactured_year'] = j['yearOfManufacture']
    car['v5c_date'] = j['dateOfLastV5CIssued']
    car['fuel_type'] = j['fuelType'].capitalize()
    car['cyclinder_capacity'] = j['engineCapacity']

    return car


field_names = [
    'registration_number',
    'brand',
    'colour',
    'manufactured_year',
    'v5c_date',
    'fuel_type',
    'cyclinder_capacity'
]


def load_to_csv():
    csvfile = open('./data.csv', 'w', newline='')
    data = csv.DictWriter(csvfile, fieldnames=field_names)
    # data.writeheader()
    for reg in registrations:
        c = get_details(reg)
        if c is None: print(reg, 'is invalid')
        else: data.writerow(c)


if __name__ == '__main__':
    load_to_csv()

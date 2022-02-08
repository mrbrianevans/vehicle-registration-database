import datetime

from mongoengine import *
import csv


class Vehicle(Document):
    license_plate = StringField(primary_key=True, max_length=8)
    brand = StringField()
    colour = StringField()
    manufactured_year = IntField()
    v5c_date = DateField()
    fuel_type = StringField()
    cyclinder_capacity = IntField()


class Ticket(Document):
    vehicle = ReferenceField(Vehicle, required=True)
    issued_at = DateTimeField(default=lambda: datetime.datetime.now())
    duration_hours = IntField()
    payment_amount = FloatField()


class Fine(Document):
    vehicle = ReferenceField(Vehicle, required=True)
    ticket = ReferenceField(Ticket, required=False)
    amount = FloatField(required=True)
    paid = BooleanField(default=False)


def load_data():
    # read CSV of data and load it into mongodb
    csvfile = open('./data.csv', 'r')
    data = csv.DictReader(csvfile)
    for row in data:
        # performs create operation in mongo
        Vehicle(**row).save()
    csvfile.close()


if __name__ == '__main__':
    connect('bem2040')

    load_data()  # create data in database from csv

    # read operation
    car = Vehicle.objects(license_plate='PSM 100').first()
    print('Vehicle with license plate "PSM 100" is a', car.manufactured_year, car.brand)

    # update operation
    car = Vehicle.objects(license_plate='WM68 NFT').first()
    car.v5c_date = '2022-01-18'
    car.save()
    print('Updated V5C date for the vehicle with "WM68 NFT" license plate')

    # delete operation
    car = Vehicle.objects(license_plate='LTZ 1772').first()
    car.delete()
    print('Deleted vehicle with "LTZ 1772" license plate')

    # aggregation
    # count number of ferraris:
    ferraris = Vehicle.objects(brand='Ferrari').count()
    print(f'There are {ferraris} Ferraris in the database')

    # count all brands of diesel vehicles
    pipeline = [
        {"$match": {"fuel_type": "Diesel"}},
        {"$sortByCount": "$brand"},
        {"$addFields": {"brand": "$_id"}}
    ]
    diesel_brands = Vehicle.objects().aggregate(pipeline)
    for row in diesel_brands:
        print(row['brand'], 'has', row['count'], 'diesel cars in the database')

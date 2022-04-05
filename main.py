import datetime
import csv

from mongoengine import *


class Vehicle(Document):
    registration_number = StringField(primary_key=True, max_length=9)
    brand = StringField()
    colour = StringField()
    manufactured_year = IntField()
    v5c_date = DateField()
    fuel_type = StringField()
    cyclinder_capacity = IntField()


class Ticket(Document):
    # ticket_id is automatically created for each new ticket
    vehicle_registration = ReferenceField(Vehicle, required=True)
    issued_at = DateTimeField(default=lambda: datetime.datetime.now())
    duration_hours = FloatField(required=True)
    payment_amount = FloatField(required=True)


class Fine(Document):
    # fine_id is automatically created for each new fine
    vehicle_registration = ReferenceField(Vehicle, required=True)
    ticket_id = ReferenceField(Ticket, required=False)
    amount = FloatField(required=True)
    paid = BooleanField(default=False)


def load_data():
    # read CSV of vehicle data and load it into mongodb
    csvfile = open('./data.csv', 'r')
    data = csv.DictReader(csvfile)
    for row in data:
        # performs create operation in mongo
        Vehicle(**row).save()
    csvfile.close()


if __name__ == '__main__':
    connect('bem2040')
    # create vehicle in database
    car_data = {'registration_number': 'WV52 TPF', 'brand': 'Toyota', 'colour': 'Black',
                'manufactured_year': '2002', 'v5c_date': '2020-05-11', 'fuel_type': 'Petrol',
                'cyclinder_capacity': '1794'}
    car = Vehicle(**car_data)
    car.save()
    load_data()  # create vehicles data in database from csv
    print('Inserted vehicle data')

    # read operation
    car = Vehicle.objects(registration_number='WF20 TJU').first()
    if car:
        print('Query: vehicle with license plate "WF20 TJU" is a', car.manufactured_year, car.brand)

    # update operation
    car = Vehicle.objects(registration_number='WM68 NFT').first()
    car.v5c_date = '2022-01-18'
    car.save()
    print('Updated V5C date for the vehicle with "WM68 NFT" license plate')

    # delete operation
    car = Vehicle.objects(registration_number='WV52 TPF').first()
    car.delete()
    print('Deleted vehicle with "WV52 TPF" license plate')

    # aggregation
    # count number of ferraris:
    ferraris = Vehicle.objects(brand='Ferrari').count()
    print(f'There are {ferraris} Ferraris in the database')

    # count all brands of diesel vehicles
    pipeline = [
        {"$match": {"fuel_type": "Diesel"}},
        {"$sortByCount": "$brand"},
        {"$addFields": {"brand": "$_id"}},
        {"$limit": 3}
    ]
    diesel_brands = Vehicle.objects().aggregate(pipeline)
    for row in diesel_brands:
        print(row['brand'], 'has', row['count'], 'diesel cars in the database')

    # insert some sample parking tickets into the database
    ticket_data = [
        {'vehicle_registration': 'EX64 HBL', 'issued_at': '2022-04-05 10:30:56.706',
         'duration_hours': '0.50', 'payment_amount': '0.8'},
        {'vehicle_registration': 'YN57 NLC', 'issued_at': '2022-04-05 10:30:58.285',
         'duration_hours': '1', 'payment_amount': '1.5'},
        {'vehicle_registration': 'NU61 EDC', 'issued_at': '2022-04-05 10:31:02.184',
         'duration_hours': '0.75', 'payment_amount': '1'},
        {'vehicle_registration': 'WJ64 WZY', 'issued_at': '2022-04-05 10:31:04.873',
         'duration_hours': '1', 'payment_amount': '1.5'},
        {'vehicle_registration': 'BJ10 FXG', 'issued_at': '2022-04-05 10:31:08.385',
         'duration_hours': '0.50', 'payment_amount': '0.8'}
    ]
    for ticket in ticket_data:
        Ticket(**ticket).save()

    # insert a fine into the database
    ticket = Ticket.objects(vehicle_registration='WJ64 WZY').first()
    fine_data = {'vehicle_registration': 'WJ64 WZY', 'ticket_id': ticket, 'amount': '20',
                 'paid': 'false'}
    Fine(**fine_data).save()

    #     main success scenario
    vehicle_count = Vehicle.objects().count()  # count the number of cars in the database
    total_parking_bays = 200
    available_bays = total_parking_bays - vehicle_count
    print(f'There are {available_bays} available bays in the car parking lot')

    #     insert new car into database and issue a ticket
    new_car = Vehicle(registration_number='CK09 ENV', brand='Vauxhall', colour='Blue',
                      manufactured_year=2009, v5c_date='2020-12-30', fuel_type='Petrol',
                      cyclinder_capacity=1242)
    new_car.save()
    new_ticket = Ticket(vehicle_registration=new_car, duration_hours=2, payment_amount=2.40)
    new_ticket.save()

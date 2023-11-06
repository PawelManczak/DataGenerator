import random
import string
from datetime import datetime, timedelta
from random import choice

N_OF_AIRPORTS = 20
N_OF_AIRLINES = 10
airport_codes = []
airlines = []

N_OF_FLIGHTS = 100

def generate_airports():
    for i in range(N_OF_AIRPORTS):
        code = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(3))
        airport_codes.append(code)

def generate_airlines():
    pass


# Zakres dat - na przykład, loty w ciągu roku od dzisiaj
start_date = datetime.now()
end_date = start_date + timedelta(days=365)

def generate_flight_dates():
    departure_date = start_date + timedelta(days=random.randint(1, 365))
    arrival_date = departure_date + timedelta(hours=random.randint(1, 12), minutes=random.randint(0, 59))
    return departure_date, arrival_date

def generate_seat_counts():
    total_seats = random.randint(100, 200)  # Losowa liczba miejsc ogółem (np. od 100 do 200)
    business_class_seats = random.randint(10, total_seats // 3)  # Losowa liczba miejsc w klasie biznesowej (np. od 10 do 1/3 miejsc ogółem)
    economy_class_seats = total_seats - business_class_seats  # Liczba miejsc w klasie ekonomicznej to reszta

    # Wylosuj liczbę zajętych miejsc dla każdej klasy (od 0 do liczby miejsc w danej klasie)
    business_class_occupied = random.randint(0, business_class_seats)
    economy_class_occupied = random.randint(0, economy_class_seats)

    return {
        "total_seats": total_seats,
        "business_class_seats": business_class_seats,
        "economy_class_seats": economy_class_seats,
        "business_class_occupied": business_class_occupied,
        "economy_class_occupied": economy_class_occupied,
    }

if __name__ == '__main__':
    generate_airports()
    generate_airlines()

    print(airport_codes)
    with open('flight.txt', 'w') as f:
        for id in range(N_OF_FLIGHTS):
            # id
            f.write(str(id))

            departure_date, arrival_date = generate_flight_dates()
            # departure date
            f.write(str(departure_date))
            # arrival date
            f.write(str(arrival_date))
            # airport code
            f.write(airport_codes[random.randint(N_OF_AIRPORTS, 1)])

            seat_data = generate_seat_counts()
            # NumberOfEconomySeats
            f.write(str(seat_data["economy_class_seats"]))
            # NumberOfBuissnessSeats
            f.write(str(seat_data["business_class_seats"]))
            # NumberOfEconomyPassengers
            f.write(str(seat_data["economy_class_occupied"]))
            # NumberOfBuisnessPassengers
            f.write(str(seat_data["business_class_occupied"]))
            # airline id
            f.write(str(random.randint(N_OF_AIRLINES, 1)))

            economy_price = random.randint(500, 1)+250
            # business price
            f.write(str(economy_price*1.5))
            # economy price
            f.write(str(economy_price))



            f.write('\n')


"""
najpierw sheet 2
generujemy 20 lotnisk i mamy je w tabeli LOTNISKA
później sheet 1
Generujemy linie lotnicze i mamy je w tabelki

Generujemy X Flight i itemrujemy po x
Dla każdego x:
    Losujemy daty
    Airport code - tutaj losujemy z sheet2 - lotniska
    Numbery losujemy od 60-120
        Dla liczby pasażerów tworzymy tyle rezerwacji
            I od razu random passenger
         
    Airline id bierzemy z sheet 1
    ceny losujemy
    
    Flight delay ma 10% na utworzenie
        dane random, reason z kilku opcji
    Ticket refun ma 5% szns na utworzenie
    
"""
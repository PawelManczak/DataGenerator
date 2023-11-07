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
    business_class_seats = random.randint(10,
                                          total_seats // 3)  # Losowa liczba miejsc w klasie biznesowej (np. od 10 do 1/3 miejsc ogółem)
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


flight_delay_id = 0
DELAY_REASONS = ["whether", "crush", "other"]


def flight_delay(flight_id: int, file):
    if random.random() > 0.9:  # 10% chance
        file.write(str(flight_delay_id))
        file.write("|")
        file.write(str(flight_id))
        file.write("|")
        # delay duration
        file.write(str(random.randint(0, 1800)))
        file.write("|")
        # delay reason
        file.write(str(DELAY_REASONS[random.randint(0, len(DELAY_REASONS) - 1)]))
        file.write('\n')

        flight_id += 1


reservation_id = 0
passenger_id = 0
PAYMENT_METHODS = ["card", "cash"]


def reservation(file, flight_id, ticket_class, price_of_economy, price_of_business, date):
    file.write(str(reservation_id))
    file.write("|")
    file.write(str(flight_id))
    file.write("|")
    # todo generate passenger
    file.write(str(passenger_id))
    file.write("|")
    reservation_date = date - timedelta(days=random.randint(1, 365))
    file.write(str(reservation_date))
    file.write("|")
    if ticket_class == "business":
        file.write(str(price_of_business))
    else:
        file.write(str(price_of_economy))
    file.write("|")
    file.write(random.choice(PAYMENT_METHODS))
    file.write("|")
    if ticket_class == "business":
        file.write("business")
    else:
        file.write("economy")
    file.write("|")

    file.write('\nf')


if __name__ == '__main__':
    generate_airports()
    generate_airlines()

    print(airport_codes)
    with open('flight.txt', 'w') as f:
        with open('flight_delay.txt', 'w') as delay_file:
            with open('reservation.txt', 'w') as reservation_file:
                for id in range(N_OF_FLIGHTS):
                    # id
                    f.write(str(id))

                    departure_date, arrival_date = generate_flight_dates()
                    # departure date
                    f.write(str(departure_date))
                    f.write("|")
                    # arrival date
                    f.write(str(arrival_date))
                    f.write("|")
                    # airport code
                    f.write(airport_codes[random.randint(0, N_OF_AIRPORTS - 1)])
                    f.write("|")

                    seat_data = generate_seat_counts()
                    # NumberOfEconomySeats
                    f.write(str(seat_data["economy_class_seats"]))
                    f.write("|")
                    # NumberOfBuissnessSeats
                    f.write(str(seat_data["business_class_seats"]))
                    f.write("|")
                    # NumberOfEconomyPassengers
                    f.write(str(seat_data["economy_class_occupied"]))
                    f.write("|")
                    # NumberOfBuisnessPassengers
                    f.write(str(seat_data["business_class_occupied"]))
                    f.write("|")
                    # airline id
                    f.write(str(random.randint(0, N_OF_AIRLINES - 1)))
                    f.write("|")

                    economy_price = random.randint(0, 500) + 250
                    # business price
                    f.write(str(economy_price * 1.5))
                    f.write("|")
                    # economy price
                    f.write(str(economy_price))
                    f.write("|")

                    # other files

                    flight_delay(id, delay_file)

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

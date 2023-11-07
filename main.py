import random
from datetime import datetime, timedelta

N_OF_AIRPORTS = 20
N_OF_AIRLINES = 10
airport_codes = []
airlines = []

N_OF_FLIGHTS = 100


def generate_airports():
    with open('sheet2.txt', 'w') as f:
        for i in range(N_OF_AIRPORTS):
            code = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(3))
            f.write(code)
            f.write("|")
            name = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(7))
            f.write(name)
            f.write("|")
            location = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(7))
            f.write(location)
            f.write("|")

            airport_codes.append(code)


def generate_airlines():
    with open('sheet1.txt', 'w') as f:
        for airline_id in range(N_OF_AIRLINES):
            airlines.append(airline_id)

            f.write(str(airline_id))
            f.write("|")
            f.write(str(random.randint(5, 100)))
            f.write("|")


# Date range - flights within a year from today
start_date = datetime.now()
end_date = start_date + timedelta(days=365)


def generate_flight_dates():
    departure_date = start_date + timedelta(days=random.randint(1, 365))
    arrival_date = departure_date + timedelta(hours=random.randint(1, 12), minutes=random.randint(0, 59))
    return departure_date, arrival_date


def generate_seat_counts():
    total_seats = random.randint(100, 200)  # Random amount of all seats
    business_class_seats = random.randint(10,
                                          total_seats // 3)
    economy_class_seats = total_seats - business_class_seats

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
    global flight_delay_id
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

    flight_delay_id += 1


reservation_id = 0
passenger_id = 0
PAYMENT_METHODS = ["card", "cash"]


def reservation(file, flight_id, ticket_class, price_of_economy, price_of_business, date, passenger_file, is_delayed,
                refund_file):
    global reservation_id
    global passenger_id

    if (is_delayed and random.random() > 0.5) or random.random() > 0.8:
        price = price_of_business if ticket_class == "business" else price_of_economy

        ticket_refund(refund_file, reservation_id, date, price)

    file.write(str(reservation_id))
    file.write("|")
    file.write(str(flight_id))
    file.write("|")

    # generate passenger
    passenger_file.write(generate_passenger(passenger_id))
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

    file.write('\n')

    reservation_id += 1
    passenger_id += 1


def generate_passenger(passenger_id):
    first_name = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(5))
    last_name = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(10))
    date_of_birth = datetime(random.randint(1950, 2005), random.randint(1, 12), random.randint(1, 28))
    nationality = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(3))
    return f"{passenger_id}|{first_name}|{last_name}|{date_of_birth}|{nationality}\n"


refund_id = 0
REFUND_REASONS = ["delay", "other"]
REFUND_STATUS = ["accepted", "refused", "waiting"]


def ticket_refund(refund_file, reservation_id, date, price):
    global refund_id
    refund_file.write(str(refund_id))
    refund_file.write("|")
    refund_file.write(str(reservation_id))
    refund_file.write("|")

    refund_date = date + timedelta(hours=random.randint(1, 12), minutes=random.randint(0, 59),
                                   days=random.randint(0, 365))
    refund_file.write(str(refund_date))
    refund_file.write("|")
    refund_file.write(str(price))
    refund_file.write("|")
    refund_file.write(random.choice(REFUND_REASONS))
    refund_file.write("|")
    refund_file.write(random.choice(REFUND_STATUS))
    refund_id += 1


if __name__ == '__main__':
    generate_airports()
    generate_airlines()

    print(airport_codes)
    with open('flight.bulk', 'w') as f:
        with open('flight_delay.bulk', 'w') as delay_file:
            with open('reservation.bulk', 'w') as reservation_file:
                with open('passenger.bulk', 'w') as passenger_file:
                    with open('ticket_refund.bulk', 'w') as refund_file:
                        for id in range(N_OF_FLIGHTS):
                            is_delayed = False
                            # ticket refund
                            if random.random() > 0.9:  # 10% chance
                                flight_delay(id, delay_file)
                                is_delayed = True

                            # id
                            f.write(str(id))
                            f.write("|")
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
                            business_price = economy_price * 1.5
                            # business price
                            f.write(str(business_price))
                            f.write("|")
                            # economy price
                            f.write(str(economy_price))
                            f.write("|")
                            wasCancel = 0
                            if random.random() > 0.95:
                                wasCancel = 1
                            f.write(str(wasCancel))
                            f.write('\n')

                            # other files

                            for _ in range(seat_data["economy_class_occupied"]):
                                reservation(reservation_file, id, "economy", economy_price, business_price,
                                            departure_date,
                                            passenger_file, is_delayed, refund_file)
                            for _ in range(seat_data["business_class_occupied"]):
                                reservation(reservation_file, id, "business", economy_price, business_price,
                                            departure_date,
                                            passenger_file, is_delayed,
                                            refund_file)

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

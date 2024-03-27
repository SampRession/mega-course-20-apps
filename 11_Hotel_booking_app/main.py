import pandas as pd

df = pd.read_csv("resources/hotels.csv")
df_cards = (pd.read_csv("resources/cards.csv", dtype=str)
            .to_dict(orient="records"))
df_cards_security = pd.read_csv("resources/card_security.csv", dtype=str)

# NOTE: Commented class User (not working with property tests)

# class User:
#     def __init__(self, name):
#         self.name = name

#     def name(self):
#         name = f"{self.f_name} {self.l_name}"
#         return name


class Hotel:
    def __init__(self, h_id):
        self.h_id = h_id
        self.name = df.loc[df["id"] == self.h_id, "name"].squeeze()

    def view(self):
        """Return a list of hotels, with id, name, city, capacity,
        availability."""
        pass

    def available(self):
        """Return True or False, depending on hotel availability."""
        availability = df.loc[df["id"] == self.h_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    def book(self):
        """Book a hotel by changing its availability to 'no'"""
        df.loc[df["id"] == self.h_id, "available"] = "no"
        df.to_csv("resources/hotels.csv", index=False)


class ResTicket:
    def __init__(self, client_name, hotel_object):
        self.client = client_name
        self.hotel = hotel_object

    def generate(self):
        """Generate the reservation ticket for a specific hotel and
        client contained in __init__."""
        ticket_content = f"""
        Thank you for your reservation!
        Here are your booking data:
        Name: {self.clean_client_name}
        Hotel: {self.hotel.name}
        """
        return ticket_content

    @property
    def clean_client_name(self):
        name = self.client.strip().title()
        return name


class SpaHotel(Hotel):
    def book_spa_package(self):
        pass


class SpaResTicket(ResTicket):
    def generate(self):
        """Generate the reservation ticket for a spa package in the booked
        hotel in class Hotel"""
        ticket_content = f"""
        Thank you for your SPA reservation!
        Here are your SPA booking data:
        Name: {self.client_name}
        Hotel: {self.hotel.name}
        """
        return ticket_content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, cvc, holder):
        card_data = {"number": self.number, "expiration": expiration,
                     "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[
            df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


def clean_empty_rows():
    """Clean the DataFrame of any empty rows"""
    df = pd.read_csv("resources/hotels.csv")
    df.dropna(inplace=True)


def main():
    name = input("Enter your name: ")
    # client = User(name)
    clean_empty_rows()
    print(df)
    h_id = int(input("Enter the id of the hotel: "))
    if df["id"].eq(h_id).any():
        hotel = SpaHotel(h_id)
        if hotel.available():
            credit_card = SecureCreditCard(number="1234567890123456")
            if credit_card.validate(expiration="12/26", cvc="123",
                                    holder="JOHN SMITH"):
                if credit_card.authenticate(given_password="mypass"):
                    hotel.book()
                    clean_empty_rows()
                    res_ticket = ResTicket(client_name=name,
                                           hotel_object=hotel)
                    print(res_ticket.generate())
                    # New lines to ask for spa reservation and create res
                    # ticket for that
                    spa_choice = input("Do you want to book a spa package? ")
                    if spa_choice == "yes" or spa_choice == "Yes":
                        spa_res_ticket = SpaResTicket(client_name=name,
                                                      hotel_object=hotel)
                        print(spa_res_ticket.generate())
                else:
                    print("Credit card authentication failed.")
            else:
                print("Your credit card is not valid.")
        else:
            print("Hotel does not have any rooms available.")
    else:
        print("This hotel is not listed.")


if __name__ == "__main__":
    main()

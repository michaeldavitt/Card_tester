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
    next_year = 24
    year_list = list(range(next_year, next_year + n + 1))
    year = random.choice(year_list)
    return month, year


creds = []
for i in range(10):
    rand_card_num = random_with_N_digits(16)
    rand_exp = random_expiry(10)
    rand_cvc = random_with_N_digits(3)
    creds.append([rand_card_num, rand_exp[0], rand_exp[1], rand_cvc])

print(creds[:5])

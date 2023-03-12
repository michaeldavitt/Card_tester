# Purpose of this script is to simulate card testing
# Scenario - I've purchased some stolen credit card creds from the dark web and a leaked Stripe API key, and want to test if the cards will get declined or not
# Generate the card numbers
# Replace the card numbers with Stripe test cards
# Plug the card creds into the payment methods API
# Generate the customer objects
# Attach the payment method objects to the customer objects
# Store the successful card numbers for future use, and discard the rest

import stripe

with open("keys.txt") as f:
    PASSWORD = ''.join(f.readlines())
    stripe.api_key = str(PASSWORD).split()[0]

starter_subscription = stripe.Product.create(
    name="Starter Subscription",
    description="$12/Month subscription",
)

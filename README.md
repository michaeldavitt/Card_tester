# Stripe Card Testing Simulator
## Description
This project seeks to examine card testing, and how bad actors can exploit a Stripe merchant's poor API key security practices to test stolen cards to see which will pass issuer authentication, and which will be declined

Someone with access to a Stripe account/API key only needs three API calls to validate if a card is live, and thus can be useful to purchase expensive items online, or sold on the black market:

1. A call to the /v1/payment_methods API - https://stripe.com/docs/api/payment_methods/create
2. A call to the /v1/customers API - https://stripe.com/docs/api/customers/create
3. A call to the /v1/payment_methods/:id/attach API - https://stripe.com/docs/api/payment_methods/attach

Once a payment method has been attached to a customer, there are two possible outcomes:

1. The card will be declined by the bank, in which case the bad actor would simply discard it, as it is of no use to them
2. The card is successfully attached to the customer - since the card didn't decline, the card tester knows that this card is live, and can be used to commit fraud

Since I do not have access to stolen credit card data, I've used the random library to generate the required credentials (card number, expiry, and CVC code). For each randomly generated credit card, I've made test calls to the three Stripe APIs listed above. Finally, I export the successful cards to a CSV file and disgard the rest
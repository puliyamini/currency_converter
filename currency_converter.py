import requests


API_URL = "https://open.er-api.com/v6/latest/{}"


def get_exchange_rate(from_currency, to_currency):
    """Fetch the exchange rate between two currencies."""

    url = API_URL.format(from_currency)

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        data = response.json()

        if data.get("result") != "success":
            print("Error: Could not retrieve exchange rates.")
            return None

        rates = data.get("rates", {})

        if to_currency not in rates:
            print(f"Error: Currency '{to_currency}' is not supported.")
            return None

        return rates[to_currency]

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please try again.")

    except requests.exceptions.ConnectionError:
        print("Error: Check your internet connection.")

    except requests.exceptions.HTTPError:
        print("Error: The exchange-rate service returned an HTTP error.")

    except requests.exceptions.RequestException as error:
        print(f"Network error: {error}")

    except ValueError:
        print("Error: Invalid data received from the API.")

    return None


def convert_currency(amount, from_currency, to_currency):
    """Convert an amount from one currency to another."""

    rate = get_exchange_rate(from_currency, to_currency)

    if rate is None:
        return None

    converted_amount = amount * rate
    return converted_amount, rate


def main():
    print("=" * 45)
    print("         CURRENCY CONVERTER")
    print("=" * 45)

    print("Examples of currency codes: USD, INR, EUR, GBP, JPY")
    print("Currency code must contain three letters.")

    # Get the amount
    try:
        amount = float(input("\nEnter amount: ").strip())

        if amount <= 0:
            print("Error: Amount must be greater than zero.")
            return

    except ValueError:
        print("Error: Please enter a valid numeric amount.")
        return

    # Get source and target currencies
    from_currency = input(
        "Convert from currency (e.g., USD): "
    ).strip().upper()

    to_currency = input(
        "Convert to currency (e.g., INR): "
    ).strip().upper()

    # Validate currency codes
    if (
        len(from_currency) != 3
        or not from_currency.isalpha()
        or len(to_currency) != 3
        or not to_currency.isalpha()
    ):
        print("Error: Enter valid three-letter currency codes.")
        return

    print("\nFetching the latest available exchange rate...")

    # Convert the currency
    result = convert_currency(
        amount,
        from_currency,
        to_currency
    )

    if result is None:
        print("Currency conversion failed.")
        return

    converted_amount, rate = result

    # Display the result
    print("\n" + "=" * 45)
    print("          CONVERSION RESULT")
    print("=" * 45)

    print(f"Original amount : {amount:,.2f} {from_currency}")
    print(f"Exchange rate   : 1 {from_currency} = "
          f"{rate:.6f} {to_currency}")
    print(f"Converted amount: {converted_amount:,.2f} "
          f"{to_currency}")

    print("=" * 45)
    print("Rate provider: ExchangeRate-API")
    print("https://www.exchangerate-api.com/")
    print("Rates may differ from bank or card-provider rates.")


if __name__ == "__main__":
    main()
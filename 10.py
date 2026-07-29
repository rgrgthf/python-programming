def average_price(prices):
    return sum(prices) / len(prices)
def sorted_prices(prices):
    return sorted(prices.items(), key=lambda x: x[1])

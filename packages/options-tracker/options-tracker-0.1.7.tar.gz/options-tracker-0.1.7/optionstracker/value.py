from .vesting import vested


def value(size, grant_price, mkt_price):
    return size * (mkt_price - grant_price)


def value_at(
        size, grant_date, grant_price, vesting_rate, check_date, market_price):
    v, vu = vested(size, check_date, grant_date, vesting_rate)
    return (value(v, grant_price, market_price),
            value(vu, grant_price, market_price))

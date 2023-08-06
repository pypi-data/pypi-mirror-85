from dateutil.relativedelta import relativedelta


def vested(quantity, check_date, grant_date, vest_rate, vest_interval='m'):
    elapsed = relativedelta(check_date, grant_date)
    if elapsed.years >= 3:
        return (quantity, 0)
    if vest_interval == 'm':
        v = int((12 * elapsed.years + elapsed.months) * vest_rate * quantity)
    elif vest_interval == 'y':
        v = int(elapsed.years * vest_rate * quantity)
    return (v, quantity - v)


def vesting_profile(
        grant_quantity, grant_date, vesting_rate,
        profile_interval=relativedelta(months=+1)):
    d = grant_date
    p = []
    uv = grant_quantity
    while uv > 0:
        v, uv = vested(grant_quantity, d, grant_date, vesting_rate)
        p.append((d, v, uv))
        d = d + profile_interval
    return p

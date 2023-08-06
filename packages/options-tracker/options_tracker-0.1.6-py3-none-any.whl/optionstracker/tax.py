from math import floor


def capital_gains_tax(
        gain, tax_free_allowance_remaining=1230000,
        higher_rate_income_tax=True):
    if gain < tax_free_allowance_remaining:
        return 0
    if higher_rate_income_tax:
        return floor(0.2 * (gain - tax_free_allowance_remaining))

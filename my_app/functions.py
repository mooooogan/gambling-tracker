# tai calculations
# gang and gaoyin calculations


def tai_calculation(number_of_tai, price_tai, zimo):
    if number_of_tai == 0:
        price_tai = price_tai / 2
    if zimo:
        per_person = (price_tai * (2 ** (int(number_of_tai) - 1))) * 2
        total_amount = per_person * 3
    else:
        per_person = price_tai * (2 ** (int(number_of_tai) - 1))
        total_amount = per_person * 4
    return total_amount, per_person


def gang_calculations(price, am_gang):
    if am_gang:
        total_amount = price * 2 * 3
    else:
        total_amount = price * 3

    return total_amount

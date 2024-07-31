def extract_by_date(transactions, type):
    sign = 1 if type == 'Income' else -1
    days_in_month = 31
    Income_by_date = [0] * days_in_month

    for transaction in transactions:
        if transaction['Category'] == type:
            if transaction['Day'] < days_in_month:
                amount = sign * float(transaction['Amount'])
                Income_by_date[transaction['Day']] += amount

    return Income_by_date
def analyze_transactions(transactions,type):
    Income = 0
    Spending = 0
    for transaction in transactions:
        if transaction['Category'] == 'Income':
            Income += float(transaction['Amount'])
        elif transaction['Category'] == 'Expense':
            Spending += float(transaction['Amount'])
    return Income, Spending
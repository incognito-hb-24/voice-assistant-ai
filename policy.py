
def check(intent, entities, risk):
    decision = {
        'allowed': True,
        'step_up': False,
        'risk': risk,
        'notes': []
    }

    if intent == 'transfer':
        amount = entities.get('amount', 0) or 0
        if amount <= 0:
            decision['allowed'] = False
            decision['notes'].append('Amount is missing or invalid.')
        if entities.get('payee') is None:
            decision['allowed'] = False
            decision['notes'].append('Payee name is missing.')
        if amount >= 1000:
            decision['step_up'] = True
            decision['notes'].append('High-value transfer requires OTP verification.')

    return decision

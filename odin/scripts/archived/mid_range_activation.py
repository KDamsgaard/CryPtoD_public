"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""

script_name = __name__.split(".")[-1]
arg_fields = [['_trades'],
              ['_pair_settings', 'factors']]
factors = {'short': {'value': 0, 'increment': 1, 'constraints': [{'operator': '>=', 'value': 0}]},
           'long': {'value': 0, 'increment': 10, 'constraints': [{'operator': '>', 'value': 'short'}]},
           'tension': {'value': 0, 'increment': 100, 'constraints': [{'operator': '>', 'value': 'long'},
                                                                     {'operator': '!=', 'value': None}]}
           }


def primary_function(pair_name, log, args: list):
    trades = args[0]
    factors = args[1]

    for key in factors.keys():
        val = factors[key]['value']
        if isinstance(val, str) and not val or val < 0:
            print(f"Detected erroneous factor value! {factors[key]}")

    if trades:
        now = trades[-1]['time']
        calculations = calculate(now=now,
                                 factors=factors,
                                 trades=trades)
        if calculations:
            decision = make_decision(log=log, calculations=calculations)
            analysis = {'time': now, 'calculations': calculations, 'decision': decision}
            return analysis

    else:
        log.debug(f"{pair_name} - {script_name} received one or more empty arguments")
        return False


def calculate(now, factors, trades):
    calculations = {'short': None, 'long': None, 'tension': None}

    timeframe_short = now - minutes_to_seconds(minutes=factors['short']['value'])
    timeframe_long = now - minutes_to_seconds(minutes=factors['long']['value'])
    timeframe_tension = now - minutes_to_seconds(minutes=factors['tension']['value'])

    total = 0
    count = 0
    for trade in trades[::-1]:
        total += trade['price']
        count += 1

        if not calculations['short']:
            if trade['time'] < timeframe_short:
                new_sma = total / count
                calculations['short'] = new_sma
        if not calculations['long']:
            if trade['time'] < timeframe_long:
                new_sma = total / count
                calculations['long'] = new_sma
        if not calculations['tension']:
            if trade['time'] < timeframe_tension:
                new_sma = total / count
                calculations['tension'] = new_sma
                break
    if calculations['short'] and calculations['long'] and calculations['tension']:
        return calculations
    else:
        return None


def make_decision(log, calculations):
    decision = {'direction': None, 'estimated_price': None}

    short = calculations['short']
    long = calculations['long']
    tension = calculations['tension']

    try:
        if tension > short > long:
            decision['direction'] = 'b'
        if tension < short < long:
            decision['direction'] = 's'
    except TypeError:
        log.error(f"Something went wrong - {calculations}")
        pass

    if decision['direction']:
        decision['estimated_price'] = short
        return decision
    else:
        return None


def minutes_to_seconds(minutes):
    """
    Converts minutes to seconds for use when comparing timeframes with timestamps. Note that unix
    timestamps are created as seconds (IE: divides the timestamp by 1000), hence this function does not return
    milliseconds.

    :param minutes: The amount of minutes to convert to seconds
    :return: Parameter "Minutes" in seconds
    """
    return minutes * 60

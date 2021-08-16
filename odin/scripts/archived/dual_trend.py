"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Søren B. Ølholm
"""

script_name = __name__.split(".")[-1]
arg_fields = [['_trades'],
              ['_settings', 'factors'],
              ['_analyses']]
factors = {'short': {'value': 1, 'increment': 0.1},
           'threshold': {'value': 1, 'increment': 0.1}}


def primary_function(pair_name, log, args: list):
    trades = args[0]
    factors = args[1]
    analyses = args[2]

    now = trades[-1]['time']

    if trades and factors:
        calculations = calculate(log=log,
                                 trades=trades,
                                 analyses=analyses,
                                 factors=factors,
                                 now=now)
        if calculations:
            decision = make_decision(log=log, calculations=calculations)
            analysis = {'time': now, 'calculations': calculations, 'decision': decision}
            return analysis

    else:
        log.debug(f"{pair_name} - {script_name} received one or more empty arguments")
        return False


def calculate(log, trades, analyses, factors, now):
    calculations = {'short_sma': None, 'vtrend_short': None, 'trend': None}

    tf_short = factors['short']['value']
    tf_threshold = factors['threshold']['value']
    tf_short = now - minutes_to_seconds(minutes=tf_short)
    tf_threshold = now - minutes_to_seconds(minutes=tf_threshold)

    total = 0
    count = 0
    for trade in trades[::-1]:
        total += trade['price']
        count += 1

        if not calculations['short_sma']:
            if trade['time'] < tf_short:
                new_sma = total / count
                calculations['short_sma'] = new_sma
                break

    pvolume_short = None
    svolume_short = None

    total = 0
    for trade in trades[::-1]:
        if trade['direction'] == 'b':
            total += trade['volume']
            if not pvolume_short:
                if trade['time'] < tf_short:
                    pvolume_short = total
                    break
    total = 0
    for trade in trades[::-1]:
        if trade['direction'] == 's':
            total += trade['volume']
            if not svolume_short:
                if trade['time'] < tf_short:
                    svolume_short = total
                    break

    last_short_sma = None
    if analyses:
        for analysis in analyses[::-1]:
            lss = analysis['calculations']['short_sma']
            if not last_short_sma:
                if analysis['time'] < tf_threshold:
                    last_short_sma = lss
                    break

    if last_short_sma:
        if calculations['short_sma'] > last_short_sma:
            calculations['trend'] = 1
        elif calculations['short_sma'] == last_short_sma:
            calculations['trend'] = 0
            calculations['sma_diff'] = 0
        else:
            calculations['trend'] = -1
    else:
        calculations['trend'] = 0
        calculations['sma_diff'] = 0

    if pvolume_short and svolume_short:
        calculations['vtrend_short'] = pvolume_short - svolume_short
    else:
        pass

    if calculations['short_sma'] and calculations['vtrend_short']:
        return calculations
    else:
        return False


def make_decision(log, calculations):
    decision = {'direction': None, 'estimated_price': None}
    vtrend_short = calculations['vtrend_short']
    trend = calculations['trend']
    short_sma = calculations['short_sma']

    # log.info(f'calculations {calculations}')

    # --> Good
    # if vtrend_short >= 0 and short_sma > tension_sma:
    #     decision['direction'] = 'b'
    #     decision['estimated_price'] = short_sma
    # if short_sma < long_sma:
    #     decision['direction'] = 's'
    #     decision['estimated_price'] = short_sma

    # --> Good needs backstop for buys
    if not trend or trend == 1 and vtrend_short > 0:
        decision['direction'] = 'b'
        decision['estimated_price'] = short_sma
    if not trend or trend == -1 and vtrend_short < 0:
        decision['direction'] = 's'
        decision['estimated_price'] = short_sma
    return decision


def minutes_to_seconds(minutes):
    """
    Converts minutes to seconds for use when comparing timeframes with timestamps. Note that unix
    timestamps are created as seconds (IE: divides the timestamp by 1000), hence this function does not return
    milliseconds.

    :param minutes: The amount of minutes to convert to seconds
    :return: Parameter "Minutes" in seconds
    """
    return minutes * 60

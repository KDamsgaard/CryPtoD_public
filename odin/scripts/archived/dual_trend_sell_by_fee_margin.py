"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Søren B. Ølholm
"""

script_name = __name__.split(".")[-1]
arg_fields = [['_trades'],
              ['_settings', 'timeframes'],
              ['_settings', 'modifiers'],
              ['_settings', 'fees'],
              ['_analyses']]


def primary_function(pair_name, log, args: list):
    trades = args[0]
    timeframes = args[1]
    modifiers = args[2]
    fees = args[3]
    analyses = args[4]

    now = trades[-1]['time']

    if trades and timeframes:
        calculations = calculate(log=log,
                                 trades=trades,
                                 fees=fees,
                                 analyses=analyses,
                                 timeframes=timeframes,
                                 now=now)
        if calculations:
            decision = make_decision(log=log, fees=fees, calculations=calculations)
            analysis = {'time': now, 'calculations': calculations, 'decision': decision}
            return analysis

    else:
        log.debug(f"{pair_name} - {script_name} received one or more empty arguments")
        return False


def calculate(log, trades, fees, analyses, timeframes, now):
    calculations = {'short_sma': None, 'long_sma': None, 'sma_diff': None, 'vtrend_short': None, 'trend': None}

    tf_short = timeframes['short']
    tf_long = timeframes['long']
    tf_threshold = timeframes['threshold']
    tf_short = now - minutes_to_seconds(minutes=tf_short)
    tf_long = now - minutes_to_seconds(minutes=tf_long)
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
        if not calculations['long_sma']:
            if trade['time'] < tf_long:
                new_sma = total / count
                calculations['long_sma'] = new_sma
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
    last_long_sma = None
    if analyses:
        for analysis in analyses[::-1]:
            lss = analysis['calculations']['long_sma']
            if not last_long_sma:
                if analysis['time'] < tf_long:
                    last_long_sma = lss
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
    if last_long_sma:
        calculations['sma_diff'] = 100 - ((last_long_sma / calculations['long_sma']) * 100)
    else:
        calculations['sma_diff'] = 0

    # if analyses and calculations['short_sma']:
    #     if calculations['short_sma'] > analyses[-1]['calculations']['short_sma']:
    #         calculations['trend'] = 1
    #     elif calculations['short_sma'] == analyses[-1]['calculations']['short_sma']:
    #         calculations['trend'] = 0
    #     else:
    #         calculations['trend'] = -1
    # else:
    #     calculations['trend'] = 0

    if pvolume_short and svolume_short:
        calculations['vtrend_short'] = pvolume_short - svolume_short

    if calculations['short_sma'] and calculations['vtrend_short']:
        return calculations
    else:
        return False


def make_decision(log, calculations, fees):
    decision = {'direction': None, 'estimated_price': None}
    vtrend_short = calculations['vtrend_short']
    trend = calculations['trend']
    short_sma = calculations['short_sma']
    long_sma = calculations['long_sma']
    sma_diff = calculations['sma_diff']

    #log.info(f'calculations {calculations}')

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
    # if not trend or trend == -1 and vtrend_short < 0:
    #     decision['direction'] = 's'
    #     decision['estimated_price'] = short_sma
    if sma_diff > fees['taker']*2:
        decision['direction'] = 's'
        decision['estimated_price'] = short_sma
    #print(f'Sell decision sma_diff {sma_diff}/{fees["taker"]}')
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
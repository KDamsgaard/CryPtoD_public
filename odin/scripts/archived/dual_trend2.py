"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Søren B. Ølholm
"""


#dual_trends2
script_name = __name__.split(".")[-1]
arg_fields = [['_trades'],
              ['_pair_settings', 'factors'],
              ['_analyses']]


def primary_function(pair_name, log, args: list):
    trades = args[0]
    settings = args[1]
    #print(settings)
    timeframes = settings['timeframes']
    modifiers = settings['modifiers']
    analyses = args[2]

    now = trades[-1]['time']

    if trades and timeframes:
        calculations = calculate(log=log,
                                 trades=trades,
                                 analyses=analyses,
                                 timeframes=timeframes,
                                 modifiers=modifiers,
                                 now=now)
        if calculations:
            #print(calculations)
            decision = make_decision(log=log, calculations=calculations)
            analysis = {'time': now, 'calculations': calculations, 'decision': decision}
            #print(analysis)
            return analysis

    else:
        log.debug(f"{pair_name} - {script_name} received one or more empty arguments")
        return False


def _calc_buy(calculations, trades, analyses, timeframes, modifiers, now):
    tf_buy_long = timeframes['long']
    tf_buy_threshold = modifiers['buy']
    tf_buy_long = now - minutes_to_seconds(minutes=tf_buy_long)
    tf_buy_threshold = now - minutes_to_seconds(minutes=tf_buy_threshold)

    total = 0
    count = 0
    for trade in trades[::-1]:
        total += trade['price']
        count += 1

        if not calculations['long_sma']:
            if trade['time'] < tf_buy_long:
                new_sma = total / count
                calculations['long_sma'] = new_sma
                break

    pvolume = None
    svolume = None

    total = 0
    for trade in trades[::-1]:
        if trade['direction'] == 'b':
            total += trade['volume']
            if not pvolume:
                if trade['time'] < tf_buy_long:
                    pvolume = total
                    break
    total = 0
    for trade in trades[::-1]:
        if trade['direction'] == 's':
            total += trade['volume']
            if not svolume:
                if trade['time'] < tf_buy_long:
                    svolume = total
                    break

    last_sma = None
    if analyses:
        for analysis in analyses[::-1]:
            lss = analysis['calculations']['long_sma']
            if not last_sma:
                if analysis['time'] < tf_buy_threshold:
                    last_sma = lss
                    break

    if last_sma:
        if calculations['long_sma'] > last_sma:
            calculations['long_trend'] = 1
        elif calculations['long_sma'] == last_sma:
            calculations['long_trend'] = 0
        else:
            calculations['long_trend'] = -1
    else:
        calculations['long_trend'] = 0

    if pvolume and svolume:
        calculations['vtrend_long'] = pvolume - svolume
    else:
        pass

    return calculations

def _calc_sell(calculations, trades, analyses, timeframes, modifiers, now):
    tf_sell_short = timeframes['short']
    tf_sell_threshold = modifiers['sell']
    tf_sell_short = now - minutes_to_seconds(minutes=tf_sell_short)
    tf_sell_threshold = now - minutes_to_seconds(minutes=tf_sell_threshold)

    total = 0
    count = 0
    for trade in trades[::-1]:
        total += trade['price']
        count += 1

        if not calculations['long_sma']:
            if trade['time'] < tf_sell_short:
                new_sma = total / count
                calculations['long_sma'] = new_sma
                break

    pvolume = None
    svolume = None

    total = 0
    for trade in trades[::-1]:
        if trade['direction'] == 'b':
            total += trade['volume']
            if not pvolume:
                if trade['time'] < tf_sell_short:
                    pvolume = total
                    break
    total = 0
    for trade in trades[::-1]:
        if trade['direction'] == 's':
            total += trade['volume']
            if not svolume:
                if trade['time'] < tf_sell_short:
                    svolume = total
                    break

    last_sma = None
    if analyses:
        for analysis in analyses[::-1]:
            lss = analysis['calculations']['short_sma']
            if not last_sma:
                if analysis['time'] < tf_sell_threshold:
                    last_sma = lss
                    break

    if last_sma:
        if calculations['short_sma'] > last_sma:
            calculations['short_trend'] = 1
        elif calculations['short_sma'] == last_sma:
            calculations['short_trend'] = 0
        else:
            calculations['short_trend'] = -1
    else:
        calculations['short_trend'] = 0

    if pvolume and svolume:
        calculations['vtrend_short'] = pvolume - svolume
    else:
        pass

    return calculations

def calculate(log, trades, analyses, timeframes, modifiers, now):
    calculations = {'super_short_sma': None, 'short_sma': None, 'long_sma': None, 'vtrend_short': None, 'vtrend_long': None, 'short_trend': None, 'long_trend': None}

    total = 0
    count = 0
    for trade in trades[::-1]:
        total += trade['price']
        count += 1
        if not calculations['super_short_sma']:
            if count == 5:
                calculations['super_short_sma'] = total / count
                break

    calculations = _calc_buy(calculations, trades, analyses, timeframes, modifiers, now)
    calculations = _calc_sell(calculations, trades, analyses, timeframes, modifiers, now)

    if calculations['short_sma'] and calculations['vtrend_short'] or calculations['long_sma'] and calculations['vtrend_long']:
        return calculations
    else:
        return False


def make_decision(log, calculations):
    decision = {'direction': None, 'estimated_price': None}
    vtrend_short = calculations['vtrend_short']
    vtrend_long = calculations['vtrend_long']
    short_trend = calculations['short_trend']
    long_trend = calculations['long_trend']
    super_short_sma = calculations['super_short_sma']
    short_sma = calculations['short_sma']
    long_sma = calculations['long_sma']

    #log.info(f'calculations {calculations}')

    # --> Good
    # if vtrend_short >= 0 and short_sma > tension_sma:
    #     decision['direction'] = 'b'
    #     decision['estimated_price'] = short_sma
    # if short_sma < long_sma:
    #     decision['direction'] = 's'
    #     decision['estimated_price'] = short_sma

    # --> Good needs backstop for buys
    decision['estimated_price'] = super_short_sma
    if not short_trend or short_trend == -1 and vtrend_short < 0:
        decision['direction'] = 's'
        decision['estimated_price'] = super_short_sma
    if not long_trend or long_trend == 1 and vtrend_long > 0:
        decision['direction'] = 'b'
        decision['estimated_price'] = super_short_sma
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
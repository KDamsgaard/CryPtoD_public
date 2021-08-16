
script_name = __name__.split(".")[-1]
arg_fields = [['_trades'],
              ['_settings', 'timeframes']]
triggers = ['b', 's']

def primary_function(pair_name, log, args: list):
    trades = args[0]
    timeframes = args[1]

    now = trades[-1]['time']

    if trades and timeframes:
        calculations = calculate(trades=trades, timeframes=timeframes, now=now, log=log)
        if calculations:
            decision = make_decision(calculations=calculations)
            analysis = {'time': now, 'calculations': calculations, 'decision': decision}
            return analysis

    else:
        log.debug(f"{pair_name} - {script_name} received one or more empty arguments")
        return False


def calculate(trades, timeframes, now, log):
    calculations = {'ptrend': 0, 'vtrend': 0, 'sma': 0}

    tf_short = timeframes['short']

    tf_short = now - minutes_to_seconds(minutes=tf_short)

    total_purchases_price = 0
    total_sales_price = 0
    total_purchases_volume = 0
    total_sales_volume = 0
    count_purchases = 0
    count_sales = 0
    for trade in trades[::-1]:
        if not calculations['ptrend']:
            btime = trade['time']
            stime = trade['time']
            if trade['direction'] == 'b':
                total_purchases_price += trade['price']
                total_purchases_volume += trade['volume']
                count_purchases += 1
                btime = trade['time']
            if trade['direction'] == 's':
                total_sales_price += trade['price']
                total_sales_volume += trade['volume']
                count_sales += 1
                stime = trade['time']

            if btime < tf_short and stime < tf_short:
                break

    if count_purchases > 0 and count_sales > 0:
        calculations['ptrend'] = total_purchases_price / count_purchases
        calculations['vtrend'] = total_purchases_volume / count_purchases
        calculations['ptrend'] = calculations['ptrend'] - (total_sales_price / count_sales)
        calculations['vtrend'] = calculations['vtrend'] - (total_sales_volume / count_sales)
        calculations['psma'] = total_purchases_price / count_purchases
        calculations['ssma'] = total_sales_price / count_sales

    if calculations['ptrend']:
        return calculations
    else:
        return False


def make_decision(calculations):
    decision = {'direction': None, 'estimated_price': None}
    ptrend = calculations['ptrend']
    vtrend = calculations['vtrend']
    ssma = calculations['ssma']
    psma = calculations['psma']

    decision['direction'] = None
    decision['estimated_price'] = 0

    if vtrend > 0 and ptrend > 0:
        decision['direction'] = 'b'
        decision['estimated_price'] = psma
    if vtrend < 0 and ptrend < 0:
        decision['direction'] = 's'
        decision['estimated_price'] = ssma
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
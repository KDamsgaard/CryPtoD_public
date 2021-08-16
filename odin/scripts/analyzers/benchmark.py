"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""
import time

script_name = __name__.split(".")[-1]
arg_fields = [['_trades'],
              ['_settings', 'timeframes']]
start = 0
stop = 0


def primary_function(pair_name, log, args: list):
    trades = args[0]
    timeframes = args[1]

    global start
    global stop

    if trades and timeframes:
        start = time.time()
        benchmark = {'start': start, 'stop': None, 'elapsed': None}
        calculations = fake_work_calculate(trades=trades, timeframes=timeframes, now=start)
        decision = fake_work_make_decision(calculations=calculations)
        stop = time.time()
        benchmark['stop'] = stop
        benchmark['elapsed'] = stop - start
        analysis = {'time': start, 'benchmark': benchmark, 'calculations': calculations, 'decision': decision}
        return analysis

    else:
        log.debug(f"{pair_name} - {script_name} received one or more empty arguments")
        return False


def fake_work_calculate(trades, timeframes, now):
    calculations = {'short_sma': None, 'long_sma': None, 'tension_sma': None}

    tf_short = timeframes['short']
    tf_long = timeframes['long']
    tf_tension = timeframes['tension']

    tf_short = now - minutes_to_seconds(minutes=tf_short)
    tf_long = now - minutes_to_seconds(minutes=tf_long)
    tf_tension = now - minutes_to_seconds(minutes=tf_tension)

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
        if not calculations['tension_sma']:
            if trade['time'] < tf_tension:
                new_sma = total / count
                calculations['tension_sma'] = new_sma
                break
    return calculations


def fake_work_make_decision(calculations):
    decision = {'direction': None, 'estimated_price': None}
    short = calculations['short_sma']
    long = calculations['long_sma']
    tension = calculations['tension_sma']

    if short and long and tension:
        if tension > short > long:
            decision['direction'] = 'b'
            decision['estimated_price'] = short
        if tension < short < long:
            decision['direction'] = 's'
            decision['estimated_price'] = short
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
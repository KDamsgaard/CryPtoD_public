"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""

import time

script_name = __name__.split(".")[-1]
arg_fields = [['_trades', 'purchases'],
              ['_settings', 'timeframes']]
triggers = ['b']


def primary_function(args: list):
    trades = args[0]
    timeframes = args[1]
    last_smas = trades[-1]['smas']

    smas = {'short': None, 'long': None, 'tension': None}
    trends = {'short': None, 'long': None, 'tension': None}
    analysis = {'time': time.time(), 'smas': smas, 'trends': trends}
    total = 0
    count = 0

    tf_short = analysis['time'] - minutes_to_seconds(minutes=timeframes['short'])
    tf_long = analysis['time'] - minutes_to_seconds(minutes=timeframes['long'])
    tf_tension = analysis['time'] - minutes_to_seconds(minutes=timeframes['tension'])

    for trade in trades[::-1]:
        total += trade['price']
        count += 1

        if not smas['short']:
            if trade['time'] < tf_short:
                new_sma = total / count
                trends['short'] = calculate_trend(new_sma=new_sma, old_sma=last_smas['short'])
                smas['short'] = new_sma
        if not smas['long']:
            if trade['time'] < tf_long:
                new_sma = total / count
                trends['long'] = calculate_trend(new_sma=new_sma, old_sma=last_smas['long'])
                smas['long'] = new_sma
        if not smas['tension']:
            if trade['time'] < tf_tension:
                new_sma = total / count
                trends['tension'] = calculate_trend(new_sma=new_sma, old_sma=last_smas['tension'])
                smas['tension'] = new_sma
                break

    if smas['tension']:
        return analysis
    else:
        return False


def calculate_trend(new_sma, old_sma):
    if old_sma:
        if new_sma < old_sma:
            return -1
        elif new_sma > old_sma:
            return 1
    return 0


def minutes_to_seconds(minutes):
    """
    Converts minutes to seconds for use when comparing timeframes with timestamps. Note that unix
    timestamps are created as seconds (IE: divides the timestamp by 1000), hence this function does not return
    milliseconds.

    :param minutes: The amount of minutes to convert to seconds
    :return: Parameter "Minutes" in seconds
    """
    return minutes * 60
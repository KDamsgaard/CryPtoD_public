"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""

script_name = __name__.split(".")[-1]
arg_fields = [['_trades', 'purchases'],
              ['_settings', 'timeframes']]
triggers = ['b']

def primary_function(pair_name, log, args: list):
    if args[0]:
        trades = args[0]
        timeframes = args[1]

        t = trades[-1]['time']

        smas = {'short': None, 'long': None, 'tension': None}
        analysis = {'time': t, 'smas': smas}

        tf_short = timeframes['short']
        tf_long = timeframes['long']
        tf_tension = timeframes['tension']

        tf_short = analysis['time'] - minutes_to_seconds(minutes=tf_short)
        tf_long = analysis['time'] - minutes_to_seconds(minutes=tf_long)
        tf_tension = analysis['time'] - minutes_to_seconds(minutes=tf_tension)

        total = 0
        count = 0
        for trade in trades[::-1]:
            total += trade['price']
            count += 1

            if not smas['short']:
                if trade['time'] < tf_short:
                    new_sma = total / count
                    smas['short'] = new_sma
            if not smas['long']:
                if trade['time'] < tf_long:
                    new_sma = total / count
                    smas['long'] = new_sma
            if not smas['tension']:
                if trade['time'] < tf_tension:
                    new_sma = total / count
                    smas['tension'] = new_sma
                    break
        if smas['tension']:
            log.debug(f"{pair_name} - {script_name} computed a new analysis")
            return analysis
        else:
            log.debug(f"{pair_name} - {script_name} was unable to calculate a tension")
            return False
    else:
        log.debug(f"{pair_name} - {script_name} received empty trades array")


def minutes_to_seconds(minutes):
    """
    Converts minutes to seconds for use when comparing timeframes with timestamps. Note that unix
    timestamps are created as seconds (IE: divides the timestamp by 1000), hence this function does not return
    milliseconds.

    :param minutes: The amount of minutes to convert to seconds
    :return: Parameter "Minutes" in seconds
    """
    return minutes * 60


script_name = __name__.split(".")[-1]
arg_fields = [['_analyses', 'purchases'],
              ['_settings']]


def primary_function(pair_name, log, args: list):
    """
    This is essentially a worse version of "peak_trading".

    Uses purchase analyses (SMAs).

    Tracks long SMA minimum and maximum and current short SMA.
    If short SMA is above long SMA min * modifier factor; will buy.
    If short SMA is below long SMA max * modifier factor; will sell.

    Threshold is the amount of hours to track long SMA.

    Note that tension SMA is used to keep analyses from being removed from the pairwatcher. This is not a good option.
    """
    analyses = args[0]
    if analyses:
        settings = args[1]
        threshold = settings['timeframes']['threshold']
        modifiers = settings['modifiers']
        buy_factor = 1 + (modifiers['buy'] / 100)
        sell_factor = 1 - (modifiers['sell'] / 100)

        newest_analysis = analyses[-1]
        now = newest_analysis['time']

        short = newest_analysis['smas']['short']

        decision = {'time': now, 'direction': None, 'estimated_price': None, "details": {}}

        long_high = newest_analysis['smas']['long']
        long_low = long_high
        for analysis in analyses:
            if analysis['time'] > now - threshold:
                if analysis['smas']['long'] < long_low:
                    long_low = analysis['smas']['long']
                if analysis['smas']['long'] > long_high:
                    long_high = analysis['smas']['long']

        decision['details'] = {'short': short,
                               'long_low': long_low,
                               'long_high': long_high,
                               'factors': {'buy': buy_factor,
                                           'sell': sell_factor}}

        if short > long_high * sell_factor:
            decision['direction'] = 's'
        if short < long_low * buy_factor:
            decision['direction'] = 'b'

        if decision['direction']:
            decision['estimated_price'] = short
            return decision
    return False


def _hours_to_seconds(hours):
    """
    Converts minutes to seconds for use when comparing timeframes with timestamps. Note that unix
    timestamps are created as seconds (IE: divides the timestamp by 1000), hence this function does not return
    milliseconds.

    :param minutes: The amount of minutes to convert to seconds
    :return: Parameter "Minutes" in seconds
    """
    return hours * 60 * 60

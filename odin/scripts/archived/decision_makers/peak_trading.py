
script_name = __name__.split(".")[-1]
arg_fields = [['_analyses', 'purchases'],
              ['_settings']]


def primary_function(pair_name, log, args: list):
    """
    Tracks tension and short SMA, reacting when short SMA moves far enough above or blow tension.
    Buy and sell modifiers can be adjusted to have the algorithm react quicker with lower settings, and vice versa.
    Short SMA and tension can be adjusted to have tension "lag behind" making decisions more likely.

    The algorithm contains no back-stop, however, and this will have to be implemented.

    Good settings so far (for BTC only):
    Short   Tension Buy     Sell    Note
    0.5     60      0.20    0.40    Yields good results
    1       20      0.25    0.40    Seems stable and safe
    1       20      0.20    0.40    Slightly more willing to take risks, more trades overall
    """
    analyses = args[0]
    if analyses:
        settings = args[1]
        modifiers = settings['modifiers']
        buy_factor = 1 - (modifiers['buy'] / 100)
        sell_factor = 1 + (modifiers['sell'] / 100)

        newest_analysis = analyses[-1]
        now = newest_analysis['time']
        short = newest_analysis['smas']['short']
        long = newest_analysis['smas']['long']
        tension = newest_analysis['smas']['tension']

        decision = {'time': now, 'direction': None, 'estimated_price': None}

        if short > tension * sell_factor:
            decision['direction'] = 's'
        if short < tension * buy_factor and tension < long:
            decision['direction'] = 'b'

        if decision['direction']:
            decision['estimated_price'] = short
            return decision
    log.debug(f"{pair_name} - {script_name} received empty analyses array")
    return False


def _minutes_to_seconds(minutes):
    """
    Converts minutes to seconds for use when comparing timeframes with timestamps. Note that unix
    timestamps are created as seconds (IE: divides the timestamp by 1000), hence this function does not return
    milliseconds.

    :param minutes: The amount of minutes to convert to seconds
    :return: Parameter "Minutes" in seconds
    """
    return minutes * 60
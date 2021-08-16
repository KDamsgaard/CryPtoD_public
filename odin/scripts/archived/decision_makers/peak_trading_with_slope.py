
script_name = __name__.split(".")[-1]
arg_fields = [['_analyses', 'purchases'],
              ['_settings']]


def primary_function(pair_name, log, args: list):
    """
    Tracks tension and short SMA, reacting when short SMA moves far enough above or blow tension.
    Buy and sell modifiers can be adjusted to have the algorithm react quicker with lower settings, and vice versa.
    Short SMA and tension can be adjusted to have tension "lag behind" making decisions more likely.

    The algorithm implements slope to stop purchase-actions when market is trending down.


    """

    """
    This algorithm determines to sell if the market trends down and to buy if the market trends up. These determinations
    are made by selecting two fixed points and calculation if the line through them has a positive or negative slope.
    Modifiers are used to restrict decisions so that the algorithm does not keep selling or buying on markets that are
    trending heavily up or down.
    """
    analyses = args[0]
    if analyses:
        settings = args[1]
        threshold = settings['timeframes']['threshold']
        if threshold <= 0:
            log.error(f"{pair_name} - {script_name} received threshold value of 0 or less")
            return False
        else:
            latest_analysis = analyses[-1]
            buy_modifier = settings['modifiers']['buy']
            sell_modifier = settings['modifiers']['sell']

            now = latest_analysis['time']
            decision = {'time': now, 'direction': None, 'estimated_price': None, 'details': {}}

            smas = latest_analysis['smas']
            new_short = smas['short']
            new_long = smas['long']
            new_tension = smas['tension']
            old_tension = None

            for analysis in analyses:
                if analysis['time'] > now - threshold:
                    old_tension = analysis['smas']['tension']
                    break

            if old_tension:
                buy_factor = 1 - (buy_modifier / 100)
                sell_factor = 1 + (sell_modifier / 100)

                if old_tension < new_tension and new_short < new_tension * buy_factor:
                    decision['direction'] = 'b'
                if old_tension > new_tension and new_short > new_tension * sell_factor:
                    decision['direction'] = 's'

            if decision['direction']:
                decision['estimated_price'] = new_short
                return decision
            else:
                return False
    else:
        log.debug(f"{pair_name} - {script_name} received empty analyses array")
        return False


def find_analysis_by_threshold(now, analyses, threshold):
    result = None
    for analysis in analyses:
        if analysis['time'] > now - threshold:
            result = analysis
            break
    return result


# def _minutes_to_seconds(minutes):
#     """
#     Converts minutes to seconds for use when comparing timeframes with timestamps. Note that unix
#     timestamps are created as seconds (IE: divides the timestamp by 1000), hence this function does not return
#     milliseconds.
#
#     :param minutes: The amount of minutes to convert to seconds
#     :return: Parameter "Minutes" in seconds
#     """
#     return minutes * 60
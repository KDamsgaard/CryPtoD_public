
script_name = __name__.split(".")[-1]
arg_fields = [['_analyses', 'purchases']]


def primary_function(pair_name, log, args: list):
    """
    Uses purchase analyses (SMAs).

    If the current short SMA lies within the band defined by the long SMA and tension, a decision is made.

    Theory:
    If three SMAs are calculated based on three different timeframes the corresponding graphs will react differently.
    The shorter the timeframe, the quicker the SMA will react to market changes. This means that if the market values of
    purchases is generally going down the short SMA values will be below the long SMA values which will be below the
    tension values. The opposite is true if market values are going up.

    When the market changes trend (IE: values go from trending down to trending up or vice versa), the SMA values will
    change relative position and because the short SMA reacts fast it will be between long and tension for a period of
    time. During this period the algorithm determines if a sale or purchase should be made depending on whether short
    SMA is above or below long SMA.

    """
    analyses = args[0]
    if analyses:
        analysis = analyses[-1]
        now = analysis['time']
        decision = {'time': now, 'direction': None, 'estimated_price': None}

        if analysis:
            short = analysis['smas']['short']
            long = analysis['smas']['long']
            tension = analysis['smas']['tension']

            if tension < short < long:
                decision['direction'] = 's'
            if tension > short > long:
                decision['direction'] = 'b'

            if decision['direction']:
                decision['estimated_price'] = short
                return decision
    else:
        log.debug(f"{pair_name} - {script_name} received empty analyses array")
        return False

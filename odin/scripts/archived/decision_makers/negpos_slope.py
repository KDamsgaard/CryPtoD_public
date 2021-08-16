import time

script_name = __name__.split(".")[-1]
arg_fields = [['_analyses', 'purchases'],
              ['_settings']]


def primary_function(pair_name, log, args: list):
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
            return f"{pair_name} - {script_name} received threshold value of 0 or less"
        else:
            latest_analysis = analyses[-1]

            now = latest_analysis['time']
            decision = {'time': now, 'direction': None, 'estimated_price': None, 'details': {}}

            new_tension = latest_analysis['smas']['tension']
            old_tension = None

            for analysis in analyses:
                if analysis['time'] > now - threshold:
                    old_tension = analysis['smas']['tension']
                    break

            if old_tension:
                buy_factor = 1 + (settings['modifiers']['buy'] / 100)
                sell_factor = 1 - (settings['modifiers']['sell'] / 100)
                if old_tension < new_tension:
                    decision['direction'] = 'b'
                if old_tension > new_tension:
                    decision['direction'] = 's'
                # if old_tension < new_tension < old_tension * buy_factor:
                #     decision['direction'] = 'b'
                # if old_tension > new_tension > old_tension * sell_factor:
                #     decision['direction'] = 's'

            if decision['direction']:
                decision['estimated_price'] = new_tension
            return decision
    else:
        log.debug(f"{pair_name} - {script_name} received empty trades array")
        return False

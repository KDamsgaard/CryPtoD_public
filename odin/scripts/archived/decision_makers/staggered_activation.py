
script_name = __name__.split(".")[-1]
arg_fields = [['_analyses', 'purchases']]


def primary_function(pair_name, log, args: list):
    """


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

            if short < tension < long:
                decision['direction'] = 's'
            if short > tension > long:
                decision['direction'] = 'b'

            if decision['direction']:
                decision['estimated_price'] = short
                return decision

    return False

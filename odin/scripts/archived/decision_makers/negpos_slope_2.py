import time

script_name = __name__.split(".")[-1]
arg_fields = [['_analyses'],
              ['_settings']]


def primary_function(pair_name, log, args: list):
    """
    This algorithm determines to sell if the market trends down and to buy if the market trends up. These determinations
    are made by selecting three fixed points - if the "middle" point is above or below the other points a trend shift
    has occurred and a decision can be made.
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
            now = latest_analysis['time']
            decision = {'time': now, 'direction': None, 'estimated_price': None, 'details': {}}
            middle_threshold = threshold
            rear_threshold = threshold * 3

            tensions = {"rear": None, "middle": None, "front": latest_analysis['smas']['tension']}

            for analysis in analyses[::-1]:
                if not tensions['middle'] and analysis['time'] < now - middle_threshold:
                    tensions['middle'] = analysis['smas']['tension']
                if analysis['time'] < now - rear_threshold:
                    tensions['rear'] = analysis['smas']['tension']
                    break

            if tensions['rear']:
                if tensions['rear'] > tensions['middle'] and tensions['middle'] < tensions['front']:
                    decision['direction'] = 'b'
                if tensions['rear'] < tensions['middle'] and tensions['middle'] > tensions['front']:
                    decision['direction'] = 's'

            if decision['direction']:
                decision['estimated_price'] = tensions['front']
            return decision
    else:
        log.debug(f"{pair_name} - {script_name} received empty trades array")
        return False

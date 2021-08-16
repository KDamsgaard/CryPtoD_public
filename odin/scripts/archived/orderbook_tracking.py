"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""
import time

from modules.kraken_services.public_kraken_services import PublicKrakenServices

script_name = __name__.split(".")[-1]
arg_fields = [['_trades'],
              ['_analyses'],
              ['_settings', 'fees'],
              ['_settings', 'timeframes']]
triggers = []


def primary_function(pair_name, log, args: list):
    """
    This script attempts to determine whether to buy or sell depending on the high- and low-points of a tension band.

    First the newest tension SMA is calculated.
    Next the highest and lowest tension SMA values within the threshold are determined.
    The live orderbook is loaded from Kraken:
        If an asking price below "low tension" is found the decision is to buy.
        If an asking price above "high tension" is found the decision is to sell.
    """
    trades = args[0]
    analyses = args[1]
    fees = args[2]
    timeframes = args[3]

    now = time.time()

    if trades and timeframes:
        analysis = {'time': now}
        calculations = calculate(trades=trades,
                                 analyses=analyses,
                                 timeframes=timeframes,
                                 now=now)
        if calculations['tension_sma']:
            analysis['calculations'] = calculations
            orderbook = get_cropped_orderbook(pair_name=pair_name)
            decision = make_decision(orderbook=orderbook,
                                     calculations=analysis['calculations'])
            analysis['decision'] = decision
            analysis['orderbook'] = orderbook
            return analysis
        return None
    else:
        log.debug(f"{pair_name} - {script_name} received one or more empty arguments")
        return False


def get_cropped_orderbook(pair_name):
    orderbook = PublicKrakenServices().fetch_orderbook_for_pair(pair_name=pair_name)[pair_name]
    asks = orderbook['asks']
    best_ask = float(asks[0][0])
    bids = orderbook['bids']
    best_bid = float(bids[0][0])
    return {'best_ask': best_ask, 'best_bid': best_bid}


def calculate(trades, timeframes, now, analyses):
    """
    This function determines the relevant factors of the algorithm by calling helper functions (calculate_tension() and
    find_min_max_tension()).
    """
    tension = calculate_tension(trades=trades,
                                timeframes=timeframes,
                                now=now)
    min_max = find_min_max_tension(analyses=analyses,
                                   timeframes=timeframes,
                                   new_tension=tension,
                                   now=now)
    result = {'tension_sma': tension,
              'min_tension': min_max[0],
              'max_tension': min_max[1]}
    return result


def calculate_tension(trades, timeframes, now):
    """
    Calculates the newest tension value by tracking backwards in the list of trades, adding the prices and dividing by
    the amount of trades found within the timeframe.


    :param trades: The list of trades to analyse.
    :param timeframes: The "timeframes" setting object from the database.
    :param now: Unix timestamp - supplied by primary function (variable "now").
    """

    tf_tension = now - minutes_to_seconds(timeframes['tension'])

    total = 0
    count = 0
    for trade in trades[::-1]:
        if trade['time'] < tf_tension:
            break
        total += trade['price']
        count += 1
    return total / count


def find_min_max_tension(analyses, timeframes, new_tension, now):
    """
    Locates the minimum and maximum tension values within the timeframe by tracking backwards in the list of analyses
    and comparing the found values to the currently set minimum/maximum.

    :param analyses: A list of analyses to analyse
    :param timeframes: The "timeframes" setting object from the database.
    :param new_tension: The newest tension value calculated by calculate_tension()
    :param now: Unix timestamp - supplied by primary function (variable "now").
    """
    if new_tension:
        min_tension = new_tension
        max_tension = new_tension

        threshold = now - minutes_to_seconds(timeframes['threshold'])

        cropped_analyses = []
        for analysis in analyses[::-1]:
            if analysis['time'] > threshold:
                cropped_analyses.append(analysis)

        for analysis in cropped_analyses:
            tension_sma = analysis['calculations']['tension_sma']

            if tension_sma:
                if tension_sma < min_tension:
                    min_tension = tension_sma
                if tension_sma > max_tension:
                    max_tension = tension_sma
            else:
                break
        return min_tension, max_tension
    return None, None


def make_decision(orderbook, calculations):
    """
    Determines if a trade should be performed
    """
    decision = {'direction': None, 'estimated_price': None}

    if spread_is_high_enough(min_tension=calculations['min_tension'], max_tension=calculations['max_tension']):
        estimated_ask = orderbook[0]
        estimated_bid = orderbook[1]

        if estimated_ask < calculations['min_tension']:
            decision['direction'] = 'b'
            decision['estimated_price'] = estimated_ask

        if estimated_bid > calculations['max_tension']:
            decision['direction'] = 's'
            decision['estimated_price'] = estimated_bid
    return decision


def spread_is_high_enough(min_tension, max_tension):
    print(f"Tension spread: {round(max_tension / min_tension, 6)}")
    if min_tension and max_tension:
        return max_tension / min_tension > 1.002
    else:
        return False


def minutes_to_seconds(minutes):
    """
    Converts minutes to seconds for use when comparing timeframes with timestamps. Note that unix
    timestamps are created as seconds (IE: divides the timestamp by 1000), hence this function does not return
    milliseconds.

    :param minutes: The amount of minutes to convert to seconds
    :return: Parameter "Minutes" in seconds
    """
    return minutes * 60

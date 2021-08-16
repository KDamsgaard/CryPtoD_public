"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""
script_name = 'test'
analyzer_name = 'test'
arg_fields = []


def primary_function(pair_name, log, args):
    log.info(f"{__name__} was called for {pair_name}")
    fees = {'maker': 0.16, 'taker': 0.26}
    modifiers = {'buy': 0.1, 'sell': 0.1}
    timeframes = {'short': 1, 'long': 2, 'tension': 30}
    settings = {'fees': fees,
                'modifiers': modifiers,
                'scripts': {'analyzer': analyzer_name},
                'timeframes': timeframes}

    return settings

"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Søren B. Ølholm
"""

def primary_function(pair_name, log, args):
    # The maximum value of short/threshold
    maximum = args['maximum']
    minimum = args['minimum']
    finished = False
    short = minimum
    threshold = minimum

    if args['settings']:
        short = args['settings']['short']
        threshold = args['settings']['threshold']

        if threshold < short == maximum:
            threshold += minimum
            short = minimum

        if short < maximum:
            short += minimum

    if short == maximum and threshold == maximum:
        finished = True

    return {'short': round(short, 2), 'threshold': round(threshold, 2), 'finished': finished}

args = {'settings': None, 'minimum': 0.5, 'maximum': 3}
for i in range(1000000):
    args['settings'] = primary_function(None, None, args)
    print(i, args['settings'])
    if args['settings']['finished']:
        print('Maximum settings reached!')
        print('Finished...')
        break

def primary_function(pair_name, log, args):
    minimum = 0
    increment = 0.1

    if not args:
        args = {'timeframes': {'short': 0, 'long': 0}, 'modifiers': {'buy': 0, 'sell': 0}}

    if args['timeframes']['long'] < args['modifiers']['buy']:
        args['timeframes']['long'] += increment
    else:
        args['timeframes']['long'] = minimum
        args['modifiers']['buy'] += increment

    if args['timeframes']['short'] < args['modifiers']['sell'] < args['timeframes']['long'] < args['modifiers']['buy']:
        args['timeframes']['short'] += increment
    elif args['modifiers']['sell'] < args['timeframes']['long'] < args['modifiers']['buy']:
        args['timeframes']['short'] = minimum
        args['modifiers']['sell'] += increment

    args = {'timeframes':
                {'short': round(args['timeframes']['short'], 2),
                 'long': round(args['timeframes']['long'], 2)},
            'modifiers':
                {'buy': round(args['modifiers']['buy'], 2),
                 'sell': round(args['modifiers']['sell'], 2)}}

    return args


iterrations = 500
args = None
for i in range(0, iterrations):
    args = primary_function(None, None, args)

    print(args)
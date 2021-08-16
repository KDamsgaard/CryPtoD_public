from datetime import datetime

class GraphDataCompilerService:
    def __init__(self, result):
        self._result = result
        self._name = self._get_compiled_name(result)
        self._graph_data = {'compiled_name': self._name,
                            'labels': [],
                            'trades': {'purchases': [], 'sales': []},
                            'decisions': {'purchases': [], 'sales': []},
                            'actions': {'purchases': [], 'sales': []}
                            }

        self._compile_labels()
        self._compile_trades()
        self._compile_decisions()
        self._compile_actions()

    def _get_compiled_name(self, result):
        _time = result['time']
        dt = self._convert_timestamp(result['time'], True)
        dataset = result['dataset_name']
        script = result['scripts']['analyzer']
        return f'{_time}-{dt}_{dataset}_{script}'

    def _convert_timestamp(self, ts, dirname=False):
        if not dirname:
            return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return datetime.utcfromtimestamp(ts).strftime('%Y%m%d%H-%M-%S')

    def _compile_labels(self):
        last_ts = None
        for trade in self._result['trades']:
            if not last_ts:
                self._graph_data['labels'].append(self._convert_timestamp(trade['time']))
            elif last_ts < trade['time']:
                self._graph_data['labels'].append(self._convert_timestamp(trade['time']))

    def _compile_trades(self):
        for trade in self._result['trades']:
            if trade['direction'] == 'b':
                plot = {'x': self._convert_timestamp(trade['time']), 'y': trade['price']}
                self._graph_data['trades']['purchases'].append(plot)
            if trade['direction'] == 's':
                plot = {'x': self._convert_timestamp(trade['time']), 'y': trade['price']}
                self._graph_data['trades']['sales'].append(plot)

    def _compile_decisions(self):
        for analyses in self._result['analyses']:
            if analyses['decision']['estimated_price']:
                if analyses['decision']['direction'] == 'b':
                    plot = {'x': self._convert_timestamp(analyses['time']), 'y': analyses['decision']['estimated_price']}
                    self._graph_data['decisions']['purchases'].append(plot)
                if analyses['decision']['direction'] == 's':
                    plot = {'x': self._convert_timestamp(analyses['time']), 'y': analyses['decision']['estimated_price']}
                    self._graph_data['decisions']['sales'].append(plot)

    def _compile_actions(self):
        for action in self._result['actions']:
            if action['direction'] == 'b':
                plot = {'x': self._convert_timestamp(action['time']), 'y': action['price']}
                self._graph_data['actions']['purchases'].append(plot)
            if action['direction'] == 's':
                plot = {'x': self._convert_timestamp(action['time']), 'y': action['price']}
                self._graph_data['actions']['sales'].append(plot)

    @property
    def graph_data(self):
        return self._graph_data
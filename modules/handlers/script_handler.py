import importlib
import logging


class ScriptHandler:
    def __init__(self, caller):
        self._log = logging.getLogger(self.__class__.__name__)
        self._caller = caller

    def load_script(self, script_type, script_name):
        """
        Loads a script based on type and name.

        :param script_type: The type of script to load (essentially which folder to look in).
        :param script_name: The name of the script to load
        :return: Tuple (the names of the fields which the scripts needs and the script's primary function object)
        """
        path = "scripts." + script_type + "s." + script_name
        try:
            script = importlib.import_module(path)

            script_name = getattr(script, 'script_name')
            arg_fields = getattr(script, 'arg_fields')
            function = getattr(script, 'primary_function')
            factors = getattr(script, 'factors')

            return {'script_name': script_name,
                    'arg_fields': arg_fields,
                    'primary_function': function,
                    'factors': factors}

        except ModuleNotFoundError:
            self._log.error(f"Script \"{script_name}\" was not found")
        except AttributeError:
            self._log.error(f"Attempted to load field for {script_name} which contains no such field.")

        return False

    def load_args(self, arg_fields):
        """
        Returns the PairWatcher variables which a script needs to execute properly.

        :param arg_fields: The names of the fields to load.
        :return: The actual variables contained in the PairWatcher which correspond to a loaded script's needs.
        """
        args = []
        for field in arg_fields:
            arg = getattr(self._caller, field[0])
            if len(field) > 1:
                for i, component in enumerate(field):
                    if i > 0:
                        arg = arg[component]
            args.append(arg)
        return args

    def run_script(self, function, args):
        """
        Runs the function loaded by the class and returns the resulting return values of the script
        """
        return function(pair_name=self._caller.pair_name, log=self._log, args=args)

    @property
    def caller(self):
        return self._caller

    @property
    def script(self):
        return self._script

    @property
    def args(self):
        return self._args

    @property
    def factors(self):
        return self._script['factors']

    @property
    def result(self):
        return self._result

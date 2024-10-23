"""Default parameter values, and object for holding parameters.
"""


default_parameters = {
    'transmission_rate': 1.0,
    'recovery_rate': 0.5,
    'waning_rate': 0.1,
    'proportion_symptomatic': 0.25,
}


class ModelParameters:
    """Parameters for Model.
    """
    def __getattr__(self, name):

        if name in default_parameters:
            return default_parameters[name]

        raise AttributeError('{} parameter not found'.format(name))

    def __init__(self):
        pass

    def _set_parameter(self, name, value):
        setattr(self, name, value)

    def set_parameters(self, param_dict):
        """Set parameters from dictionary.

        Parameters
        ----------
        param_dict : dict
            {'parameter_name': parameter_value} of each parameter
        """
        for k, v in param_dict.items():
            self._set_parameter(k, v)

    def remove_parameter(self, name):
        """Remove a parameter.

        Parameters
        ----------
        name : str
            Name of parameter to be removed
        """
        delattr(self, name)

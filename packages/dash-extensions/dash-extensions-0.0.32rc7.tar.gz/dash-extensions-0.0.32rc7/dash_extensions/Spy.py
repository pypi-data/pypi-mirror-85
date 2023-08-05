# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Spy(Component):
    """A Spy component.
The Sync component makes it possible to synchronize states between components.

Keyword arguments:
- children (list of a list of or a singular dash component, string or numbers; optional): The children of this component.
- links (dict; optional): The ID used to identify this component in Dash callbacks. links has the following type: list of list of dicts containing keys 'id', 'prop'.
Those keys have the following types:
  - id (string; required)
  - prop (boolean | number | string | dict | list; required)s
- id (string; optional): The ID used to identify this component in Dash callbacks."""
    @_explicitize_args
    def __init__(self, children=None, links=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'links', 'id']
        self._type = 'Spy'
        self._namespace = 'dash_extensions'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'links', 'id']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Spy, self).__init__(children=children, **args)

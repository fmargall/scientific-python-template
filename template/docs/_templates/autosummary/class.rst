{#- Page of a class, for the autosummary directive of api.md: its public methods -#}
{#- and attributes are documented on the same page                              -#}
{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:
   :show-inheritance:

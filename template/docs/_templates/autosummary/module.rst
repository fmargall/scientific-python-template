{#- Page of a module, for the autosummary directive of api.md. Unlike the default -#}
{#- template, it gives a page to each member and to each submodule, so that     -#}
{#- :recursive: documents the whole package                                     -#}
{{ fullname | escape | underline }}

.. automodule:: {{ fullname }}

{% block functions %}
{%- if functions %}
.. rubric:: Functions

.. autosummary::
   :toctree:
{% for item in functions %}
   {{ item }}
{%- endfor %}
{% endif %}
{%- endblock %}

{% block classes %}
{%- if classes %}
.. rubric:: Classes

.. autosummary::
   :toctree:
{% for item in classes %}
   {{ item }}
{%- endfor %}
{% endif %}
{%- endblock %}

{% block exceptions %}
{%- if exceptions %}
.. rubric:: Exceptions

.. autosummary::
   :toctree:
{% for item in exceptions %}
   {{ item }}
{%- endfor %}
{% endif %}
{%- endblock %}

{% block modules %}
{%- if modules %}
.. rubric:: Modules

.. autosummary::
   :toctree:
   :recursive:
{% for item in modules %}
   {{ item }}
{%- endfor %}
{% endif %}
{%- endblock %}

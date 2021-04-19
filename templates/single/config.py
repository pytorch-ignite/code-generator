{% extends "_argparse.py" %}
{% block get_default_parser %}
UPDATES = {
    # training options
    "max_epochs": {
        "default": {{max_epochs}},
        "type": int,
        "help": "max_epochs of ignite.Engine.run() for training. Default: %(default)s",
    }
}

DEFAULTS.update(UPDATES)

{{ super() }}
{% endblock %}

{% block imports %}
from torchvision import models

{% endblock %}

{% block get_model %}
def get_model(name):
    if name in models.__dict__:
        fn = models.__dict__[name]
    else:
        raise RuntimeError(f"Unknown model name {name}")

    return fn(num_classes=10)
{% endblock %}

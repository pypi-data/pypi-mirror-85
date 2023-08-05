# X-Net Django Color Field

A color field for Django models and forms.

# Installation

1. `pip install x_net_django_color_field`
2. Add `x_net_django_color_field` to INSTALLED_APPS

## Usage

Consider the following model using a `ColorField`

```python
from django.db import models
from x_net_django_color_field.models import ColorField

class CustomModel(models.Model):
    color = ColorField(verbose_name="Color")
```

Consider the following form using a `ColorField`

```python
from django.forms import forms
from x_net_django_color_field.forms import ColorField

class CustomForm(forms.Form):
    color = ColorField(label="Color")
```

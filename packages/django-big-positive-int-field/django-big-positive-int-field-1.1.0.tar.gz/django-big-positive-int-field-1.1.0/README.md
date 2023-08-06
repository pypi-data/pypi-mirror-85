# Big Positive Integer Field
`django-big-positive-int-field` contains a generic model field for storing a big positive integer something like factorial of a number in python

## Intsallation 
```pip install django-big-positive-int-field```

## Usage
To add `BigPositiveIntegerField` field in your model use following:
```
from big_positive_int_field import BigPositiveIntegerField

from django.db import models

class MyModel(models.Model):
    ...
    big_int_field = BigPositiveIntegerField(default=0)
    ...
```

import os

import django
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models.query_utils import DeferredAttribute
from django.test import SimpleTestCase
from django.utils.module_loading import import_string
from sphinx.application import Sphinx

import sphinxcontrib_django2
from sphinxcontrib_django2 import docstrings


class User2(models.Model):
    pass


class SimpleModel(models.Model):
    user = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    user2 = models.ForeignKey("User2", related_name="+", on_delete=models.CASCADE)
    user3 = models.ForeignKey("auth.User", related_name="+", on_delete=models.CASCADE)
    dummy_field = models.CharField(max_length=3)


class SimpleForm(forms.ModelForm):
    test1 = forms.CharField(label="Test1")
    test2 = forms.CharField()

    class Meta:
        model = SimpleModel
        fields = ("user", "user2", "user3")


class TestDocStrings(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestDocStrings, cls).setUpClass()
        root = os.path.dirname(sphinxcontrib_django2.__file__)
        confdir = os.path.join(os.path.dirname(__file__), "testdocs")
        cls.app = Sphinx(
            srcdir=root,
            confdir=confdir,
            outdir=os.path.join(confdir, "_build"),
            doctreedir=root,
            buildername="html",
            freshenv=True,
        )
        sphinxcontrib_django2.setup(cls.app)

    def test_foreignkey_type(self):
        """Test how the foreignkeys are rendered."""
        self.assertEqual(
            docstrings._get_field_type(SimpleModel._meta.get_field("user")),
            ":type user: ForeignKey to :class:`~django.contrib.auth.models.User`",
        )
        self.assertEqual(
            docstrings._get_field_type(SimpleModel._meta.get_field("user2")),
            ":type user2: ForeignKey to"
            " :class:`~sphinxcontrib_django2.tests.test_docstrings.User2`",
        )
        self.assertEqual(
            docstrings._get_field_type(SimpleModel._meta.get_field("user3")),
            ":type user3: ForeignKey to :class:`~django.contrib.auth.models.User`",
        )

    def test_model_init_params(self):
        """Model __init__ gets all fields as params."""
        lines = []
        simple_model_path = "{}.{}".format(SimpleModel.__module__, SimpleModel.__name__)
        docstrings.improve_model_docstring(
            self.app, "class", simple_model_path, SimpleModel, {}, lines
        )
        self.assertEqual(
            lines,
            [
                ":param id: Id",
                ":type id: AutoField",
                ":param user: User",
                ":type user: ForeignKey to :class:`~django.contrib.auth.models.User`",
                ":param user2: User2",
                ":type user2: ForeignKey to"
                " :class:`~sphinxcontrib_django2.tests.test_docstrings.User2`",
                ":param user3: User3",
                ":type user3: ForeignKey to :class:`~django.contrib.auth.models.User`",
                ":param dummy_field: Dummy field",
                ":type dummy_field: CharField",
            ],
        )

    def test_add_form_fields(self):
        """Form fields should be mentioned."""
        lines = []
        simple_form_path = "{}.{}".format(SimpleForm.__module__, SimpleForm.__name__)
        docstrings.improve_model_docstring(
            self.app, "class", simple_form_path, SimpleForm, {}, lines
        )
        self.assertEqual(
            lines,
            [
                "**Form fields:**",
                "",
                "* ``user``: User (:class:`~django.forms.models.ModelChoiceField`)",
                "* ``user2``: User2 (:class:`~django.forms.models.ModelChoiceField`)",
                "* ``user3``: User3 (:class:`~django.forms.models.ModelChoiceField`)",
                "* ``test1``: Test1 (:class:`~django.forms.fields.CharField`)",
                "* ``test2``: Test2 (:class:`~django.forms.fields.CharField`)",
            ],
        )

    def test_model_fields(self):
        lines = []
        simple_model_path = "{}.{}".format(SimpleModel.__module__, SimpleModel.__name__)
        if django.VERSION < (2, 1):
            obj = DeferredAttribute(field_name="dummy_field", model=simple_model_path)
        elif django.VERSION < (3, 0):
            obj = DeferredAttribute(field_name="dummy_field")
        else:
            model = import_string(simple_model_path)
            obj = DeferredAttribute(field=model._meta.get_field("dummy_field"))

        docstrings.improve_model_docstring(
            self.app,
            "attribute",
            "{}.dummy_field".format(simple_model_path),
            obj,
            {},
            lines,
        )
        self.assertEqual(
            lines,
            [
                "**Model field:** dummy field",
            ],
        )

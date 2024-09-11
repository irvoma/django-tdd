from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item


EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

class ItemForm(forms.models.ModelForm):
    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

    class Meta:
        model = Item
        fields = ('text', )
        widgets= {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg'
            })
        }
        error_messages = {
            'text': {
                'required': EMPTY_ITEM_ERROR,
            }
        }


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def save(self):
        """ call the original method (the parent's parent save method """
        # NOTE: Since both forms to call the save parent's parent method works, the author
        #  prefers to use the second (the uncommented one), since he likes it the most.
        # return super(ItemForm, self).save()
        return forms.models.ModelForm.save(self)

    def validate_unique(self):
        """ The book suggests to use validate_unique function, but unique together is
            defined using constraints Meta class option, and the defined constraints are
            validated through the validate_constraints function in the model
            Further info at https://docs.djangoproject.com/en/4.2/ref/models/instances/#django.db.models.Model.validate_unique
        """
        # NOTE: the unique together constraint is defined using the constraints Model Meta option,
        #  since Django recommends to use it instead of the unique_together option, but this method
        #  is not called elsewhere in the code of the form. By now I cannot currently find it.
        try:
            self.instance.validate_unique()
            self.instance.validate_constraints()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

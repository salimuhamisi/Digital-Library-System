from django import forms

class BorrowForm(forms.Form):
    borrowing_date = forms.DateField(label='Borrowing Date')
    returning_date = forms.DateField(label='Returning Date')
    book_id = forms.IntegerField(widget=forms.HiddenInput())
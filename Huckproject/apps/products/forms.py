from django import forms

class ProductFilterForm(forms.Form):
    GRADE_CHOICES = [(0, '全学年')] + [(i, f'{i}年') for i in range(1, 5)]
    FACULTY_CHOICES = [
        ('', '全学部'),
        ('法学部', '法学部'),
        ('経済学部', '経済学部'),
        ('経営学部', '経営学部'),
        ('外国語学部', '外国語学部'),
        ('人間学部', '人間学部'),
        ('都市情報学部', '都市情報学部'),
        ('情報工学部', '情報工学部'),
        ('理工学部', '理工学部'),
        ('農学部', '農学部'),
        ('薬学部', '薬学部'),
    ]

    grade = forms.ChoiceField(choices=GRADE_CHOICES, required=False)
    faculty = forms.ChoiceField(choices=FACULTY_CHOICES, required=False)
    department = forms.CharField(required=False)
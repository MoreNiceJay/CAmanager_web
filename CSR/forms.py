from django import forms
from .models import CSR


class CSRForm(forms.ModelForm): # 모델 폼 정의
	class Meta:
		model = CSR
		fields = ['organization','organization_unit','country', 'state', 'locality',
        'common_name','algorithm','domain',]
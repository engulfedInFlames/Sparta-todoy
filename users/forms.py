from django import forms

from .models import CustomUser


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label="비밀번호",
        required=True,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="비밀번호 확인",
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "password1",
            "password2",
            "nickname",
            "gender",
            "age",
            "introduction",
        )
        labels = {
            "email": "이메일 주소",
            "nickname": "닉네임",
            "address": "주소",
            "gender": "성별",
            "age": "나이",
            "introdution": "자기소개",
        }
        widgets = {
            "email": forms.EmailInput(),
            "gender": forms.Select(),
            # attrs={"class": "form-control"}
        }
        error_messages = {}

    field_order = [
        "email",
        "password1",
        "password2",
        "nickname",
        "gender",
        "age",
        "introduction",
    ]

    # ↓ clean 함수는 form이 submit 됐을 때 각 field가 가진 validator를 사용하여 입력값이 유효한지 확인
    # 비밀번호 일치 여부를 확인하는 과정을 추가하기 위해 오버라이팅

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        try:
            if password1 != password2:
                raise forms.ValidationError(
                    {
                        "password2": ["비밀번호가 일치하지 않습니다"],
                    }
                )
        except forms.ValidationError as e:
            print(f"Password Validation Error\n: {e}")

        return cleaned_data


class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = {
            "email",
            "password",
        }
        labels = {
            "email": "이메일 주소",
            "password": "비밀번호",
        }
        widgets = {
            "email": forms.EmailInput(),
            "password": forms.PasswordInput(),
        }

    field_order = [
        "email",
        "password",
    ]

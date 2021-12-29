from django import forms
from quiz.models import *
from practical.models import *
from user.models import *
from video.models import *
from sign.models import *
from rest_framework import serializers


class ElectronicalJournal(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel()
        fields = '__all__'


class CarForm(forms.ModelForm):
    class Meta:
        model = Car()
        fields = '__all__'


class PracticalForm(forms.ModelForm):
    class Meta:
        model = Practical()
        fields = '__all__'


class DayOfWeekForm(forms.ModelForm):
    class Meta:
        model = DayOfWeek()
        fields = '__all__'


class PaymentForPracticalForm(forms.ModelForm):
    class Meta:
        model = PaymentForPractical()
        fields = '__all__'


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer()
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question()
        fields = '__all__'


class BiletForm(forms.ModelForm):
    class Meta:
        model = Bilet()
        fields = '__all__'


class SavolForm(forms.ModelForm):
    class Meta:
        model = Savol()
        fields = '__all__'


class JavobForm(forms.ModelForm):
    class Meta:
        model = Javob()
        fields = '__all__'


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result()
        fields = '__all__'


class ResultQuizForm(forms.ModelForm):
    class Meta:
        model = ResultQuiz()
        fields = '__all__'


class AttemptForm(forms.ModelForm):
    class Meta:
        model = Attempt()
        fields = ['allowed', 'solved', 'user']


class ResultJavobForm(forms.ModelForm):
    class Meta:
        model = ResultJavob()
        fields = '__all__'


class CheckTestColorForm(forms.ModelForm):
    class Meta:
        model = CheckTestColor()
        fields = '__all__'


class SignCategoryForm(forms.ModelForm):
    class Meta:
        model = SignCategory()
        fields = '__all__'


class SignForm(forms.ModelForm):
    class Meta:
        model = Sign()
        fields = '__all__'


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject()
        fields = '__all__'


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme()
        fields = '__all__'


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule()
        fields = '__all__'


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material()
        fields = '__all__'


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region()
        fields = '__all__'


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District()
        fields = '__all__'


class EducationCategoryForm(forms.ModelForm):
    class Meta:
        model = EducationCategory()
        fields = '__all__'


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group()
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = ['name', 'initsatial', 'role', 'school', 'email', 'birthday', 'username','password']
        fields = '__all__'


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['title', 'director', 'phone', 'bank', 'region', 'district']


class SignUpSchoolForm(forms.ModelForm):
    class Meta:
        model = SignUpSchool()
        fields = '__all__'


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact()
        fields = '__all__'


class FileForm(forms.ModelForm):
    class Meta:
        model = File()
        fields = '__all__'


class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referral()
        exclude = ('created_at',)


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance()
        fields = '__all__'


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating()
        fields = '__all__'


class SmsForm(forms.ModelForm):
    class Meta:
        model = Sms()
        fields = '__all__'


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment()
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category()
        fields = '__all__'


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video()
        fields = '__all__'


class ViewCompleteForm(forms.ModelForm):
    class Meta:
        model = ViewComplete()
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment()
        fields = '__all__'


class FilesForm(forms.ModelForm):
    class Meta:
        model = Files()
        fields = '__all__'


class NaborForm(forms.ModelForm):
    class Meta:
        model = Nabor()
        fields = '__all__'


class PayForm(forms.ModelForm):
    class Meta:
        model = Pay()
        fields = '__all__'


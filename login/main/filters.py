import django_filters
from main.models import Courses

class CourseFilter(django_filters.Filter):
    class Meta:
        model = Courses
        fields = '__all__'
from django.db import models
from apps.classes.models import EN_Classes
from apps.organization.models import EN_Organization

class EN_ClassTimings(models.Model):

    organization = models.ForeignKey(EN_Organization, null=False, on_delete=models.CASCADE)
    class_fk = models.ForeignKey(EN_Classes, null=False, on_delete=models.CASCADE)
    timing_name = models.CharField(max_length=100,null=False)

    is_timing_for_sunday = models.BooleanField(null=False, default=False)
    is_timing_for_monday = models.BooleanField(null=False, default=True)
    is_timing_for_tuesday = models.BooleanField(null=False, default=True)
    is_timing_for_wednesday = models.BooleanField(null=False, default=True)
    is_timing_for_thursday = models.BooleanField(null=False, default=True)
    is_timing_for_friday = models.BooleanField(null=False, default=True)
    is_timing_for_saturday = models.BooleanField(null=False, default=False)

    class_starting_time = models.TimeField(null=False)
    class_ending_time = models.TimeField(null=False)

    class Meta:
        db_table = "en_class_timings"
        unique_together = ('organization', 'class_fk', 'timing_name')


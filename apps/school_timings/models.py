from django.db import models
from apps.organization.models import EN_Organization

class EN_SchoolTimings(models.Model):

    organization = models.ForeignKey(EN_Organization, null=False, on_delete=models.CASCADE)
    timing_name = models.CharField(max_length=150,null=False)

    school_starting_time = models.TimeField(null=False)
    school_closing_time = models.TimeField(null=False)

    class_off_on_sunday = models.BooleanField(null=False, default=False)
    class_off_on_monday = models.BooleanField(null=False, default=True)
    class_off_on_tuesday = models.BooleanField(null=False, default=True)
    class_off_on_wednesday = models.BooleanField(null=False, default=True)
    class_off_on_thursday = models.BooleanField(null=False, default=True)
    class_off_on_friday = models.BooleanField(null=False, default=True)
    class_off_on_saturday = models.BooleanField(null=False, default=False)

    assembly_on_sunday = models.BooleanField(null=False, default=False)
    assembly_on_monday = models.BooleanField(null=False, default=False)
    assembly_on_tuesday = models.BooleanField(null=False, default=False)
    assembly_on_wednesday = models.BooleanField(null=False, default=False)
    assembly_on_thursday = models.BooleanField(null=False, default=False)
    assembly_on_friday = models.BooleanField(null=False, default=False)
    assembly_on_saturday = models.BooleanField(null=False, default=False)
    assembly_duration = models.IntegerField(null=True)

    class Meta:
        db_table = "en_school_timings"
        unique_together = ('organization', 'timing_name')


class EN_SchoolTimingBreakup(models.Model):

    timing = models.ForeignKey(EN_SchoolTimings, null=False, on_delete=models.CASCADE)
    is_break = models.BooleanField(null=False)
    is_period = models.BooleanField(null=False)
    duration = models.IntegerField(null=False)
    description = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "en_school_timing_breakup"

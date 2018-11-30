from django.db import models
from apps.organization.models import EN_Organization

class EN_SchoolTimings(models.Model):

    organization = models.ForeignKey(EN_Organization, null=False, on_delete=models.CASCADE)
    timing_name = models.CharField(max_length=150,null=False)

    #Mandatory
    school_starting_time = models.TimeField(null=False)
    school_closing_time = models.TimeField(null=False)

    # Put null if not applicable
    breakfast_starting_time = models.TimeField(null=True)
    breakfast_ending_time = models.TimeField(null=True)

    # Put null if not applicable
    lunch_starting_time = models.TimeField(null=True)
    lunch_ending_time = models.TimeField(null=True)

    # Put null if not applicable
    dinner_starting_time = models.TimeField(null=True)
    dinner_ending_time = models.TimeField(null=True)

    # Mandatory
    no_of_periods = models.IntegerField(null=False)

    # Put null if not applicable
    first_interval_starting_time = models.TimeField(null=True)
    first_interval_ending_time = models.TimeField(null=True)

    # Put null if not applicable
    second_interval_starting_time = models.TimeField(null=True)
    second_interval_ending_time = models.TimeField(null=True)

    # Put null if not applicable
    third_interval_starting_time = models.TimeField(null=True)
    third_interval_ending_time = models.TimeField(null=True)

    # Put null if not applicable
    fourth_interval_starting_time = models.TimeField(null=True)
    fourth_interval_ending_time = models.TimeField(null=True)

    # mandatory : LIST --> [monday,tuesday,wednesday,thursday,friday] or [] -> No Assembly
    assembly_on_days = models.CharField(max_length=60, null=False, default="[]")
    assembly_starting_time = models.TimeField(null=True)
    assembly_ending_time = models.TimeField(null=True)

    #mandatory : LIST --> [saturday,sunday]
    off_days = models.CharField(max_length=30, null=False, default="[]")

    class Meta:
        db_table = "en_school_timings"
        unique_together = ('organization', 'timing_name')

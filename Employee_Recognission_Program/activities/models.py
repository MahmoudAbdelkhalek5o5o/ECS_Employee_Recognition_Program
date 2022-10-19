from django.db import models
from Users.models import User, Role
from enum import Enum

# Create your models here.



class ActivityCategory(models.Model):
    category_name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    description =  models.CharField(max_length=255,null=False, blank= False, default="")
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True , null = True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="category_owner")
    budget = models.IntegerField(null = False, blank = False)
    budget_compare = models.IntegerField(null = False, blank = False)


class CategoryArchive(models.Model):
    category_name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    description =  models.CharField(max_length=255,null=False, blank= False, default = "")
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True , null = True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="archivedcategory_owner")
    budget = models.IntegerField(null = False, blank = False)
    budget_compare = models.IntegerField(null = False, blank = False)
    archive_date = models.DateTimeField(auto_now_add=True,editable=False)
    archived_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="archived_by")




class Activity(models.Model):
    activity_name = models.CharField(max_length=30,null=False, blank= False, unique=True)
    activity_description = models.CharField(max_length=1024,null=False, blank= True)
    category = models.ForeignKey(ActivityCategory,on_delete=models.CASCADE,null=False)
    points = models.IntegerField(null = False, blank = False)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    evidence_needed =  models.CharField(max_length=1024,null=False, blank= False)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True,null=True)
    is_approved = models.BooleanField(null=False,blank = False , default=False)


class ActivityRequest(models.Model):
    STATUS = [
        ("PENDING" , "Pending"),
        ("ACCEPTED" , "Accpeted"),
        ("REJECTED" , "Rejected"),
        ("WITHDRAWN" , "Withdrawn"),

              
    ]
    emp = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name="original_uploader")
    submission_date = models.DateTimeField(auto_now_add=True)
    date_of_action = models.DateTimeField(null = False)
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE,  null=False, db_constraint= True)
    activity = models.ForeignKey(Activity, on_delete = models.CASCADE,  null=True, db_constraint= True)
    status = models.CharField(max_length=10, null = False , blank = False, choices=STATUS, default=STATUS[0])
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True, related_name="approver_of_upload")
    evidence_needed = models.CharField(max_length=1024,null=False, blank= False, default="Provide evidence please")
    proof_of_action = models.FileField(upload_to = "proofs/",null=False, blank= False)
    activity_approval_date = models.DateTimeField(auto_now_add=False, auto_now=False, null = True, blank = False)

class OldActivityRequest(models.Model):
    STATUS = [
        ("PENDING" , "Pending"),
        ("ACCEPTED" , "Accpeted"),
        ("REJECTED" , "Rejected"),
        ("WITHDRAWN" , "Withdrawn"),

              
    ]
    emp = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name="submitter")
    submission_date = models.DateTimeField()
    date_of_action = models.DateTimeField(null = False)
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE,  null=False, db_constraint= True)
    activity = models.ForeignKey(Activity, on_delete = models.CASCADE,  null=True, db_constraint= True)
    status = models.CharField(max_length=10, null = False , blank = False, choices=STATUS)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE , null = True, related_name="approver")
    evidence_needed = models.CharField(max_length=1024,null=False, blank = False, default="Provide evidence please")
    proof_of_action = models.FileField(upload_to = "proofs/",null=False, blank = False)
    activity_approval_date = models.DateTimeField(auto_now_add=False, auto_now=False, null = True, blank = False)
    update_date = models.DateTimeField(auto_now_add=True,editable=False)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="update_activityrequest_by")
    updated_approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="update_approved_by")


    
    
class ActivitySuggestion(models.Model):
    activity_name = models.CharField(max_length=30 , null = False, blank=False)
    category = models.ForeignKey(ActivityCategory , on_delete=models.CASCADE , null=False)
    activity_description = models.CharField(max_length=1024 , null = False, blank=False)
    justification = models.CharField(max_length=30 , null = True, blank=True)
    evidence_needed = models.CharField(max_length=1024 , null = True, blank=True)
    is_archived = models.BooleanField(null=False , default = False)
    
class Points(models.Model):
    points = models.IntegerField(null = False, blank = False)
    amounts = models.IntegerField(null = False, blank = False)
    start_date = models.DateTimeField(auto_now_add=True,editable=False)
    end_date = models.DateTimeField(editable=False)
    employee = models.ForeignKey(User , on_delete=models.CASCADE,null=True , related_name="earned_to")
    is_used = models.BooleanField(null=False,blank = False , default=False)
    



class ActivityArchive(models.Model):
    id = models.IntegerField(null = False, blank = False , primary_key = True)
    activity_name = models.CharField(max_length=30,null=False, blank= False, unique=True)
    activity_description = models.CharField(max_length=1024,null=False, blank= True)
    category = models.ForeignKey(ActivityCategory,on_delete=models.CASCADE,null=False)
    points = models.IntegerField(null = False, blank = False)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    evidence_needed =  models.CharField(max_length=1024,null=False, blank= False)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    archived_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="archive_activity_by")
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True,null=True)
    is_approved = models.BooleanField(null=False,blank = False , default=False)
    archive_date = models.DateTimeField(auto_now_add=True,editable=False)

class ActivityRestorationRequest(models.Model):
    STATUS = [
        ("PENDING" , "Pending"),
        ("ACCEPTED" , "Accpeted"),
        ("REJECTED" , "Rejected"),
        ("WITHDRAWN" , "Withdrawn"),

              
    ]
    id = models.IntegerField(null = False, blank = False , primary_key = True)
    activity_name = models.CharField(max_length=30,null=False, blank= False, unique=True)
    activity_description = models.CharField(max_length=1024,null=False, blank= True)
    category = models.ForeignKey(ActivityCategory,on_delete=models.CASCADE,null=False)
    points = models.IntegerField(null = False, blank = False)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    evidence_needed =  models.CharField(max_length=1024,null=False, blank= False)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    archived_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="archived_activity_by")
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True,null=True)
    is_approved = models.BooleanField(null=False,blank = False , default=False)
    archive_date = models.DateTimeField(auto_now_add=True,editable=False)
    status = models.CharField(max_length=10, null = False , blank = False, choices=STATUS, default=STATUS[0])
 




class OldDataActivities(models.Model):
    original_activity = models.ForeignKey(Activity, on_delete=models.CASCADE,null=True )
    activity_name = models.CharField(max_length=30,null=False, blank= False, unique=True)
    activity_description = models.CharField(max_length=1024,null=False, blank= True)
    category = models.ForeignKey(ActivityCategory,on_delete=models.CASCADE,null=False)
    points = models.IntegerField(null = False, blank = False)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    evidence_needed =  models.CharField(max_length=1024,null=False, blank= False)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    approve_update_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="approve_update_activity_by")
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True,null=True)
    is_approved = models.BooleanField(null=False,blank = False , default=False)
    update_date = models.DateTimeField(auto_now_add=True,editable=False)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="update_activity_by")


class OldDataActivitySuggestion(models.Model):
    original_activity_suggestion = models.ForeignKey(ActivitySuggestion, on_delete=models.CASCADE,null=True )
    activity_name = models.CharField(max_length=30 , null = False, blank=False)
    category = models.ForeignKey(ActivityCategory , on_delete=models.CASCADE , null=False )
    activity_description = models.CharField(max_length=1024 , null = False, blank=False)
    justification = models.CharField(max_length=30 , null = True, blank=True)
    evidence_needed = models.CharField(max_length=1024 , null = True, blank=True)
    update_date = models.DateTimeField(auto_now_add=True,editable=False)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="update_categorySuggestion_by")



class OldDataCategory(models.Model):
    original_category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE,null=False)
    category_name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    description =  models.CharField(max_length=255,null=False, blank= False, default="")
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True , null = True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    budget = models.IntegerField(null = False, blank = False)
    budget_compare = models.IntegerField(null = False, blank = False)
    update_date = models.DateTimeField(auto_now_add=True,editable=False)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE , null=True , related_name="update_category_by")

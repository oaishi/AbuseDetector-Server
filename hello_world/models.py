from django.db import models
from django.db.models import *

# Create your models here.


class Users(models.Model):
    user_name = CharField(max_length=100, unique=True, null=False)
    # user_name = CharField(max_length=100, unique=True, NullBooleanField=False)
    email_address = CharField(max_length=100, unique=True, null=False)
    first_name = CharField(max_length=50, null=False)
    last_name = CharField(max_length=50, null=False)
    password = CharField(max_length=50, null=False)
    accound_status = CharField(max_length=10, default='Active', null=False)
    phone_number = CharField(max_length=20)
    country = CharField(max_length=30, default='Bangladesh', null=False)
    gender = CharField(max_length=10,choices=[('male','male'),('female','female')], null=False)


class Observable_Account(models.Model):
    user_id = ForeignKey(Users, on_delete=models.CASCADE)
    user_name_in_this_account = CharField(max_length=30)
    account_type_of_this_account = CharField(max_length=30)
    email_address_of_this_account= CharField(max_length=30)


class Offender(models.Model):
    offender_name = CharField(max_length=30, unique=True, null=False)
    user_id = ForeignKey(Users, on_delete=models.CASCADE)
    observable_account_id = ForeignKey(Observable_Account, on_delete=models.CASCADE)
    email_address_of_offender = CharField(max_length=30, null=False)

class Trusted_Contact(models.Model):
    user_id = ForeignKey(Users, on_delete=models.CASCADE)
    contact_name = CharField(max_length=30, unique=True, null=False)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=30, null=False)
    priority = CharField(max_length=30)

class Authority(models.Model):
    authority_name = CharField(max_length=30, unique=True, null=False)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=30, null=False)
    type = CharField(max_length=20, null=False) # police, agency, ngo,
    country = CharField(max_length=20, null=False)
    region = CharField(max_length=20, null=False) # dhaka, chittagong



class Prediction(models.Model):
    offender_id = models.FloatField(default=0)#ForeignKey(Offender, on_delete=models.SET_NULL, null=True)
    #feedback_id = ForeignKey(User_Feedback)
    toxic_percentage = models.FloatField(default=0)
    severe_toxic_percentage = models.FloatField(default=0)
    obscene_percentage = models.FloatField(default=0)
    threat_percentage = models.FloatField(default=0)
    insult_percentage = models.FloatField(default=0)
    identity_hate_percentage = models.FloatField(default=0)
    average_percentage = models.FloatField(default=0)


class User_Feedback(models.Model):
    user_id = ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    prediction_id = ForeignKey(Prediction, on_delete=models.SET_NULL, null=True)
    action_taken_against_offender = CharField(max_length=20, null=False)
    comment = CharField(max_length=100, null=True)


class Message(models.Model):
    user_id = ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    observable_account_id = ForeignKey(Observable_Account, on_delete=models.SET_NULL, null=True)
    sender_email_address = CharField(max_length=20, null=False)
    time_and_date = DateTimeField(auto_now_add=True , null=False)
    ip_address = CharField(max_length=64, null=False) ###????
    contents = CharField(max_length=500, null=False)

class History(models.Model):
    user_id = ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    authority_id = ForeignKey(Authority, on_delete=models.SET_NULL, null=True)
    message_id = ForeignKey(Message, on_delete=SET_NULL, null=True)
    user_feedback_id = ForeignKey(User_Feedback, on_delete=models.SET_NULL, null=True)
    #????



from django.db import models


class payment_stats(models.Model):
	status = models.CharField(max_length=10)
	firstname = models.CharField(max_length=10)
	amount = models.FloatField(max_length=10)
	txnid = models.CharField(max_length=20)
	productinfo = models.CharField(max_length=20)








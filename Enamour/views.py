from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template, RequestContext
import datetime
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf


def Home(request):
	MERCHANT_KEY = "EPLXxZ4h"
	key = "EPLXxZ4h"
	SALT = "q2plxvdank"
	PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
	action = ''
	posted = {'amount': '10',
			  'firstname': 'renjith',
			  'email': 'sraj@gmail.com',
			  'phone': '9746272610', 'productinfo': 'test',
			  'lastname': 'test', 'address1': 'test',
			  'address2': 'test', 'city': 'test',
			  'state': 'test', 'country': 'test',
			  'zipcode': 'tes', 'udf1': '',
			  'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
			  }
	# Merchant Key and Salt provided y the PayU.
	for i in request.POST:
		posted[i] = request.POST[i]
	hash_object = hashlib.sha256(b'randint(0,20)')
	txnid = hash_object.hexdigest()[0:20]
	hashh = ''
	posted['txnid'] = txnid
	hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
	posted['key'] = key
	hash_string = ''
	hashVarsSeq = hashSequence.split('|')
	for i in hashVarsSeq:
		try:
			hash_string += str(posted[i])
		except Exception:
			hash_string += ''
		hash_string += '|'
	hash_string += SALT
	hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
	action = PAYU_BASE_URL
	mycontext = {"head": "PayU Money", "MERCHANT_KEY": MERCHANT_KEY, "posted": posted, "hashh": hashh,
				 "hash_string": hash_string, "txnid": txnid, "action": action}

	if (posted.get("key") != None and posted.get("txnid") != None and posted.get("productinfo") != None and posted.get(
			"firstname") != None and posted.get("email") != None):
		return render(request, 'current_datetime.html', context=mycontext)
	else:
		return render_to_response('current_datetime.html', RequestContext(request, {"posted": posted, "hashh": hashh,
																					"MERCHANT_KEY": MERCHANT_KEY,
																					"txnid": txnid,
																					"hash_string": hash_string,
																					"action": action}))


@csrf_protect
@csrf_exempt
def success(request):
	c = {}
	c.update(csrf(request))
	status = request.POST.get("status")
	firstname = request.POST.get("firstname")
	amount = request.POST.get("amount")
	txnid = request.POST.get("txnid")
	posted_hash = request.POST.get("hash")
	key = request.POST.get("key")
	productinfo = request.POST.get("productinfo")
	email = request.POST.get("email")
	salt = "GQs7yium"
	try:
		additionalCharges = request.POST["additionalCharges"]
		retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
	except Exception:
		retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
	hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
	if (hashh != posted_hash):
		print("Invalid Transaction. Please try again")
	else:
		print("Thank You. Your order status is ", status)
		print("Your Transaction ID for this transaction is ", txnid)
		print("We have received a payment of Rs. ", amount, ". Your order will soon be shipped.")
	context = {"txnid": txnid, "status": status, "amount": amount}
	return render_to_response('sucess.html', RequestContext(request,context))


@csrf_protect
@csrf_exempt
def failure(request):
	c = {}
	c.update(csrf(request))
	status = request.POST.get("status")
	firstname = request.POST.get("firstname")
	amount = request.POST.get("amount")
	txnid = request.POST.get("txnid")
	posted_hash = request.POST.get("hash")
	key = request.POST.get("key")
	productinfo = request.POST.get("productinfo")
	email = request.POST.get("email")
	salt = "q2plxvdank"
	try:
		additionalCharges = request.POST["additionalCharges"]
		retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
	except Exception:
		retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
	hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
	if (hashh != posted_hash):
		print("Invalid Transaction. Please try again")
	else:
		print("Thank You. Your order status is ", status)
		print("Your Transaction ID for this transaction is ", txnid)
		print("We have received a payment of Rs. ", amount, ". Your order will soon be shipped.")
	return render_to_response("Failure.html", RequestContext(request, c))

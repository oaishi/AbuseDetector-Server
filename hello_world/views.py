from django.shortcuts import render
import json
from django.contrib.auth.models import User #####
from django.http import JsonResponse , HttpResponse ####

from bs4 import BeautifulSoup


from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from hello_world import models

# Create your views here.
print('\n>>>Server initialized<<<\n')
import tensorflow as tf
from hello_world.SmartAgent_API import *
model = load_model()
graph = tf.get_default_graph()

# Create your views here.
import gc


def hello_world(request):
    return render(request, 'hello_world.html', {})

def mail_receive(request):
    htmlmail = request.GET.get('htmlmail', None)
    sender = request.GET.get('sender', None)
    date = request.GET.get('date', None)
    subject = request.GET.get('subject', None)

    print('mail sent: ', htmlmail, 'sender: ', sender, 'date: ', date, 'subject: ', subject)

    soup = BeautifulSoup(htmlmail, "lxml")
    text_of_mail = soup.get_text()

    with graph.as_default():
        prediction = predict_single_sentence(model=model, _sentence_=text_of_mail)
    print(prediction)
    # return render(request, 'hello_world.html', {'sentence': x, 'prediction': prediction[0]})

    message = models.Prediction()

    data = {'sentence': text_of_mail}
    for i in range(6):
        print(str(abuseDimensions[i]), float(prediction[0][i])*100)
        data[str(abuseDimensions[i])] = round(float(prediction[0][i])*100,0)
        # print(abuseDimensions[i], ':', testPrediction[0][i] * 100.0, '%')
    data['is_taken'] = True,  #if sentence is abusive
    data['raw'] = 'Mail received!'
    data['sender'] = sender
    data['date'] = date
    data['subject'] = subject

    message.toxic_percentage = data['toxic']
    message.severe_toxic_percentage = data['severe_toxic']
    message.threat_percentage = data['threat']
    message.obscene_percentage = data['obscene']
    message.insult_percentage = data['insult']
    message.identity_hate_percentage = data['identity_hate']

    # thresholding
    data['thres'] = 50
    conn__ = 'abc|'+sender
    l__ = list(channel_map)
    print('channels:',l__)
    if conn__ in channel_map:
        print('connection:',channel_map[conn__])
        thresh__ = channel_map[conn__][1]*100
        data['thres'] = thresh__

        if message.toxic_percentage <  thresh__ and message.severe_toxic_percentage < thresh__ and  message.threat_percentage < thresh__ and message.obscene_percentage < thresh__ and message.insult_percentage < thresh__ and message.identity_hate_percentage < thresh__:
            data['is_taken'] = False



    data['average'] =  round((data['toxic'] + data['severe_toxic'] + data['threat'] + data['obscene'] + data['insult'] + data['identity_hate'])/6,2)

    message.average_percentage = round((data['toxic'] + data['severe_toxic'] + data['threat'] + data['obscene'] + data['insult'] + data['identity_hate'])/6,2)

    message.offender_id = 1

    message.save()

    gc.collect()

    return JsonResponse(data=data)


class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = UserCreationForm

def validate_username(request):
    username = request.GET.get('username', None)
    password = request.GET.get('password', None)

    print('username:', username, 'pass:', password)

    check = True
    check2 = True
    try:
        q = models.Users.objects.get(user_name=username)
        print("query:", q.user_name, q.password, q.pk)
        if q.password != password:
            check2 = False
    except:
        print("in except of database query.", username, "not found.")
        check = False

    #while True:
    #    pass

    if check:
        if check2:
            data = {
                'is_taken': True,
                'raw': 'Login Successful',
                'username': q.user_name,
                'email': q.email_address,
                'phone': q.phone_number,
                'country': q.country,
                'name': q.first_name + ' ' +q.last_name,
            }
        else:
            data = {
                'is_taken': False,
                'raw': 'Login Unsuccessful! Invalid Password',
                'username': username,
                # 'q.username': q.user_name,
                # 'q.password': q.password,
            }
    else:
        data = {
            'is_taken': False,
            'raw': 'Not in database',
            'username': username,
        }

    print('json-data to be sent: ',data)

    return JsonResponse(data)
    #return HttpResponse(json.dumps(data), mimetype='application/json')

def discarding(request):
    username = request.GET.get('username', None)
    sender = request.GET.get('sender', None)
    val = request.GET.get('x', None)

    print('username:', username, 'sender:', sender,'val',val)

    check = True
    check2 = True
    try:
        q = models.Users.objects.get(user_name=username)
        print("query:", q.user_name, q.password, q.pk)
    except:
        print("in except of database query.", username, "not found.")
        check = False

    #while True:
    #    pass

    if check:
        data = {
            'is_taken': True,
            'raw': 'Threshold Updated!',
        }

        conn = username + '|' + sender
        print()
        if val == '0':
            if conn in channel_map:
                x = channel_map[conn][0]
                y = channel_map[conn][1]
                channel_map[conn] = [x + 1, custom_sigmoid(x + 1)]
                print('Previous threshold', y * 100, '%\nNew threshold', custom_sigmoid(x + 1)*100, '%\n')
            else:
                channel_map[conn] = [1, custom_sigmoid(1)]
                print('set',conn,channel_map[conn])

        elif val == '1':
            if conn in channel_map:
                x = channel_map[conn][0]
                y = channel_map[conn][1]
                if x > 0:
                    channel_map[conn] = [x - 1, custom_sigmoid(x - 1)]
                    print('Previous threshold', y * 100, '%\nNew threshold', custom_sigmoid(x + 1)*100, '%\n')
            else:
                channel_map[conn] = [0, custom_sigmoid(0)]
                print('set', channel_map[conn])



    else:
        data = {
            'is_taken': False,
            'raw': 'Unsuccessful!',
        }

    print('json-data to be sent: ',data)

    return JsonResponse(data)
    #return HttpResponse(json.dumps(data), mimetype='application/json')


def validate_registration(request):

    firstname = request.GET.get('firstname', None)
    lastname = request.GET.get('lastname', None)
    username = request.GET.get('username', None)
    password = request.GET.get('password', None)
    email = request.GET.get('email', None)
    phone = request.GET.get('phone', None)
    gender = request.GET.get('gender', None)
    country = request.GET.get('country', None)
    date = request.GET.get('date', None)

    #print('username:', firstname, 'email:', email , 'phone:', phone , 'gender:', gender , 'country:', country ,'date:', date)

    newuser = models.Users()

    newuser.user_name = username
    newuser.email_address = email
    newuser.first_name = firstname
    newuser.last_name = lastname
    newuser.password = password
    newuser.phone_number = phone
    newuser.country = country
    newuser.gender = gender.lower()

    try:
        newuser.save()
    except:
        pass

    data = {
        'is_taken': True,
        'raw': 'Signup Successful!',
        'username': username,
    }

    print('json-data to be sent: ',data)

    return JsonResponse(data)
    #return HttpResponse(json.dumps(data), mimetype='application/json')

def add_offender(request):

    offender_name = request.GET.get('offender_name', None)
    offender_email = request.GET.get('offender_email', None)
    username = request.GET.get('username', None)

    print('username:', username)

    check = True
    try:
        q = models.Users.objects.get(user_name=username)
        print("query:", q.user_name, q.password)
    except:
        print("in except of database query.", username, "not found.")
        check = False

    #while True:
    #    pass


    if check:
        id = q.pk
        newOffender = models.Offender()
        newOffender.offender_name = offender_name
        newOffender.email_address_of_offender = offender_email
        newOffender.user_id = q
        newOffender.observable_account_id = 1

        try:
            newOffender.save()
            data = {
                'is_taken': True,
                'raw': 'Offender Added!',
            }

        except:
            data = {
                'is_taken': False,
                'raw': 'Error while adding Offender!',
            }

    return JsonResponse(data)
    #return HttpResponse(json.dumps(data), mimetype='application/json')


def add_trusted_contact(request):

    contact_name = request.GET.get('contact_name', None)
    contact_email = request.GET.get('contact_email', None)
    contact_number = request.GET.get('contact_number', None)
    priority = request.GET.get('priority', None)
    username = request.GET.get('username', None)

    print('username:', username)

    check = True
    try:
        q = models.Users.objects.get(user_name=username)
        print("query:", q.user_name, q.password)
    except:
        print("in except of database query.", username, "not found.")
        check = False

    #while True:
    #    pass


    if check:

        id = q.pk
        newContact = models.Trusted_Contact()
        newContact.contact_name = contact_name
        newContact.email_address = contact_email
        newContact.phone_number = contact_number
        newContact.priority = priority
        newContact.user_id = q

        try:
            newContact.save()
            data = {
                'is_taken': True,
                'raw': 'Contact Added!',
            }

        except:
            data = {
                'is_taken': False,
                'raw': 'Error while adding Contact!',
            }

    print(data['raw'])

    return JsonResponse(data)
    #return HttpResponse(json.dumps(data), mimetype='application/json')


def change_username(request):
    oldusername = request.GET.get('oldusername', None)
    newusername = request.GET.get('newusername', None)

    print('oldusername:', oldusername, 'new: ', newusername)

    check = True
    try:
        q = models.Users.objects.get(user_name=oldusername)
        print("query:", q.user_name, q.password)
    except:
        print("in except of database query.", oldusername, "not found.")
        check = False

    #while True:
    #    pass

    if check:
        q.user_name = newusername

        try:
            q.save()
            data = {
                'is_taken': True,
                'raw': 'Username Change Successful!',
            }

        except:
            data = {
                'is_taken': False,
                'raw': 'Username Change Unsuccessful!',
            }
    else:
        data = {
                'is_taken': False,
                'raw': 'Invalid Old Username!',
            }

    print('json-data to be sent: ',data)

    return JsonResponse(data)
    #return HttpResponse(json.dumps(data), mimetype='application/json')


def change_email(request):
    oldusername = request.GET.get('oldusername', None)
    newemail = request.GET.get('newemail', None)

    print('oldusername:', oldusername, 'new: ', newemail)

    check = True
    try:
        q = models.Users.objects.get(user_name=oldusername)
        print("query:", q.user_name, q.password)
    except:
        print("in except of database query.", oldusername, "not found.")
        check = False

    # while True:
    #    pass

    if check:
        q.email_address = newemail

        try:
            q.save()
            data = {
                'is_taken': True,
                'raw': 'Email Change Successful!',
            }

        except:
            data = {
                'is_taken': False,
                'raw': 'Email Change Unsuccessful!',
            }
    else:
        data = {
            'is_taken': False,
            'raw': 'Invalid Username!',
        }
    print('json-data to be sent: ', data)

    return JsonResponse(data)
    # return HttpResponse(json.dumps(data), mimetype='application/json')

def change_password(request):
    oldusername = request.GET.get('oldusername', None)
    oldpassword = request.GET.get('oldpassword', None)
    newpassword = request.GET.get('newpassword', None)

    check = True
    check2 = True
    try:
        q = models.Users.objects.get(user_name=oldusername)
        print("query:", q.user_name, q.password)
        if q.password != oldpassword:
            check2 = False
    except:
        print("in except of database query.", oldusername, "not found.")
        check = False

    # while True:
    #    pass

    if check:
        if check2:
            q.password = newpassword

            try:
                q.save()
                data = {
                    'is_taken': True,
                    'raw': 'Password Change Successful!',
                }

            except:
                data = {
                    'is_taken': False,
                    'raw': 'Password Change Unsuccessful!',
                }
        else:
            data = {
                'is_taken': False,
                'raw': 'Invalid Old Password',
            }
    else:
        data = {
            'is_taken': False,
            'raw': 'Username Not in database',
        }

    print('json-data to be sent: ', data)

    return JsonResponse(data)
    # return HttpResponse(json.dumps(data), mimetype='application/json')

def change_number(request):
    oldusername = request.GET.get('oldusername', None)
    newnumber = request.GET.get('newnumber', None)

    print('oldusername:', oldusername, 'new: ', newnumber)

    check = True
    try:
        q = models.Users.objects.get(user_name=oldusername)
        print("query:", q.user_name, q.password)
    except:
        print("in except of database query.", oldusername, "not found.")
        check = False

    # while True:
    #    pass

    if check:
        q.phone_number = newnumber

        try:
            q.save()
            data = {
                'is_taken': True,
                'raw': 'Number Change Successful!',
            }

        except:
            data = {
                'is_taken': False,
                'raw': 'Number Change Unsuccessful!',
            }
    else:
        data = {
            'is_taken': False,
            'raw': 'Invalid Username!',
        }
    print('json-data to be sent: ', data)

    return JsonResponse(data)
    # return HttpResponse(json.dumps(data), mimetype='application/json')

def get_contacts(request):
    username = request.GET.get('username', None)

    print('username:', username)

    check = True
    try:
        q = models.Users.objects.get(user_name=username)
        print("query:", q.user_name, q.password)
    except:
        print("in except of database query.", username, "not found.")
        check = False

    # while True:
    #    pass

    if check:

        id = q.pk

        try:
            q = models.Trusted_Contact.objects.get(user_id=q)

            print("query:", q.email_address)

            data = {
                'is_taken': True,
                'raw': 'Contact Fetch Successful!',
                'email_address' : q.email_address,
            }

        except:
            data = {
                'is_taken': False,
                'raw': 'No Contacts Added for this user!',
            }
    else:
        data = {
            'is_taken': False,
            'raw': 'Invalid Username!',
        }
    print('json-data to be sent: ', data)

    return JsonResponse(data)
    # return HttpResponse(json.dumps(data), mimetype='application/json')
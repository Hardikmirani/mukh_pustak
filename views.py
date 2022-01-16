# Create your views here.
from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from .models import Profile, FriendRequest, BlockFriend , MessageFriend
from django.contrib.auth.models import User, auth
from random import randint
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from itertools import chain
import json
from django.contrib import messages   

import joblib

# clf = joblib.load("/Users/hardik/Desktop/Yudiz/envpy/Final_mpp/static/model_pkl")


otp = randint(000000,999999) 


# Create your views here.
def sample(request):
    return HttpResponse("Hello")



def login(request):

    if request.method=="POST":
        
        username = request.POST['username']
        request.session['username'] = request.POST['username']
        print(request.session['username'])
  
        password = request.POST['password']
        try :
            user = auth.authenticate(username= username , password = password)
            print("ffhfhhfhfhf",user.username)


            if user is not None:

                myuser = User.objects.get(username = user.username)
                print("iiiiiid", myuser.id)
                myprofile = Profile.objects.get(user = myuser.id)
                myprofile.onoff = True
                myprofile.save()

            
                return redirect(dashboard)

            else :
                messages.error(request,'username or password not correct')
                return render(request, "login.html")
        except:
            # print("fail")
            return render(request, "login.html")

    return render(request, "login.html")



def dashboard(request):
    if not request.session.has_key('username'):
        print("No")

        return redirect('login')
    else:
        print("yes")

        context ={}

        myuser = User.objects.get(username = request.session['username']) 
        myprofile = Profile.objects.get(user = myuser.id)
        p = myuser.profile
        friends = p.friends.all()
        u = User.objects.all()
        # a = "/Users/hardik/Desktop/Yudiz/envpy/mukh_pustak/default.png"

        userlist = []
        for i in u:
            userlist.append(i.username)

        print(userlist)
        print (json.dumps(userlist))
        # ulist = json.dumps(userlist)
        urlist = ["a","aa","aaa"]
    
        ulist = json.dumps(urlist)
        print(ulist)    
        # b = BlockFriend.objects.filter(b_from_user = myuser)
        # print("blocked",b)
        # b = BlockFriend.objects.get(b_from_user = myuser)

        # q = myuser.BlockFriend
        # blocked = q.b_to_user.all()
        # print(blocked)

        # con={
        # 'friends': friends
        # }
        context = {
		'username': request.session['username'],
        'profile' : myprofile,
        'friends': friends,
        'u': ulist,
        # 'blocked': blocked,
	    }
    
    return render(request, "dashboard.html", context)


def register(request):

    if request.method == 'POST':
        username  = request.POST['username']
        email  = request.POST['email']
        password  = request.POST['password']
        password2  = request.POST['password2']

        if password == password2:
            if User.objects.filter(username = username).exists():
                print("Username Exists")
                return redirect('login')
            else:
                user = User.objects.create_user(username = username ,email = email, password = password)
                user.save()
                # pro = Profile.objects.creaxte(user = user)
                # pro.save()
                return redirect('login')
        else:
            print("not correct password")
    return render(request,'register.html')



def edit_profile(request):

    # username = request.session['username']
    
    myuser = User.objects.get(username = request.session['username'])
    editprofile = Profile.objects.get(user = myuser.id)
    print(editprofile.image)
    print(editprofile.bio)
    # print(editprofile.slug)
    context = {
		'bio': editprofile.bio,
        # 'blocked': blocked,
	    }

    if request.method =="POST":

        editprofile.image = request.POST['image']
        editprofile.bio = request.POST['bio']
        print("bio of pro " ,editprofile.bio)
        print(Profile.bio)
        editprofile.save()



        # context = {
		# 'bio': editprofile.bio,
        # # 'blocked': blocked,
	    # }

        
        
        # Profile.objects.update(image = editimage , bio = editbio)

        return redirect('dashboard')

    return render(request,'edit_profile.html',context)


# def make_friends(request):

#     return render(request,'make_friends.html')
    
   
    # return render(request, "make_friends.html", context)

def pending_requests(request):


    if not request.session.has_key('username'):
        print("No")

        return redirect('login')
    print("yes")
    u = User.objects.get(username = request.session['username'])
    users = Profile.objects.get(user= u.id)
    print("users",users)

    a = User.objects.get(username =users)
    print('a',a)
    recieve_friend_requests = FriendRequest.objects.filter(to_user= a)
    print('recieve_friend_requests',recieve_friend_requests)
    recieve_from = []

    for re in recieve_friend_requests:
        recieve_from.append(re.from_user.username)

    
        

    context = {
        'recieve': recieve_from
    }
    # if request.session['username'] in FriendRequest.from_user:
	# }
    return render(request, "pending.html", context)

def accept(request,username):
    
    from_user = get_object_or_404(User, username= username)
    print("fffggggggg",from_user)
    a = User.objects.get(username = request.session['username'])
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=a).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    if(FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()):
        request_rev = FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()
        request_rev.delete()
    frequest.delete()
    return redirect('dashboard')



def reject(request,username):
    from_user = get_object_or_404(User, username = username)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return redirect('dashboard')



def make_friends(request):
    query = request.GET.get('query')
    object_list = User.objects.filter(username__icontains=query)
    # print(object_list)
    # print(type(object_list))

    current_s = User.objects.get(username = request.session['username'])

    blocked_users = BlockFriend.objects.filter(b_from_user = current_s)
    # lm = blocked_users.b_to_user

    # bu = BlockFriend.objects.filter(b_to_user = )

    

    print("abcdefg",blocked_users)

    a = []
    for i in blocked_users:
        a.append(i.b_to_user)
    print("a = " ,a)

    abc = []
    for j in a:
        ab = User.objects.get(username = j)
        abc.append(ab.username)
    print('abc',abc)

    # if current_s in BlockFriend.b_to_user:
        

    lms = BlockFriend.objects.filter(b_to_user = current_s)
    # print('nacho nacho',lms.b_from_user)




    b = []

    for k in lms:
        b.append(k.b_from_user)
    print("b = ", b)

    de = []
    for l in b:
        cd = User.objects.get(username = l)
        de.append(cd.username)
    print('de',de)


    # cd = []

    for i in abc :
        de.append(i)

    print("cd",de)


    # exc_friend
    # abcd = ['Keyur', 'Baburao']
    exc_blo = object_list.exclude(username__in = de)
    print("exc_cur",exc_blo)
    # exc_friend = exc_cur.exclude(username = )
    # blocked_u = []
    # for i in blocked_users:
    #     a = i.b_to_user
    #     b_name = a.username
    #     blocked_u.append(a.username)
    # print('ar',blocked_u)
    # print('exc_cur',exc_cur)
        
    # finala = object_list.exclude(username = blocked_u)
    # print("excluding all : - ",finala)
    # myuser = User.objects.get(username = request.session['username'])
    # myprofile = Profile.objects.get(user = myuser.id)
    #     p = myuser.profile
    #     friends = p.friends.all()
    #     fri = []

    #     fri.append(friends.username)

    exc_fin = exc_blo.exclude(username = current_s.username)
    print(exc_fin)



    



    context ={
        'users': exc_fin
    }
    return render(request, "make_friends.html", context)


def delete_friend(request, id):
    user_pr = User.objects.get(username = request.session['username'])
    # user_profile
    user_profile = Profile.objects.get(user = user_pr)
    friend_profile = Profile.objects.get(id = id)
    # friend_profile = get_object_or_404(Profile, id = id)

    user_profile.friends.remove(friend_profile)
    friend_profile.friends.remove(user_profile)
    return redirect('dashboard')

def friend_request(request, username):

    # user = User.objects.get(username = username )
    # user = get_object_or_404(User, username=username)
    from_user = User.objects.get(username = request.session['username'])
    to_user = User.objects.get(username = username)
    a = FriendRequest.objects.create(from_user = from_user, to_user = to_user)
    # frequest, created = FriendRequest.objects.get_or_create(
    #         from_user=request.user,
    #         to_user=user)
    return redirect('dashboard')


def block_friend(request, username):
    
    b_from_user = User.objects.get(username = request.session['username'])
    b_to_user = User.objects.get(username = username)
    print(b_from_user)
    print(b_to_user)
    try :
        BlockFriend.objects.get(b_from_user = b_from_user, b_to_user = b_to_user)
        return redirect('dashboard')
    except:
        a = BlockFriend.objects.create(b_from_user = b_from_user, b_to_user = b_to_user)
        print("aaaaaa",a)
        return redirect('dashboard')

def message(request,id):


    # user  = User.objects.get(id = id)
    # print(user.username)
    a = User.objects.get(username = request.session['username'])
    b = User.objects.get(id = id)

    proa = Profile.objects.get(user = a)
    prob = Profile.objects.get(user = b)
    print(proa.image)
    print(prob.image)

    

    # check_block1 = BlockFriend.objects.get(b_from_user = id , b_to_user = a.id)
    if BlockFriend.objects.filter(b_from_user = a.id, b_to_user = id).exists():
        print("Hello")
        return redirect('dashboard')
        # return render(request,'message.html')
    elif BlockFriend.objects.filter(b_from_user = id, b_to_user = a.id).exists():
        return redirect('dashboard')
    else:
        context ={}


        mes1 = MessageFriend.objects.filter(m_from_user = a.id, m_to_user = id)
        mes2 = MessageFriend.objects.filter(m_from_user = id, m_to_user = a.id)
        # print(mes1)
        # print(mes2)
        # MessageFriend.objects.filtet("text").order_by("-timestamp")
        # a = mes1 + mes2
        # print(a)
        # from itertools import chain
        # result_list = list(chain(mes1, mes2))
        result_list = sorted(
            chain(mes1, mes2),
            key=lambda instance: instance.timestamp)
        

        fromuser = User.objects.get(id= id)
        Pro = Profile.objects.get(user = fromuser.id)
        print(Pro.onoff)

        if Pro.onoff == True:
            status = "Online"
        else:
            status = "Offline"

        current_u = User.objects.get(username = request.session['username'])
        # myprofile = Profile.objects.get(user = myuser.id)
        # myprofile.onoff = True
        # myuser = User.objects.get(username = request.session['username'])
        # myprofile = Profile.objects.get(user = myuser.id)
        # p = myuser.profile
        # friends = p.friends.all()
        context ={
        'mes1': result_list , 
        # 'mes2': mes2 ,
        'id':id,
        'status': status,
        'current_u' : current_u,
        'proa':proa,
        'prob':prob
    }

        return render(request,'message.html', context)

    # return render(request,'message.html')

def send_message(request,id):

    message = request.POST['message']
    a = User.objects.get(username = request.session['username'])
    b = User.objects.get(id = id)

    MessageFriend.objects.create(m_from_user = a , m_to_user = b, message = message)

    context ={}


    mes1 = MessageFriend.objects.filter(m_from_user = a.id, m_to_user = id)
    mes2 = MessageFriend.objects.filter(m_from_user = id, m_to_user = a.id)
    data = [message]

    result_list = sorted(
            chain(mes1, mes2),
            key=lambda instance: instance.timestamp)
        

    fromuser = User.objects.get(id= id)
    Pro = Profile.objects.get(user = fromuser.id)
    print(Pro.onoff)

    if Pro.onoff == True:
        status = "Online"
    else:
        status = "Offline"

    current_u = User.objects.get(username = request.session['username'])
    # my_prediction = clf.predict(data)
    # myuser = User.objects.get(username = request.session['username'])
    # myprofile = Profile.objects.get(user = myuser.id)
    # p = myuser.profile
    # friends = p.friends.all()
    
    context ={
        'mes1': result_list , 
        # 'mes2': mes2 ,
        'id':id,
        'status': status,
        'current_u' : current_u
    }

    return render(request,'message.html', context)

    # return None









def logout(request):

    myuser = User.objects.get(username = request.session['username'])
    myprofile = Profile.objects.get(user = myuser.id)
    myprofile.onoff = False
    myprofile.save()
    request.session.pop('username', None)
    return redirect('login')

    



# Create your views here.
# def login(request):
#     if request.method=="POST":
        
#         username = request.POST['username']
#         request.session['username'] = request.POST['username']
#         print(request.session['username'])
  
#         password = request.POST['password']
#         print(password)
#         try :
#             user = auth.authenticate(username= username , password = password)
#             print("ffhfhhfhfhf",user.username)
#             print("ffhfhhfhfhf",user.password)

#             if user is not None:
#                 print("efgh")

#                 return redirect('dashboard')

#             else :
#                 print("abcd")
#                 return render(request,"login.html")
#         except:
#             print("fail")
#             return render(request, "login.html")
#     return render(request,'login.html')

# def register(request):

#     if request.method == 'POST':
#         username  = request.POST['username']
#         email  = request.POST['email']
#         password  = request.POST['password']
#         password2  = request.POST['password2']

#         if password == password2:
#             if User.objects.filter(username = username).exists():
#                 print("Username Exists")
#                 return redirect('login')
#             else:
#                 user = User.objects.create_user(username = username ,email = email, password = password)
#                 user.save()
#                 return redirect('login')
#         else:
#             print("not correct password")
#     return render(request,'register.html')


def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        request.session["email"] = request.POST["email"]
        user = User.objects.get(email = email)
        print('user:',user)
            

        if user is not None:

            subject = 'OTP verification of Mukh-Pustak Account'
            message = f'Hi {user.username}, Here is your otp = >  ' + str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email,]
            send_mail( subject, message, email_from, recipient_list )
        
            return render(request,'verifyotp.html')
    return render(request,'reset.html')


def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST['otp'] 
        print(user_otp)
        request.session["user_otp"] = request.POST["otp"]
        if otp == int(user_otp):

            print("IT's matched")
            return redirect('reset_password')

    
    return render(request,'verifyotp.html')



def reset_password(request):

    user = User.objects.get(email = request.session['email'])
    print (user.username)

    if not request.session.get('user_otp'):
        return redirect('/')

    if request.method == "POST":
        user = User.objects.get(email = request.session['email'])
        print(user.username)
        print(user.password)

        password = request.POST['password']
        user.set_password(password)
        user.save()

        request.session.pop('user_otp',None)
        request.session.pop('email',None)
        return redirect('dashboard')

    return render(request,'resetpassword.html')


# def logout(request):
#     request.session.pop('username', None)
#     return redirect('login')

    

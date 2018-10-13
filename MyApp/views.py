from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import *
from .models import *
from django.contrib.auth.decorators import login_required


def login(request):
    try:
        mobile = request.session['mobile']
        if mobile:
            return HttpResponseRedirect('/dashboard/')
        else:
            return render(request, 'login.html')
    except Exception:
        return render(request,'login.html')

def base(request):
    return render(request,'base.html')


def registration(request):
    reg = Registration.objects.all()
    return render(request,'Registration.html',{'reg':reg})
#@login_required(login_url='/login/')

def dashboard(request):

    try:
        mobile = request.session['mobile']
        if mobile:
            student = StudentData.objects.all()
            data = Registration.objects.filter(mobile=mobile).all()
            return render(request,'dashboard.html',{"data": data, 'student': student})
        else:
            return HttpResponseRedirect('/login/')


    except KeyError as e:
        return HttpResponseRedirect('/login/')





# def dashboard(request):
#     mobile = request.session['mobile']
#     if mobile:
#         try:
#             if mobile:
#                 student = StudentData.objects.all()
#                 data = Registration.objects.filter(mobile=mobile).all()
#                 return render(request, 'dashboard.html', {"data": data, 'student': student})
#             else:
#                 return HttpResponseRedirect('/login/')
#         except KeyError:
#             raise HttpResponseRedirect('/login/')
#     else:
#         return HttpResponseRedirect('/login/')





#@login_required(login_url='/login/')
@csrf_exempt
def loginUser(request):
    response = {}

    if request.method == "POST":
        mobile = request.POST['mobile']
        password = request.POST['password']
        try:
            login = Registration.objects.get(mobile=mobile, password=password)
            if login :
                request.session['mobile'] = mobile
                response['success']=True
                return JsonResponse(response)
                #return HttpResponseRedirect('/dashboard/')
            else:
                response['success']=False
                return JsonResponse(response)
        except Exception as e:
            print("Login Error")


        return JsonResponse(response)





@csrf_exempt
def register_data_store(request):
    response={}
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        # print(name)
        # print(email)
        # print(mobile)
        # print(gender)
        # print(password)
        # return JsonResponse(response)

        reg = Registration.objects.create(name=name,email=email,mobile=mobile,gender=gender,password=password)
        if reg:
            response['success']=True
            return JsonResponse(response)
        else:
            response['success']=False
            return JsonResponse(response)


    else:
        return render(request,'Registration.html',{'status':"Not Store Data In Database"})


@csrf_exempt
def profile_update(request):
    student = StudentData.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        Registration.objects.filter(mobile=mobile).update(name=name,email=email,password=password)
        data = Registration.objects.filter(mobile=mobile)
        return render(request,'dashboard.html',{"data": data,'student':student})
    else:
        return render(request, 'dashboard.html', {'student': student})



def material(request):
    return render(request,'material.html')



def studentpage(request):
    sid = request.GET.get('sid')
    #print(sid)
    student = StudentData.objects.filter(sid=sid)


    return render(request, 'studentpage.html',{'student':student})

@csrf_exempt
def student_data_store(request):
    response={}
    if request.method == "POST":
        sid = request.POST.get('sid')
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        # print(sid)
        # print(name)
        # print(email)
        # print(mobile)
        # print(gender)
        # print(password)
        # print(dob)
        # print(address)
        # response['success']=True
        # return JsonResponse(response)
        try:
            reg = StudentData.objects.create(sid=sid,name=name,email=email,mobile=mobile,password=password,gender=gender,dob=dob,address=address)
            if reg:
                response['success'] = True
                return JsonResponse(response)
            else:
                response['success'] = False
                return JsonResponse(response)

        except Exception as ex:
            print(ex)
            return render(request,'studentpage.html',{'msg':"This ID Already Exist"})
    else:
        return render(request,'studentpage.html',{'status1':"Record Not Store"})



@csrf_exempt
def student_data_update(request):
    response={}
    if request.method == "POST":
        sid = request.POST.get('sid')
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        # print(sid)
        # print(name)
        # print(email)
        # print(mobile)
        # print(password)
        # print(address)
        # print(dob)
        # response['success']=True
        # return JsonResponse(response)
        try:
            std = StudentData.objects.filter(sid=sid).update(name=name, email=email,mobile=mobile,
                                                             password=password,dob=dob, address=address)
            #print(std)
            if std:
                response['success'] = True
                return JsonResponse(response)
            else:
                response['success'] = False
                return JsonResponse(response)
        except Exception as e:
            print(e)



@csrf_exempt
def student_data_delete(request):
    sid = request.GET.get('sid')
    print(sid)
    StudentData.objects.filter(sid=sid).delete()
    return HttpResponseRedirect('/dashboard/')



def resetpage(request):
    reg = Registration.objects.all()
    return render(request,'forget.html',{'reg':reg})

@csrf_exempt
def reset_password(request):
    response={}
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        # print(mobile)
        # print(password)
        try:
            reg = Registration.objects.filter(mobile=mobile).update(password=password)
            if reg:
                response['success']=True
                return JsonResponse(response)
            else:
                response['success']=False
                return JsonResponse(response)
        except Exception as e:
            raise Http404


    else:
        return render(request,'forget.html')



@csrf_exempt
def logout(request):
    try:
        del request.session['mobile']
        return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')








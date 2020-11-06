from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group

from .models import *
from .serializers import UserInfoSerializer, RecordSerializer

from rest_framework import viewsets, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .decorators import unauthenticated_user, allowed_users, admin_only
from django.views.decorators.csrf import csrf_exempt 

from .forms import *

from django.shortcuts import render
from django.views.decorators import csrf
from django.http import HttpResponse
import pygraphviz as pgv
import collections
from collections import deque
from .models import UserInfo, Contact, Record

# from .models import UserInfo, Contact, Record

# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['tracer'])
def home(request):
    return render(request,'user/home.html', {})

@login_required(login_url='login')
@allowed_users(allowed_roles=['tracer'])
def search_status(request):
    if request.POST:
        context = {}
        user = UserInfo.objects.filter(phone=request.POST['phone'])
        if len(user) == 0:
            context['test_result'] = "No such user in the system"
            return render(request, "user/home.html", context)
        test_result = user[0].test_result
        context['test_result'] = test_result

        user = UserInfo.objects.filter(phone=request.POST['phone'])
        
        contacts1 = Contact.objects.filter(user1=user[0].relate)
        contacts2 = Contact.objects.filter(user2=user[0].relate)
        
        if len(contacts1) == 0 and len(contacts2) == 0:
            context['results'] = "No contact for this person"
            return render(request, "user/home.html", context)
        
        context['results'] = "Contacts with:"
        context['phone'] = []
        for contact in contacts1:
            user1 = UserInfo.objects.filter(relate=contact.user2)
            context['phone'].append(user1[0].phone)

        for contact in contacts2:
            user2 = UserInfo.objects.filter(relate=contact.user1)
            context['phone'].append(user2[0].phone)
        
        contacts = Contact.objects.all()
        A = pgv.AGraph(directed=True)
        A.node_attr['style']='filled'
        s = set()
        for contact in contacts:
            user1 = UserInfo.objects.filter(relate=contact.user1)
            if user1[0].phone not in s:
                s.add(user1[0].phone)
                A.add_node(user1[0].phone)
                if user1[0].test_result == "True":
                    n = A.get_node(user1[0].phone)
                    n.attr['fillcolor']="#F94848"
                else:
                    n = A.get_node(user1[0].phone)
                    n.attr['fillcolor']="#FFFFFF"
        
            user2 = UserInfo.objects.filter(relate=contact.user2)
            if user2[0].phone not in s:
                s.add(user2[0].phone)
                A.add_node(user2[0].phone)
                if user2[0].test_result == "True":
                    n = A.get_node(user2[0].phone)
                    n.attr['fillcolor']="#F94848"
                else:
                    n = A.get_node(user2[0].phone)
                    n.attr['fillcolor']="#FFFFFF"
        
        sp = set()
        for contact in contacts:
            user1 = UserInfo.objects.filter(relate=contact.user1)
            user2 = UserInfo.objects.filter(relate=contact.user2)
            if (user1[0].phone, user2[0].phone) not in sp:
                sp.add((user1[0].phone, user2[0].phone))
                A.add_edges_from([(user1[0].phone, user2[0].phone)])

        A.layout(prog='dot')
        A.draw(path="static/media/images/graph.png", prog='dot')
        context['img'] = "img"
        return render(request, "user/home.html", context)

    

@login_required(login_url='login')
@allowed_users(allowed_roles=['tracer'])
def change_status(request):
    if request.POST:
        context = {}
        user = UserInfo.objects.get(phone=request.POST['phone'])
        test_result = request.POST['status']
        if test_result != "positive" and test_result != "negative" and test_result != "unknown":
            context['msg'] = "invalid status"
            return render(request, "user/home.html", context)
        elif test_result == "positive":
            user.test_result = True
        elif test_result == "negative":
            user.test_result = False
        else:
            user.test_result = None

        user.save()
        context['msg'] = "changed sucessfully"
        return render(request, "user/home.html", context)

    return HttpResponse("Invalid request")

@login_required(login_url='login')
@allowed_users(allowed_roles=['tracer'])
def search_contact(request):
    if request.POST:
        context = {}
        user1 = UserInfo.objects.filter(phone=request.POST['phone1'])
        user2 = UserInfo.objects.filter(phone=request.POST['phone2'])

        contacts1 = Contact.objects.filter(user1=user1[0].relate)
        contacts2 = Contact.objects.filter(user2=user2[0].relate)
        
        if len(contacts1) == 0 and len(contacts2) == 0:
            context['results'] = "No contact for this person"
            return render(request, "user/home.html", context)
        
        context['phone'] = []
        for phone in contacts1:
            context['phone'].append(phone.phone2)

        for phone in contacts2:
            context['phone'].append(phone.phone1)

        return render(request, "user/home.html", context)
    
    return HttpResponse("Invalid request")

@login_required(login_url='login')
@allowed_users(allowed_roles=['tracer'])
def add_contact(request):
    if request.POST:
        context = {}
        user1 = UserInfo.objects.filter(phone=request.POST['phone1'])
        user2 = UserInfo.objects.filter(phone=request.POST['phone2'])
        if  len(user1) > 0 and len(user2) > 0:
            pair = Contact(user1=user1[0].relate, user2=user2[0].relate)
            pair.save()
            context['addmsg'] = "Added sucessfully"
        else:
            context['addmsg'] = "invalid phone number"
        return render(request, "user/home.html", context)
    
    return HttpResponse("Invalid request")

@login_required(login_url='login')
@allowed_users(allowed_roles=['tracer'])
def delete_contact(request):
    if request.POST:
        context = {}
        user1 = UserInfo.objects.filter(phone=request.POST['phone1'])
        user2 = UserInfo.objects.filter(phone=request.POST['phone2'])
        if len(user1) == 0 or len(user2) == 0:
            context['delmsg'] = "No such user in the system"
            return render(request, "user/home.html", context)
            
        Contact.objects.filter(user1=user1[0].relate, user2=user2[0].relate).delete()
        Contact.objects.filter(user1=user2[0].relate, user2=user1[0].relate).delete()
        context['delmsg'] = "Delete sucessfully"
        return render(request, "user/home.html", context)

    return HttpResponse("Invalid request")

@login_required(login_url='login')
@allowed_users(allowed_roles=['tracer'])
def search_records(request):
    if request.POST:
        context = {}
        user = UserInfo.objects.filter(phone=request.POST['phone'])
        if len(user) == 0:
            context['recmsg'] = "No such user in the system"
            return render(request, "user/home.html", context)
    
        records = Record.objects.filter(user=user[0].relate)
        if len(records) == 0:
            context['recmsg'] = "No such record in the system"
            return render(request, "user/home.html", context)
        
        context['records'] = []
        for record in records:
            context['records'].append(record.time)
            context['records'].append(record.location)
            context['records'].append(record.address)  
            context['records'].append("next")       

        return render(request, "user/home.html", context)
    
    return HttpResponse("Invalid request")


@login_required(login_url='login')
@allowed_users(allowed_roles=['tracer'])
def generate_graph(request):
    contacts = Contact.objects.all()
    A = pgv.AGraph(directed=True)
    A.node_attr['style']='filled'
    s = set()
    for contact in contacts:
        user1 = UserInfo.objects.filter(relate=contact.user1)
        if user1[0].phone not in s:
            s.add(user1[0].phone)
            A.add_node(user1[0].phone)
            if user1[0].test_result == "True":
                n = A.get_node(user1[0].phone)
                n.attr['fillcolor']="#F94848"
            else:
                n = A.get_node(user1[0].phone)
                n.attr['fillcolor']="#FFFFFF"
        
        user2 = UserInfo.objects.filter(relate=contact.user2)
        if user2[0].phone not in s:
            s.add(user2[0].phone)
            A.add_node(user2[0].phone)
            if user2[0].test_result == "True":
                n = A.get_node(user2[0].phone)
                n.attr['fillcolor']="#F94848"
            else:
                n = A.get_node(user2[0].phone)
                n.attr['fillcolor']="#FFFFFF"
        
    sp = set()
    for contact in contacts:
        user1 = UserInfo.objects.filter(relate=contact.user1)
        user2 = UserInfo.objects.filter(relate=contact.user2)
        if (user1[0].phone, user2[0].phone) not in sp:
            sp.add((user1[0].phone, user2[0].phone))
            A.add_edges_from([(user1[0].phone, user2[0].phone)])

    A.layout(prog='dot')
    A.draw(path="media/graph.png", prog='dot')
    return render(request, "user/home.html", {}) 


@login_required(login_url='login')
@allowed_users(allowed_roles=['tracer'])
def initiate_cluster(request):
    users = UserInfo.objects.all()
    cluster = 1
    for user in users:
        id = user.relate
        u = UserInfo.objects.get(relate=id)
        if u.test_result == 'True':
            u.cluster_id = cluster
            u.save()
            cluster += 1
        else:
            u.cluster_id = 0
            u.save()

    return render(request, "user/home.html", {}) 



################################################################################################
################################################################################################
##################################    System admin & User   ####################################
################################################################################################
################################################################################################


class UserViewSet(viewsets.ModelViewSet):
    # authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserInfoSerializer(queryset, many=True)
        return Response(serializer.data)
    

class RecordViewSet(viewsets.ModelViewSet):
    # authentication_classes = (BasicAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = StayHomeRecord.objects.all()
    serializer_class = RecordSerializer
    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = RecordSerializer(queryset, many=True)
    #     return Response(serializer.data)

@unauthenticated_user
@csrf_exempt
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(str(user.groups.all()[0]))
            if str(user.groups.all()[0]) == 'normal_user':
                return redirect('user_page')
            elif str(user.groups.all()[0]) == 'tracer':
                return redirect('tracer_home')
            elif str(user.groups.all()[0]) == 'researcher':
                return redirect('researcher_dashboard')
            elif str(user.groups.all()[0]) == 'admin':
                return redirect('homepage')
            else:
                return redirect('homepage')
		# else:
		# 	messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'user/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def registerPage(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='normal_user')
            UserInfo.objects.create(
                relate=user
            )
            user.groups.add(group)
            return redirect('login')

    context = {'form':form}
    return render(request, 'user/register.html', context)

@login_required(login_url='login')
@admin_only
def dashboardPage(request):
    personalInfo = UserInfo.objects.all()
    records = Record.objects.all()
    stayhomerecords = StayHomeRecord.objects.all()
    contacts = Contact.objects.all()
    context = {'info': personalInfo[:10], 'records':records[:10], 'stayhomerecords':stayhomerecords[:10], 'contacts':contacts[:10]}
    return render(request, 'user/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['normal_user'])
# @allowed_users(allowed_roles=['normal_user'])
def userPage(request):
    # info  = request.user.relate.objects.all()
    userInfo = UserInfo.objects.filter(relate=request.user)
    records = Record.objects.filter(user=request.user)
    stayHomeRecords = StayHomeRecord.objects.filter(user=userInfo[0].relate)
    context = {'info': userInfo[0], 'records': records, 'stayhomerecords': stayHomeRecords}
    return render(request, 'user/user.html', context)

@login_required(login_url='login')
def createRecord(request):
    form = RecordForm()
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('homepage')
        else:
            pass
    context = {'form':form}
    return render(request, 'user/create_record.html', context)

@login_required(login_url='login')
def deleteRecord(request, pk):
    record = Record.objects.get(id=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('homepage')
    context = {'record':record}
    return render(request, 'user/delete.html', context)

@login_required(login_url='login')
def updateInfo(request, pk):
    userInfo = UserInfo.objects.get(id=pk)
    form = UserInfoForm(instance=userInfo)

    if request.method == 'POST':
        form = UserInfoForm(request.POST, instance=userInfo)
        if form.is_valid():
            form.save()
            return redirect('homepage')
        else:
            print(form)

    context = {'form':form}
    return render(request, 'user/update_info.html', context)

@login_required(login_url='login')
def createStayHomeRecord(request, pk):
    form = StayHomeRecordForm()
    if request.method == 'POST':
        form = StayHomeRecordForm(request.POST)
        if form.is_valid():
            userInfo = UserInfo.objects.filter(relate=request.user)[0]
            obj = form.save(commit=False)
            obj.user = request.user
            obj.name = userInfo.name
            obj.phone = userInfo.phone
            obj.save()
            return redirect('homepage')
        else:
            pass
    context = {'form':form}
    return render(request, 'user/create_stayhomerecord.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createContactRecord(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
        else:
            return redirect('homepage')
    context = {'form':form}
    return render(request, 'user/create_contact.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteContactRecord(request, pk):
    record = Contact.objects.get(id=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('homepage')
    context = {'record':record}
    return render(request, 'user/delete_contact.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createStayHomeRecordAdmin(request):
    class StayHomeRecordFullForm(ModelForm):
        # user = models.ForeignKey(User)
        class Meta:
            model = Record
            fields =  '__all__'
    form = StayHomeRecordFullForm()
    if request.method == 'POST':
        form = StayHomeRecordFullForm(request.POST)
        if form.is_valid():
            print(request)
            userInfo = UserInfo.objects.filter(relate=form.cleaned_data['user'])[0]
            obj = form.save()
            return redirect('homepage')
        else:
            pass
    context = {'form':form}
    return render(request, 'user/create_stayhomerecord_admin.html', context)

def viewStayHomeRecord(request, pk):
    record = StayHomeRecord.objects.filter(id=pk)[0]
    print(record.name,record.phone,record.time_uploaded,record.location)
    context = {'stayhomerecord':record}
    return render(request, 'user/view_stayhomerecord.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['normal_user'])
def userImage(request, img):
    return None




################################################################################################
################################################################################################
######################################    Researcher   #########################################
################################################################################################
################################################################################################




given_k = 2

@login_required(login_url='login')
@allowed_users(allowed_roles=['researcher'])
def researcher_dashboard(request):
    return render(request, 'user/researcher_dashboard.html', {'data':list_cluster(request)})


def message_display_home(request, message):
    return render(request, 'user/message_display_home.html', context={'data': message})


def message_display_dashboard(request, message):
    return render(request, 'user/message_display_dashboard.html', context={'data': message})

def list_(request):
    if request.POST:
        age_min = request.POST['Age_minimal']
        age_max = request.POST['Age_maximal']
        location = request.POST['location']
        gender = request.POST['gender']
        test_result = request.POST['test_result']
        cluster_id = request.POST['cluster_id']
        # print("cluster:")
        # print(cluster_id)
        if cluster_id != "":
            return list_clu(request, cluster_id)
        elif age_max == "" and age_min == "" and location == "" and len(gender) != 1 and test_result == "":
            return list_all(request)
        elif (age_max != "" or age_min != "") and location == "" and len(gender) != 1 and test_result == "":
            return list_age(request, age_min, age_max, UserInfo.objects.all())
        elif (age_max != "" or age_min != "") and location != "" and len(gender) != 1 and test_result == "":
            return list_age(request, age_min, age_max, UserInfo.objects.filter(location=location))
        elif (age_max != "" or age_min != "") and location == "" and len(gender) == 1 and test_result == "":
            return list_age(request, age_min, age_max, UserInfo.objects.filter(gender=gender))
        elif (age_max != "" or age_min != "") and location == "" and len(gender) != 1 and test_result != "":
            return list_age(request, age_min, age_max, UserInfo.objects.filter(test_result=test_result))
        elif (age_max != "" or age_min != "") and location != "" and len(gender) != 1 and test_result == "":
            return list_age(request, age_min, age_max, UserInfo.objects.filter(location=location).filter(gender=gender))
        elif (age_max != "" or age_min != "") and location != "" and len(gender) != 1 and test_result != "":
            return list_age(request, age_min, age_max, UserInfo.objects.filter(location=location).filter(test_result=test_result))
        elif (age_max != "" or age_min != "") and location == "" and len(gender) == 1 and test_result != "":
            return list_age(request, age_min, age_max, UserInfo.objects.filter(test_result=test_result).filter(gender=gender))
        elif (age_max != "" or age_min != "") and location != "" and len(gender) == 1 and test_result != "":
            return list_age(request, age_min, age_max, UserInfo.objects.filter(location=location).filter(gender=gender).filter(test_result=test_result))
        elif age_max == "" and age_min == "" and location != "" and len(gender) != 1 and test_result == "":
            return list_loc(request, location, UserInfo.objects.all())
        elif age_max == "" and age_min == "" and location != "" and len(gender) != 1 and test_result != "":
            return list_loc(request, location, UserInfo.objects.filter(test_result=test_result))
        elif age_max == "" and age_min == "" and location != "" and len(gender) == 1 and test_result == "":
            return list_loc(request, location, UserInfo.objects.filter(gender=gender))
        elif age_max == "" and age_min == "" and location != "" and len(gender) == 1 and test_result != "":
            return list_loc(request, location, UserInfo.objects.filter(test_result=test_result).filter(gender=gender))
        elif age_max == "" and age_min == "" and location == "" and len(gender) == 1 and test_result == "":
            return list_gen(request, gender, UserInfo.objects.all())
        elif age_max == "" and age_min == "" and location == "" and len(gender) != 1 and test_result != "":
            return list_res(request, test_result, UserInfo.objects.all())
        elif age_max == "" and age_min == "" and location == "" and gender != "" and test_result != "":
            return list_gen(request, gender, UserInfo.objects.filter(test_result=test_result))
        else:
            return HttpResponse("Invalid request")

    return HttpResponse("Invalid request")


def list_all(request):
    persons = k_anonymity(request, UserInfo.objects.all())
    return export_csv(request, persons)


def list_clu(request, cluster_id):
    user_list = UserInfo.objects.filter(cluster_id=cluster_id)
    users = k_anonymity(request, user_list)
    total_num = count_total(request, cluster_id)
    total_infected_num = count_total_infected(request, cluster_id)
    per = total_infected_num/total_num * 100
    total_F = user_list.filter(gender="F").count()
    total_M = user_list.filter(gender="M").count()
    return render(request, 'user/cluster.html', context={'id': cluster_id, 'data': users, 'total_num': total_num,
                                                    'total_infected_num': total_infected_num, 'per': per,
                                                    'total_F': total_F, 'total_M': total_M})


def list_age(request, age_min, age_max, user_list):
    if age_min == "":
        persons = k_anonymity(request, user_list.filter(age__lte=age_max))
        return export_csv(request, persons)
    elif age_max == "":
        persons = k_anonymity(request, user_list.filter(age__gte=age_min))
        return export_csv(request, persons)
    else:
        filtered_users = user_list.filter(age__lte=age_max)
        persons = k_anonymity(request, filtered_users.filter(age__gte=age_min))
        return export_csv(request, persons)


def list_loc(request, location, user_list):
    persons = k_anonymity(request, user_list.filter(location=location))
    return export_csv(request, persons)


def list_res(request, test_result, user_list):
    persons = k_anonymity(request, user_list.filter(test_result=test_result))
    return export_csv(request, persons)


def list_gen(request, gender, user_list):
    persons = k_anonymity(request, user_list.filter(gender=gender))
    return export_csv(request, persons)


def read_csv(users):
    persons = []
    for p in users:
        u = K_User.objects.create(age=p.age, age_min=p.age, age_max=p.age, gender=p.gender, location=p.location,
                                  test_result=p.test_result,
                                  cluster_id=p.cluster_id
                                  )
        persons.append(u)
    return persons


def anonymize_age(persons, times):
    for p in persons:
        age_range = 5 * times
        # if times == 1:
        #     p.age = int(p.age/5)*5
        # elif times == 2:
        #     p.age = int(p.age/10)*10
        # elif times > 2:
        p.age_min = int(p.age / age_range) * age_range
        p.age_max = p.age_min + age_range
    return persons  # 返回列表型


def anonymize_loc(persons, times):
    for p in persons:
        val = times * (-1)
        p.location = p.location[:val] + "*" * times
        print(p.location)
    return persons  # 返回列表型


def anonymize_gender(persons):  # 泛化
    for p in persons:
        p.gender = '*'
    return persons  # 返回列表型


# def copy_persons(fresh_persons):  # 拷贝数据列表
#     persons = []
#     for p in fresh_persons:
#         u = UserInfo.objects.create(name=p.name, phone=p.phone, age=p.age, address=p.address, location=p.location,
#                                 test_result=p.test_result, encryption_keys=p.encryption_keys, personal_id=p.personal_id)
#         persons.append(u)
#     return persons


def group_persons(persons):  # 将数据分组，具体原理参考get_num
    grouped_persons = {}
    for p in persons:
        pseudo_parameters = str(p.age_min) + str(p.age_max) + str(p.location) + str(p.gender)
        if grouped_persons.get(pseudo_parameters) is None:
            grouped_persons[pseudo_parameters] = []
        grouped_persons[pseudo_parameters].append(p)
    print(grouped_persons)
    return grouped_persons  # 返回字典型，每个组以键值对的形式存储


def get_k(grouped_persons):  # 获得k值（传入字典型泛化结果）
    tmpDict = {}
    for group in grouped_persons:  # 遍历所有键值对
        tmpDict[group] = len(grouped_persons[group])  # 获得每个键对应值的个数
        # 即每个分组的包含的person个数
        # 以键(组标识)值(person个数)对存在字典tmpDict里
    k = None
    for group in tmpDict:  # 遍历tmpDict，取出最小的person个数，赋值给k
        if k is None or tmpDict[group] < k:
            k = tmpDict[group]
    if not k:
        k = 0
    return k  # 返回的k值即为泛化结果的k值


def export_csv(request, persons):

    return render(request, "user/list_all.html", context={"data": persons})


def get_num(persons, type):  # 获得数据某属性个数（具体属性由type决定）
    get_num_ = {}  # 一个字典（保存键值对）
    for p in persons:  # 遍历数据
        if type == 1:  # 年龄
            tmp_str = str(p.age_min) + str(p.age_max)  # 将某一个人的出生日期作为键tmp_str
        elif type == 2:  # 邮编
            tmp_str = str(p.location)  # 将某一个人的邮编作为键tmp_str
        elif type == 3:  # 性别
            tmp_str = str(p.gender)  # 将某一个人的邮编作为键tmp_str
        if get_num_.get(tmp_str) is None:  # 如果字典中没有此键
            get_num_[tmp_str] = []  # 增加以tmp_str为键，值为空的键值对
        get_num_[tmp_str].append(p)  # 将此人的数据加到tmp_str键所对的值中
    tmp_str = {}
    return len(get_num_)  # 返回了字典中键的个数（就是属性个数）


def max_num(age_num, loc_num, gender_num):
    if age_num >= loc_num and age_num >= gender_num:
        return 1
    elif loc_num >= age_num and loc_num >= gender_num:
        return 2
    elif gender_num >= age_num and gender_num >= loc_num:
        return 3


def k_anonymity(request, user_list):
    satisfying_combinations = []
    persons = read_csv(user_list)
    age_times = 0
    loc_times = 0
    i = 0
    K_User.objects.all().delete()
    # persons = copy_persons(fresh_persons)
    while True:
        i = i + 1
        if i > 1000:
            print(i)
            break
        grouped_persons = group_persons(persons)
        k = get_k(grouped_persons)
        print("get_K=" + str(k))
        if k >= given_k:
            satisfying_combinations.append(grouped_persons)
            break
        age_num = get_num(persons, 1)
        print("age_num=" + str(age_num))
        loc_num = get_num(persons, 2)
        print("loc_num=" + str(loc_num))
        gender_num = get_num(persons, 3)
        print("gen_num=" + str(gender_num))
        if age_num == 1 and loc_num == 1 and gender_num == 1:
            break
        m = max_num(age_num, loc_num, gender_num)
        if m == 1:
            age_times = age_times + 1
            print("age_times=" + str(age_times))
            persons = anonymize_age(persons, age_times)
        elif m == 2:
            loc_times = loc_times + 1
            print("any_loc")
            persons = anonymize_loc(persons, loc_times)
        elif m == 3:
            print("any_gen")
            persons = anonymize_gender(persons)

    if len(satisfying_combinations) > 0:
        return persons
    else:
        return HttpResponse("Failed.")


def list_cluster(request):
    users = UserInfo.objects.all()
    ids = []
    valid_ids = []
    for user in users:
        print(user.cluster_id)

        if user.cluster_id in ids or user.cluster_id == 0:
            print("already exist")
            continue
        else:
            ids.append(user.cluster_id)
            count = UserInfo.objects.filter(cluster_id=user.cluster_id).count()
            # if count >= given_k:
            # print("added")
            valid_ids.append(user.cluster_id)
    return valid_ids




def count_avg(request):
    if request.POST:
        location = request.POST['location']
        total_contact = 0
        person_no = 0
        data = UserInfo.objects.filter(location=location)
        for user in data:
            person_no = person_no + 1
            id = user.relate
            contact_data = Contact.objects.all()
            for contact in contact_data:
                if contact.user1 == id or contact.user2 == id:
                    total_contact = total_contact + 1
                    print(total_contact)

        if person_no == 0:
            return HttpResponse("Invalid location")

        else:
            avg = total_contact / person_no
            message = "The average number of contacts of all people living near " + str(location) + " is " + str(avg)
            return message_display_dashboard(request, message)

    else:
        return HttpResponse("Invalid request")


def count_avg_P(request):
    if request.POST:
        location = request.POST['location']
        total_contact = 0
        person_no = 0
        data = UserInfo.objects.filter(location=location)
        for user in data:
            person_no = person_no + 1
            id = user.phone
            contact_data = Contact.objects.all()
            for contact in contact_data:
                if contact.user1 == id or contact.user2 == id:
                    total_contact = total_contact + 1
                    print(total_contact)

        if person_no == 0:
            return HttpResponse("Invalid location")

        else:
            avg = total_contact / person_no
            message = "The average number of contacts of all people living near " + str(location) + " is " + str(avg)
            return message_display_dashboard(request, message)

    else:
        return HttpResponse("Invalid request")



def count_total(request, cluster_id):
    if request.POST:
        num = len(UserInfo.objects.filter(cluster_id=cluster_id))
        return num
    else:
        return HttpResponse("Invalid request")


def count_total_infected(request, cluster_id):
    if request.POST:
        num = len(UserInfo.objects.filter(cluster_id=cluster_id).filter(test_result="True"))
        return num
    else:
        return HttpResponse("Invalid request")

def add_user_page(request):
    if request.POST:
        return add_user(request)

    else:
        return HttpResponse("Invalid request")


def add_user(request):
    if request.POST:
        name = str(request.POST['name'])
        phone_no = str(request.POST['phone'])
        address = request.POST['address']
        gender = request.POST['gender']
        location = str(request.POST['location'])
        age = int(request.POST['age'])
        test_result = str(request.POST['test_result'])
        pw = request.POST['pw']

        UserInfo.objects.create(name=name, phone=phone_no, age=age, gender=gender, address=address, location=location,
                            test_result=test_result, encryption_keys=pw)
        return message_display_dashboard(request, "User has been added")

    else:
        return HttpResponse("Invalid request")


def count_total_P(request):
    if request.POST:
        location = str(request.POST['location'])
        user_list = UserInfo.objects.filter(location=location)
        P_num = user_list.filter(test_result="True").count()
        num = user_list.count()
        per = P_num / num * 100
        line1 = "The total number of people who has a POSITIVE test result is " + str(P_num) + ". "
        line2 = "And the percentage is " + str(per) + "%"
        lines = [line1, line2]
        response_content = '\r\n'.join(lines)
        return message_display_dashboard(request, response_content)
        # return HttpResponse(response_content, content_type="text/plain")
    else:
        return HttpResponse("Invalid request")

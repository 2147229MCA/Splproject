from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from .forms import *
from .models import *
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from allauth.account.decorators import login_required   

GR1 = 0
PC1 = 0
IP1 = 0
T1 = 0
M1 = 0
PER1 = 0
TM = 0
r1 = ""
pf1 = ""
N = ""
E = ""

def redirectUser(request):
    return(redirect("/"))
# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        print(request.POST)
        questions=QuesModel.objects.all()
        marks=0
        total=0
        GR=0
        PC=0
        IP=0
        r =""
        pf=""
        for q in questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            answer = request.POST.get(q.question) # Gets user’s choice, i.e the key of answer
             # Holds the value for choice
            x = q.ans
            # Compares actual answer with user’s choice
            if "Strongly Disagree" ==  answer:
                marks+=1
                if x == "GR":
                    GR+=1
                elif x =="PC":
                    PC+=1
                else:
                    IP+=1
            elif "Disagree" == answer:
                marks+=2
                if x == "GR":
                    GR+=2
                elif x =="PC":
                    PC+=2
                else:
                    IP+=2
            elif "Neutral" == answer:
                marks+=3
                if x == "GR":
                    GR+=3
                elif x =="PC":
                    PC+=3
                else:
                    IP+=3
            elif "Agree" == answer:
                marks+=4
                if x == "GR":
                    GR+=4
                elif x =="PC":
                    PC+=4
                else:
                    IP+=4
            else:
                marks+=5
                if x == "GR":
                    GR+=5
                elif x =="PC":
                    PC+=5
                else:
                    IP+=5
        global GR1,PC1,IP1,M1,T1,PER1,r1,pf1,TM,N,E
        GR1 = GR
        PC1 = PC
        IP1 = IP
        M1 = marks
        T1 = total    
        percent = marks/(total*5) *100
        PER1 = percent
        if(percent<30)and(percent>20):
            r ="Low Grit Level"
            pf="Suitable for Low Intensity Work Profiles"
        elif(percent>30) and (percent<50):
            r ="Lower Upper Grit Level"
            pf="Suitable for Lower Moderate Intensity Work Profiles"
        elif(percent>50)and(percent<70):
            r ="Medium Grit Level"
            pf ="Suitable for Moderate Intensity Work Profiles"
        elif(percent>70)and(percent<85):
            r ="High Grit Level"
            pf ="Suitable for Higher than Average Intensity Work Profiles"
        elif(percent<=20):
            r ="Extremely Low Grit Level"
            pf ="Suitable for Highly Low Intensity Work Profiles"
        else:
            r ="Extremely High Grit Level"
            pf ="Suitable for Extreme Intensity Work Profiles"
        r1 = r
        pf1 = pf
        TM = request.POST.get('timer')
        N = request.user
        E = request.user.email
        context = {
            'grade':r,
            'prof':pf,
            'marks':marks,
            'GR':GR,
            'IP':IP,
            'PC':PC,
            'time': request.POST.get('timer'),
            'percent':percent,
            'total':total
        }
        

        return render(request,'result.html',context)
    else:
        questions=QuesModel.objects.all()
        context = {
            'questions':questions
        }
        return render(request,'home.html',context)
def users_render_pdf_view(request):
    template_path = 'generate_pdf.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    global GR1,PC1,IP1,M1,T1,PER1,r1,pf1,TM,N,E
    context = {
            'grade':r1,
            'prof':pf1,
            'marks':M1,
            'GR':GR1,
            'IP':IP1,
            'PC':PC1,
            'time': TM,
            'Name':N,
            'Email':E,
            'percent':PER1,
            'total':T1
        }
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def addQuestion(request):    
    if request.user.is_staff:
        form=addQuestionform()
        if(request.method=='POST'):
            form=addQuestionform(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        context={'form':form}
        return render(request,'addQuestion.html',context)
    else: 
        return redirect('home') 

def signupPage(request):
    if request.user.is_authenticated:
        return redirect('home') 
    else: 
        form=createuserform()
        if request.method=='POST':
            form=createuserform(request.POST)
            if form.is_valid() :
                user=form.save()
                return redirect('login')
        context={
            'form':form,
        }
        return render(request,'signup.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
       context={}
       return render(request,'login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('/')


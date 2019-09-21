#A view function, or “view” for short, is simply a Python function that takes a web request 
#and returns a web response. This response can be the HTML contents of a Web page, or a redirect,
#or a 404 error, or an XML document, or an image, etc. Example: You use view to create web pages, 
#note that you need to associate a view to a URL to see it as a web page.

from django.views import View
from django.shortcuts import render, redirect
from .models import Job,Intern,Location,Category
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth.models import User
from .forms import Job_Post,Apply_Job,Location,Category
from .forms import NewUserForm1
from .forms import NewUserForm2,EditProfileForm

from django.contrib.auth.decorators import login_required



#view for homepage 
class homepage(View):
   def get(self,request):                                              
        return render(request=request,template_name="main/home.html",)

#view for student's profile
class student_profile(View):
    def get(self,request):                                                
        return render(request=request,template_name="main/StudentProfile.html",context={"intern":Job.objects.all()} )   


 #view for employer's profile
class employer_profile(View):
    def get(self,request):                                              
        return render(request=request,template_name="main/employer_profile.html",context={"jobs":Job.objects.all()})

#view to display the details of interns applied for the internship
class interns_applied(View):
    def get(self,request):
        return render(request=request,template_name="main/jobs_posted.html",context={"intern":Intern.objects.all()})

#view to display the jobs posted by the company
class jobs_list(View):
    def get(self,request):
        return render(request=request,template_name="main/jobs_list.html",context={"jobs":Job.objects.all()})                

# view for adding category
class add_category(View):
    form_class=Category
    initial={'key':'value'}
    template_name="main/category.html"

    def get(self,request):
        form=self.form_class(initial=self.initial)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
           cat= form.save(commit=False)
           cat.save()
           username = form.cleaned_data.get('category')                     #getting the username from the form   
           messages.success(request, f"New Category {username} created")
           return redirect("main:employer")   

        else:                                                 #if form is not valid or not filled properly               
            for msg in form.error_messages:                   
                messages.error(request, f"{msg}: {form.error_messages[msg]}")   #displaying the error messages
            form=self.form_class(initial=self.initial)
            return render(request ,self.template_name,{'form':form})



# view for adding location
class add_location(View):
    form_class=Location
    initial={'key':'value'}
    template_name="main/location.html"
    
    def get(self,request):
        form=self.form_class(initial=self.initial)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
           loc= form.save(commit=False)
           loc.save()
           username = form.cleaned_data.get('location')                     #getting the username from the form   
           messages.success(request, f"New Location {username} created")
           return redirect("main:employer")
        else:
            for msg in form.error_messages:                   
                messages.error(request, f"{msg}: {form.error_messages[msg]}")   #displaying the error messages

            form=self.form_class(initial=self.initial)
            return render(request ,self.template_name,{'form':form})



# view for applying for job 
class apply_for_job(View):
    form_class=Apply_Job
    initial={'key':'value'}
    template_name="main/apply_for_job.html"

    def get(self,request):
        form=self.form_class(initial=self.initial)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            intern_profile= form.save(commit=False)
            
            intern_profile.username=request.user
            intern_profile.save()
            #username = form.cleaned_data.get('intern_profile.username')                     #getting the username from the form   
            messages.success(request, f"{intern_profile.username} has succesully applied for this job")

            return redirect("main:student")
        else:                                                 #if form is not valid or not filled properly               
            for msg in form.error_messages:                   
                messages.error(request, f"{msg}: {form.error_messages[msg]}")   #displaying the error messages

            form=self.form_class(initial=self.initial)
            return render(request ,self.template_name,{'form':form})


# view for posting a job
class post_a_job(View):
    form_class=Job_Post
    initial={'key':'value'}
    template_name="main/post_job.html"

    def get(self,request):
        form=self.form_class(initial=self.initial)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():                                                     #if the form filled is valid
            job_profile = form.save(commit=False)  
            job_profile.username=request.user  
            job_profile.save()                                       #basically save the user(since user is a part of form,thus we save the form)
            username = form.cleaned_data.get('job_title')                     #getting the username from the form   
            messages.success(request, f"New Job created: {username}")    #displaying the message that new account has been created
            
            # now after signing up we automatically logs in the user 
            # login(request, user)                                             #login(HttpResponse,User)
            return redirect("main:employer")
        
        else:                                                 #if form is not valid or not filled properly               
            for msg in form.error_messages:                   
                messages.error(request, f"{msg}: {form.error_messages[msg]}")   #displaying the error messages

            form=self.form_class(initial=self.initial)
            return render(request ,self.template_name,{'form':form})

# view for signup page of employer
class register_as_employer(View):
    form_class=NewUserForm1
    initial={'key':'value'}
    template_name="main/Employer-Signup.html"

    def get(self,request):
        form=self.form_class(initial=self.initial)
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():                                                     #if the form filled is valid
            user = form.save()                                           #basically save the user(since user is a part of form,thus we save the form)
            username = form.cleaned_data.get('username')                     #getting the username from the form   
            messages.success(request, f"New account created: {username}")    #displaying the message that new account has been created
            
            # now after signing up we automatically logs in the user 
            login(request, user)                                             #login(HttpResponse,User)
            if user.is_student:
                return redirect("main:student")
            else:
                return redirect("main:employer")  
        
        else:                                                 #if form is not valid or not filled properly               
            for msg in form.error_messages:                   
                messages.error(request, f"{msg}: {form.error_messages[msg]}")   #displaying the error messages

            form=self.form_class(initial=self.initial)
            return render(request ,self.template_name,{'form':form})


# view for signup page of student
class register_as_student(View):
    form_class=NewUserForm2
    initial={'key':'value'}
    template_name="main/Student-Signup.html"

    def get(self,request):
        form=self.form_class(initial=self.initial)
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            if user.is_student:
                return redirect("main:student")
            else:
                return redirect("main:employer")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            form=self.form_class(initial=self.initial)
            return render(request ,self.template_name,{'form':form})



#function for logging the user out of the current session
class logout_request(View):
    def get(self,request):
       logout(request)
       messages.info(request, "Logged out successfully!")
       return redirect("main:homepage") 


class login_request(View):
    form_class=AuthenticationForm
    initial={'key':'value'}
    template_name="main/login.html"

    def get(self,request):
        form=self.form_class(initial=self.initial)
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form=self.form_class(request=request,data=request.POST)
        if form.is_valid():                                                  #if the form is valid
            username = form.cleaned_data.get('username')                     #saving the username form the form
            password = form.cleaned_data.get('password')                     #saving the password from the form
            user = authenticate(username=username, password=password)        #authenticating the user i.e. username and passwords match simultaneously with a user's profile in database
            if user is not None:                                             #basically means "if user is true i.e. if user is successfully authenticated"
                login(request, user)                                         #log the user into the session
                messages.info(request, f"You are now logged in as {username}")    #display a message that user is logged in
                if user.is_student:
                  return redirect("main:student")
                else:
                  return redirect("main:employer")                               
            else:                                                            #if it fails to authenticate
                messages.error(request, "Invalid username or password.")     #display an error message
                form=self.form_class(initial=self.initial)
                return render(request ,self.template_name,{'form':form})
        
        else:                                                                #if the form is not valid
            messages.error(request, "Invalid username or password.")         #display the error message
            
            form=self.form_class(initial=self.initial)
            return render(request ,self.template_name,{'form':form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('main:view_profile'))
        else:
            return redirect(reverse('main:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'main/change_password.html', args)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return view_profile(request)
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'main/edit_profile.html', args)

def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'main/home.html', args)
                         
                                        
 
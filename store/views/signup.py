from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

from store.models.customer import Customer
from django.views import View

# print(make_password('1234'))
# print(check_password('1234', 'pbkdf2_sha256$320000$SgMApGmytrRiidet4qZWH4$+dm2t57UkJ4V/PYhfAWekFJniuAopHf0PK/Dn4zc32g='))
# True


# Create your views here.

class Signup(View):
    # print(request.method)
    def get(self, request):
        return render(request,'signup.html')
    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        # validation
        value = {'first_name':first_name,'last_name':last_name,'phone':phone,'email':email}

        error_message = None

        customer = Customer(first_name=first_name,last_name=last_name,phone=phone,email=email,password=password)

        error_message = self.validateCustomer(customer)
        # saving
        if not error_message:
            # customer = Customer(first_name=first_name,last_name=last_name,phone=phone,email=email,password=password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data  = {'error':error_message, 'values':value}
            return render(request,'signup.html',data)
        # return HttpResponse('success')
        # return HttpResponse('request.POST') middleware "request.POST.get('email')""

    def validateCustomer(self, customer):
        error_message = None
        if(not customer.first_name):
            error_message = "First Name Required!!!"
        elif len(customer.first_name)<4:
            error_message = "First Name must be 4 character long or more"

        elif not customer.last_name:
            error_message = "Last Name Required!!!"
        elif len(customer.last_name)<4:
            error_message = "Last Name must be 4 character long or more"

        elif not customer.phone:
            error_message = "Phone Number Required!!!"
        elif len(customer.phone) <10:
            error_message = "Phone Number must be 10 character long"
    
        elif len(customer.email)<5:
            error_message = "Email must be 5 character long"
         
        elif len(customer.password)<6:
            error_message = "Password must be 6 character long"

        elif customer.isExists():
            error_message = 'Email Address Already Registered...'

        return error_message

    


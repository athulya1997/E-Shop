from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models.product import Product
from .models.category import Category
from .models.customer import Customer

# print(make_password('1234'))
# print(check_password('1234', 'pbkdf2_sha256$320000$SgMApGmytrRiidet4qZWH4$+dm2t57UkJ4V/PYhfAWekFJniuAopHf0PK/Dn4zc32g='))
# True


# Create your views here.
def index(request):
    products = None
    categories = Category.get_all_categories()
    # print(products)
    # print(request.GET)
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products();
    data = {}
    data['products'] = products
    data['categories'] = categories
    return render(request,'index.html', data)

def validateCustomer(customer):
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

# def registerUser(request):

def signup(request):
    # print(request.method)
    if request.method == 'GET':
        return render(request,'signup.html')
    else:
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

        error_message = validateCustomer(customer)
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

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                return redirect('homepage')
            else:
                error_message  = "Email or Password Invalid!!!"
        else:
            error_message  = "Email or Password Invalid!!!!!!!"
        return render (request,'login.html',{'error':error_message})

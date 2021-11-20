from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http.response import HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from admin_portal.models import *


def index(request):
    return HttpResponse("Hello, world. You're at the Cashier index.")

def registeration(request):
    if request.method == "POST":
        username = request.POST['user_name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = make_password(request.POST['password'], None, 'md5')
        confirm_password = request.POST['confirm_password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username Already Exists')
            return render(request, 'cashier/registeration.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Exists')
            return render(request, 'cashier/registeration.html')
        if  check_password(password, confirm_password):
            messages.error(request, 'Password and Confirm Password is not matching')
            return render(request, 'cashier/registeration.html')
        if len(password)<6:
            messages.error(request, 'Password must be greater than 6 characters')
            return render(request, 'cashier/registeration.html')
        cashier = User(username=username,first_name=first_name,last_name=last_name,email=email,password=password,is_staff=True)
        cashier.save()
        return redirect('login')
    return render(request, 'cashier/registeration.html')

# ------------------Services--------------------- #

@login_required
def c_show_services(request):
    services = Service.objects.filter(status=True)
    return render(request,'cashier/c_show_services.html',{'services':services})
    
@login_required
def c_add_service(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        rate = request.POST['rate']
        service = Service(name=name,description=description,rate=rate)
        service.save()
        messages.success(request, 'Successfully Added the Service')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'cashier/c_add_service.html')
    
@login_required
def c_update_service(request,pk):
    service=Service.objects.filter(id=pk).first()
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        rate = request.POST['rate']
        service.name = name
        service.description = description
        service.rate = rate
        service.save()
        messages.success(request,"Service Updated Successfully !!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'cashier/c_update_service.html',{'service':service})
    
#------------------ Products ---------------------#

@login_required
def c_show_products(request):
    products = Product.objects.filter(status=True)
    return render(request,'cashier/c_show_products.html',{'products':products})


@login_required
def c_add_product(request):
    if request.method == "POST":
        name = request.POST['name']
        brand = request.POST['brand']
        sale_rate = request.POST['sale_rate']
        purchase_rate = request.POST['purchase_rate']
        product = Product(name=name,brand=brand,sale_rate=sale_rate,purchase_rate=purchase_rate)
        product.save()
        stock = Stock(product_id=product.id,quantity=0)
        stock.save()
        stockoutlog = StockOutLog(product_id=product.id,quantity=0)
        stockoutlog.save()
        messages.success(request, 'Successfully Added the Product')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'cashier/c_add_product.html')
    
@login_required
def c_update_product(request,pk):
    product=Product.objects.filter(id=pk).first()
    if request.method == "POST":
        name = request.POST['name']
        brand = request.POST['brand']
        sale_rate = request.POST['sale_rate']
        purchase_rate = request.POST['purchase_rate']
        product.name = name
        product.brand = brand
        product.sale_rate = sale_rate
        product.purchase_rate = purchase_rate
        product.save()
        messages.success(request,"Product Updated Successfully !!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'cashier/c_update_product.html',{'product':product})

#------------------ Persons ---------------------#

@login_required
def c_show_persons(request):
    persons = Person.objects.filter(status=True)
    return render(request,'cashier/c_show_persons.html',{'persons':persons})
   
@login_required
def c_add_person(request):
    if request.method == "POST":
        name = request.POST['name']
        contact = request.POST['contact']
        address = request.POST['address']
        type = request.POST['type']
        person = Person(name=name,contact=contact,address=address,type=type)
        person.save()
        messages.success(request, 'Successfully Added the Person')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'cashier/c_add_person.html')

@login_required
def c_update_person(request,pk):
    person=Person.objects.filter(id=pk).first()
    if request.method == "POST":
        name = request.POST['name']
        contact = request.POST['contact']
        address = request.POST['address']
        type = request.POST['type']
        person.name = name
        person.contact = contact
        person.address = address
        person.type = type
        person.save()
        messages.success(request,"Person Updated Successfully !!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'cashier/c_update_person.html',{'person':person})

#------------------ Purchase ---------------------#

@login_required
def c_show_purchases(request):
    purchases = Purchase.objects.filter(status=True)
    return render(request,'cashier/c_show_purchases.html',{'purchases':purchases})


@csrf_exempt
@login_required
@transaction.atomic
def c_add_purchase(request):
    products = Product.objects.all()
    persons = Person.objects.filter(type=0)
    if request.method == 'POST':
        try:
            total_amount = request.POST.get('total_price')
            paid_amount = request.POST.get('cash')
            date = request.POST.get('purcahse_date')
            person_id = request.POST.get('supplier')
            products = request.POST.getlist('products[]')
            rate = request.POST.getlist('rate[]')
            quantity = request.POST.getlist('qty[]')
            # return JsonResponse({'body': request.POST}, safe=False)
            purchase = Purchase(total_amount=total_amount,paid_amount=paid_amount ,date=date ,person_id=person_id,status=True)
            purchase.save()
            payment = Payment(credit=total_amount,debit=0,date=date,type='vendor',description='cash in',purchase_id=purchase.pk,person_id=person_id)
            payment.save()
            payment2 = Payment(credit=0,debit=paid_amount,date=date,type='vendor',description='cash out',purchase_id=purchase.pk,person_id=person_id)
            payment2.save()
            counter = 0
            for product in products:
                purhcase_detail = PurchaseDetails(purchase_id=purchase.pk, product_id=product, quantity=quantity[counter], rate=rate[counter])
                purhcase_detail.save()
                stock = Stock.objects.filter(product_id=product).first()
                if stock:
                    stock.quantity+=int(quantity[counter])
                    stock.save()
                    stockoutlog = StockOutLog(type='stock in',product_id=product,quantity=int(quantity[counter]))
                    stockoutlog.save()
                else:
                    messages.error(request,"Firstly Add the Product in Database" )
                    return redirect('c_add_purchase')
                counter += 1
                
            messages.success(request, 'Successfully Added the Purchase')
            return JsonResponse({'error': False, 'success_msg': 'Added Successfully'})
        except Exception as e:
            return JsonResponse({'error': True, 'error_msg': str(e)})
    else:
        return render(request,'cashier/c_add_purchase.html',{'products':products,'persons':persons})
    
def load_product_by_id(request):
    product_id = request.GET.get('product')
    products = Product.objects.filter(id=product_id).first()
    return HttpResponse(products.purchase_rate)

# ----------------- Sales -----------------------#

@login_required
def c_show_sales(request):
    sales = Sale.objects.all()
    return render(request, 'cashier/c_show_sales.html',{'sales':sales})
    
@login_required
@csrf_exempt
@transaction.atomic
def c_add_sale(request):
    products = Product.objects.all()
    services = Service.objects.all()
    persons = Person.objects.filter(type=1)
    if request.method == 'POST':
        try:
            phone_no = request.POST.get('phone_no')
            vehicle_name = request.POST.get('vehicle_name')
            vehicle_model = request.POST.get('vehicle_model')
            vehicle_no = request.POST.get('vehicle_no')
            maintenance_cost = request.POST.get('maintenance_cost')
            sale_amount = request.POST.get('sale_amount')
            total_amount = request.POST.get('total_price')
            discount = request.POST.get('discount')
            final_amount = request.POST.get('net_amount')
            paid = request.POST.get('cash') 
            person_name = request.POST.get('person_name', None)
            products = request.POST.getlist('products[]',None)
            services = request.POST.getlist('services[]',None)
            rate = request.POST.getlist('rate[]')
            quantity = request.POST.getlist('qty[]')
            total_product_price = request.POST.getlist('total_product_price[]')
            srate = request.POST.getlist('srate[]')
            squantity = request.POST.getlist('sqty[]')
            stotal_product_price = request.POST.getlist('stotal_product_price[]')
            # return JsonResponse({'body': request.POST}, safe=False)
            sale = Sale(discount=discount, maintenance_cost=maintenance_cost, sale_amount=sale_amount, total_amount=total_amount,  final_amount=final_amount,phone_no=phone_no,vehicle_name=vehicle_name,vehicle_model=vehicle_model,vehicle_no=vehicle_no,customer_name=person_name, paid=paid,status=True,type='sale',description='customer')
            sale.save()
            payment1 = Payment(credit=0,debit=final_amount,date=sale.date,type='walking',description='sale cash out',sale_id=sale.pk, customer_name=person_name)
            payment2 = Payment(credit=paid,debit=0,date=sale.date,type='walking',description='sale cash in',sale_id=sale.pk, customer_name=person_name)
            payment1.save()
            payment2.save()
            
            counter =  0
            for product in products:
                sale_detail_products = SaleDetails(sale_id=sale.pk, product_id=product, quantity=quantity[counter], rate=rate[counter])
                sale_detail_products.save()
                stock = Stock.objects.filter(product_id=product).first()
                stockoutlog = StockOutLog.objects.filter(product_id=product).first()
                if stock:
                    stock.quantity-=int(quantity[counter])
                    stock.save()
                    stockoutlog = StockOutLog(type='stock out',product_id=product,quantity=int(quantity[counter]))
                    stockoutlog.save()
                else:
                    messages.error(request,"Firstly Add the Product in Database" )
                    return redirect('c_add_sale')
                counter += 1
                
            counter =  0
            for service in services:
                sale_detail_services = SaleDetails(sale_id=sale.pk, service_id=service, quantity=squantity[counter], rate=srate[counter])
                sale_detail_services.save()
                counter += 1
                
                
            messages.success(request, 'Successfully Added the Sale')
            return JsonResponse({'error': False, 'success_msg': 'added the sale', 'sale_id': sale.pk})
            # return render(request,'admin_portal/invoice.html',{'saledetails':saledetails})
            # return redirect('invoice')
        except Exception as e:
            return JsonResponse({'error': True, 'error_msg': str(e)})
    else:
        return render(request, 'cashier/c_add_sale.html',{'products':products,'services':services,'persons':persons})

@csrf_exempt
def invoice(request, sale_id):
    sale = Sale.objects.get(id=sale_id)
    saleDetails = sale.sale.all()
    # return JsonResponse({'sale': json.loads(serialize('json', sale.sale.all() ))})
    # saledetails = SaleDetails.objects.filter(sale_id=sale.id) 
    return render(request,'cashier/invoice.html', {'sale': sale, 'details': saleDetails})  

def load_products_price(request):
    product_id = request.GET.get('product')
    products = Product.objects.filter(id=product_id).first()
    return HttpResponse(products.sale_rate)

def load_products_quantity(request):
    product_id = request.GET.get('product')
    products = Product.objects.filter(id=product_id).first()
    stock = Stock.objects.filter(id=products.id).first()
    return HttpResponse(stock.quantity)

def load_service_price(request):
    service_id = request.GET.get('service')
    service = Service.objects.filter(id=service_id).first()
    return HttpResponse(service.rate)


import json
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponseRedirect,JsonResponse
from admin_portal.models import *
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction




def index(request):
    return HttpResponse("Hello, world. You're at the Admin Portal index.")

def master(request):
    return render(request, 'includes/master.html')

#------------------ Authentication ---------------------#

def login(request):
    if request.method == "POST":
        user_name = request.POST['user_name']
        password = request.POST['password']
        user= auth.authenticate(username=user_name, password=password)
        if user is not None:
            if user.is_superuser:
                auth.login(request, user)
                return redirect('show_services')
            else:
                messages.error(request, 'Admin does not exist with this user name')
                return redirect('login')
        else:
            messages.error(request, 'INVALID CREDENTIALS')
            return redirect('login')
    else:
        return render(request, 'admin_portal/login.html')

@login_required  
def logout(request):
    auth.logout(request)
    return redirect('login')

#------------------ Services ---------------------#

@login_required
def show_services(request):
    if request.user.is_superuser:
        services = Service.objects.filter(status=True)
        return render(request,'admin_portal/show_services.html',{'services':services})
    else:
        return HttpResponse('Not accessible')

@login_required
def add_service(request):
    if request.user.is_superuser:
        if request.method == "POST":
            name = request.POST['name']
            description = request.POST['description']
            rate = request.POST['rate']
            service = Service(name=name,description=description,rate=rate)
            service.save()
            messages.success(request, 'Successfully Added the Service')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'admin_portal/add_service.html')
    else:
        return HttpResponse('Not accessible')
    
@login_required
def update_service(request,pk):
    if request.user.is_superuser:
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
        return render(request, 'admin_portal/update_service.html',{'service':service})
    else:
        return HttpResponse('Not accessible')
    
@login_required
def del_service(request,pk):
    service=Service.objects.filter(id=pk).first()
    service.status=False
    service.save()
    messages.success(request,"Service Deleted Successfully!!")
    return redirect('show_services')

#------------------ Products ---------------------#

@login_required
def show_products(request):
    if request.user.is_superuser:
        products = Product.objects.filter(status=True)
        return render(request,'admin_portal/show_products.html',{'products':products})
    else:
        return HttpResponse('Not accessible')

@login_required
def add_product(request):
    if request.user.is_superuser:
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
        return render(request, 'admin_portal/add_product.html')
    else:
        return HttpResponse('Not accessible')
    
@login_required
def update_product(request,pk):
    if request.user.is_superuser:
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
        return render(request, 'admin_portal/update_product.html',{'product':product})
    else:
        return HttpResponse('Not accessible')
    
@login_required
def del_product(request,pk):
    product=Product.objects.filter(id=pk).first()
    product.status=False
    product.save()
    messages.success(request,"Product Deleted Successfully!!")
    return redirect('show_products')

#------------------ Persons ---------------------#

@login_required
def show_persons(request):
    if request.user.is_superuser:
        persons = Person.objects.filter(status=True)
        return render(request,'admin_portal/show_persons.html',{'persons':persons})
    else:
        return HttpResponse('Not accessible')

@login_required
def add_person(request):
    if request.user.is_superuser:
        if request.method == "POST":
            name = request.POST['name']
            contact = request.POST['contact']
            address = request.POST['address']
            type = request.POST['type']
            person = Person(name=name,contact=contact,address=address,type=type)
            person.save()
            messages.success(request, 'Successfully Added the Person')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'admin_portal/add_person.html')
    else:
        return HttpResponse('Not accessible')
    
@login_required
def update_person(request,pk):
    if request.user.is_superuser:
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
        return render(request, 'admin_portal/update_person.html',{'person':person})
    else:
        return HttpResponse('Not accessible')
    
#------------------ Purchase ---------------------#

@login_required
def show_purchases(request):
    if request.user.is_superuser:
        purchases = Purchase.objects.filter(status=True)
        return render(request,'admin_portal/show_purchases.html',{'purchases':purchases})
    else:
        return HttpResponse('Not accessible')

@csrf_exempt
@login_required
@transaction.atomic
def add_purchase(request):
    if request.user.is_superuser:
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
                    else:
                        messages.error(request,"Firstly Add the Product in Database" )
                        return redirect('add_purchase')
                    counter += 1
                    
                messages.success(request, 'Successfully Added the Purchase')
                return JsonResponse({'error': False, 'success_msg': 'Added Successfully'})
            except Exception as e:
                return JsonResponse({'error': True, 'error_msg': str(e)})
        else:
            return render(request,'admin_portal/add_purchase.html',{'products':products,'persons':persons})
    else:
        return HttpResponse('Not accessible')
    
def load_product_by_id(request):
    product_id = request.GET.get('product')
    products = Product.objects.filter(id=product_id).first()
    return HttpResponse(products.purchase_rate)

@login_required
def show_sales(request):
    sales = Sale.objects.all()
    return render(request, 'admin_portal/show_sales.html',{'sales':sales})
    
@login_required
@csrf_exempt
@transaction.atomic
def add_sale(request):
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
                    stockoutlog.quantity+=int(quantity[counter])
                    stockoutlog.save()
                else:
                    messages.error(request,"Firstly Add the Product in Database" )
                    return redirect('add_sale')
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
        return render(request, 'admin_portal/add_sale.html',{'products':products,'services':services,'persons':persons})

from django.core.serializers import serialize

@csrf_exempt
def invoice(request, sale_id):
    sale = Sale.objects.get(id=sale_id)
    saleDetails = sale.sale.all()
    # return JsonResponse({'sale': json.loads(serialize('json', sale.sale.all() ))})
    # saledetails = SaleDetails.objects.filter(sale_id=sale.id) 
    return render(request,'admin_portal/invoice.html', {'sale': sale, 'details': saleDetails})  



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

@login_required
def show_ledger(request):
    payments = Payment.objects.all()
    return render(request, 'admin_portal/show_ledger.html',{'payments':payments})
  
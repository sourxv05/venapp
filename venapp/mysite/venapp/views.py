from django.contrib import auth, messages
from django.db.models import ExpressionWrapper, F, DurationField
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect,get_object_or_404


from django.db.models import Avg



from .models import profile, PurchaseOrder








def index1(request):

     return render(request,'index1.html')



def index(request):
#add vendor
   if request.method=='POST':
        name=request.POST.get('name','')
        address=request.POST.get('address','')
        phone=request.POST.get('phone','')
        email=request.POST.get('email','')
        code=request.POST.get('code','')
        t1=profile(name=name,address=address,phone=phone,email=email,code=code)
        t1.save()
        return redirect('/list/')
   return render(request,'index.html')


def list(request):

    v1=profile.objects.all()
    context={                                    #profile
        'v_list':v1
    }
    return render(request,'details.html',context)

def details(request,v_id):
    detail=profile.objects.get(id=v_id)
    return render(request,'profile.html',{'detail':detail})    #profile detail



def delete(request,id):
    if request.method=='POST':
        v2=profile.objects.get(id=id)
        v2.delete()                                   #delete profile
        return redirect('/list/')
    return render(request,'delete.html')


# def edit(request,id):
#     v1=profile.objects.get(id=id)
#     form=profileform(request.POST or None, request.FILES,instance=v1)
#     if form.is_valid():
#         form.save()
#         return redirect('/')
#     return render(request,'edit.html',{'form':form,'v1':v1})
# views.py



def edit(request, id):

    instance = get_object_or_404(profile, id=id)

    if request.method == 'POST':

        instance.name = request.POST.get('name')
        instance.address = request.POST.get('address')
        instance.phone = request.POST.get('phone')
        instance.email = request.POST.get('email')

        instance.save()


        return redirect("/list/")

    return render(request, 'edit.html', {'instance': instance})



#add purchse order

def po(request):
    vendors = profile.objects.all()  # Rename 'vender' to 'vendors' for clarity

    if request.method == 'POST':
        po_number = request.POST.get('po_number', '')
        vendor_id = request.POST.get('vendor', '')  # Assuming 'vendor' is the name of the select input in your HTML form
        # order_date = request.POST.get('order_date', '')
        # delivery_date = request.POST.get('delivery_date', '')
        items = request.POST.get('items', '')
        quantitye = request.POST.get('quantitye', '')
        status = request.POST.get('status', '')
        quality_rating = request.POST.get('quality_rating', '')
        issue_date = request.POST.get('issue_date', '')
        acknowledgment_date = request.POST.get('acknowledgment_date', '')
        od = request.POST.get('od', '')
        dd = request.POST.get('dd', '')

        # Retrieve the selected vendor profile instance
        vendor_instance = get_object_or_404(profile, id=vendor_id)

        # Create the PurchaseOrder instance with vendor_instance as vendor and name
        p1 = PurchaseOrder(
            po_number=po_number,
            vendor=vendor_instance,
            # name=vendor_instance,  # Assigning the vendor instance to the name field
            # order_date=order_date,
            # delivery_date=delivery_date,
            items=items,
            quantitye=quantitye,
            status=status,
            quality_rating=quality_rating,
            issue_date=issue_date,
            acknowledgment_date=acknowledgment_date,
            od=od,
            dd=dd
        )
        p1.save()
        return redirect('/list_orders/')

    return render(request, 'order.html', {'vendors': vendors})







def list_orders(request):
    vendor_id = request.GET.get('vendor')  # Query parameter for vendor ID

    if vendor_id:  # If a vendor ID is provided, filter by that vendor
        purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
    else:  # Otherwise, retrieve all purchase orders
        purchase_orders = PurchaseOrder.objects.all()

    # Retrieve all vendors for a potential dropdown filter in the template
    vendors = profile.objects.all()

    return render(
        request,
        'orderlist.html',
        {
            'purchase_orders': purchase_orders,
            'vendors': vendors,
            'selected_vendor': vendor_id  # To maintain selected filter in the template
        }
    )




def orderdetail(request,od_id):
    od=PurchaseOrder.objects.get(id=od_id)
    return render(request,'orderdetail.html',{'od':od})





def updateorder(request,id):

    update = get_object_or_404(PurchaseOrder, id=id)
    vendors = profile.objects.all()
    if request.method == 'POST':

        update.po_number = request.POST.get('po_number')
        # update.vendor = request.POST.get('vendor')
        update.order_date = request.POST.get('order_date')
        update.delivery_date = request.POST.get('delivery_date')
        update.items = request.POST.get('items')
        update.quantitye = request.POST.get('quantitye')
        update.status = request.POST.get('status')
        update.quality_rating = request.POST.get('quality_rating')
        update.issue_date = request.POST.get('issue_date')
        update.acknowledgment_date = request.POST.get('acknowledgment_date')

        update.save()


        return redirect("/list_orders/")

    return render(request, 'update.html', {'update': update,'vendors':vendors})





def delete_order(request,id):
    if request.method=='POST':
        delete=PurchaseOrder.objects.get(id=id)
        delete.delete()                                   #delete profile
        return redirect('/list_orders/')
    return render(request,'delete_order.html')

def performance(request):
    vendor_id = request.GET.get('vendor')  # Query parameter for vendor ID

    if vendor_id:  # If a vendor ID is provided, filter by that vendor
        purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
    else:  # Otherwise, retrieve all purchase orders
        purchase_orders = PurchaseOrder.objects.all()

    # Retrieve all vendors for a potential dropdown filter in the template
    vendors = profile.objects.all()

    return render(
        request,
        'orderlist.html',
        {
            'purchase_orders': purchase_orders,
            'vendors': vendors,
            'selected_vendor': vendor_id  # To maintain selected filter in the template
        }
    )






def on_time_delivery_rate_view(request, vendor_id):
    # Fetch the vendor and completed purchase orders
  vendor = profile.objects.get(id=vendor_id)
  completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')

  completed_pos_with_rating= PurchaseOrder.objects.filter(vendor=vendor,    status='completed',quality_rating__isnull=False) # Only consider POs with a quality rating



        #on_time_delivery_rate
  if completed_pos.exists():


     on_time_pos = completed_pos.filter(acknowledgment_date__lte =F ('dd'))
     try:
        on_time_rate = on_time_pos.count() / completed_pos.count()
     except ZeroDivisionError:
        on_time_rate = None
  else:
        on_time_rate = None  # No completed POs



        #quality_rating_avg


  total_po=PurchaseOrder.objects.filter(vendor=vendor)
  if completed_pos_with_rating.exists():
      quality_rating_avg = completed_pos_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg']

  else: quality_rating_avg = None


  # Fulfilment Rate:
  try:
        Fulfilment_Rate=completed_pos.count()/total_po.count()
  except ZeroDivisionError:
        Fulfilment_Rate = None




                              # Average Response Time:

  time_differences = PurchaseOrder.objects.annotate(
    acknowledgment_time_difference=ExpressionWrapper(
        F('acknowledgment_date') - F('issue_date'),  # Compute time difference
        output_field=DurationField()  # Define it as a duration
    )
    )
  pos_with_acknowledgment = time_differences.filter(vendor=vendor,acknowledgment_date__isnull=False)

  avg_acknowledgment_time = pos_with_acknowledgment.aggregate(
    Avg('acknowledgment_time_difference'))['acknowledgment_time_difference__avg']



  context = {
        'vendor': vendor,
        'on_time_delivery_rate':  on_time_rate,
        'avg_quality_rating':quality_rating_avg,
        'fulfilment':Fulfilment_Rate,
        'avg_acknowledgment':avg_acknowledgment_time,

       }

  return render(request, 'eva.html', context)

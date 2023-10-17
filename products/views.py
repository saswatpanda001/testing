from django.shortcuts import redirect, render
from products.forms import product_form, prod_comm, order_search, sales_search
from products.models import Product_Model, cart_model, product_comment, order_model, sales_list,wishlist,featured
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DeleteView, CreateView
from django.utils.decorators import method_decorator
from django.urls.base import reverse_lazy
from django.db.models import Q


@method_decorator(login_required, name='dispatch')
class create_product(CreateView):
    model = Product_Model
    fields = ("name", "image", "price", "bio")
    template_name = "products_form.html"
    context_object_name = "form"
    success_url = reverse_lazy('products:home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
def product_view(request):
    x = Product_Model.objects.filter(author=request.user).order_by("-created")

    if request.GET.get("query") != None:
        search_data = Product_Model.objects.filter(
            Q(name__icontains=request.GET.get("query")))
        search_data = search_data.filter(
            author=request.user).order_by("-created")

        return render(request, "search_product.html", {"data_sr": search_data, "search": "Search Products"})

    return render(request, "productlist.html", {"data": x, "search": "Search Products"})


@method_decorator(login_required, name='dispatch')
class product_updateview(UpdateView):
    model = Product_Model
    fields = ("name", "image", "price", "bio")
    template_name = "pr_update.html"
    context_object_name = "form"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy('products:home')


@method_decorator(login_required, name='dispatch')
class product_deleteview(DeleteView):
    model = Product_Model
    template_name = "pr_delete.html"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy('products:home')


@login_required
def prod_list(request):
    print(request.POST)
    notifications = ""
    if request.method=="POST" and "wishlist_button" in request.POST:
        print(request.POST)
        prd_id = request.POST["wishlist_button"]
        prd_model = Product_Model.objects.filter(id=prd_id)
        print(prd_model)
        if len(prd_model)>0:
            prd_model = prd_model[0]
            model = wishlist.objects.filter(buyer=request.user,product=prd_model)

            if len(model)==0:  
                new_model = wishlist.objects.create(name=prd_model.name,product=prd_model,buyer=request.user)
                new_model.save()
                notifications = "Product added to wishlist"
                return redirect('products:wishlist')
            else:
                notifications = "Product already in wishlist"




    if request.method=="POST" and "cart_button" in request.POST:

        


        prd_id = int(request.POST["cart_button"])
        prd_dt = Product_Model.objects.filter(id=prd_id)[0]
        
        mdl = cart_model.objects.filter(buyer=request.user,name=prd_dt)
        
        
        if len(mdl)==0:
            print(True)
            new_cart_model = cart_model.objects.create(buyer=request.user,name=prd_dt,quantity=1,image=prd_dt.image,net_price=prd_dt.price,seller=prd_dt.author)
            new_cart_model.save()
            return redirect('products:cart')

            
            
            

        else:
            mdl = mdl[0]
            mdl.quantity+=1
            mdl.net_price+= prd_dt.price
            mdl.save()
            
            return redirect('products:cart')

            
        
            
    
        



        




    wish_prd = wishlist.objects.filter(buyer=request.user)
    wish_id = []
    for each in wish_prd:
        wish_id.append(each.product)
    if len(wish_id)>3:
        wish_id = wish_id[:3]

    ft_prd = featured.objects.all()
    ft_id = []
    for each in ft_prd:
        ft_id.append(each.product)
    if len(ft_id)>3:
        ft_prd = ft_prd[:3]



    if request.GET.get("query") != None:
        main_q = Q(name__icontains=request.GET.get("query")) | Q(bio__icontains=request.GET.get("query")) 
        search_data = Product_Model.objects.filter(main_q)
        return render(request, "products.html", {"data": search_data, "ft_prd":ft_id,"wish_prd":wish_id})

    x = Product_Model.objects.all().order_by("-created")
    prd_data = []
    for each in x:
        if each.status!="Not Available":
            prd_data.append(each)
    return render(request, "products.html", {"data": prd_data   ,"ft_prd":ft_id,"wish_prd":wish_id})


@login_required
def products_details(request, pk):


    if request.method=="POST" and "wishlist_button" in request.POST:
        
        prd_id = request.POST["wishlist_button"]
        prd_model = Product_Model.objects.filter(id=prd_id)
        print(prd_model)
        if len(prd_model)>0:
            prd_model = prd_model[0]
            model = wishlist.objects.filter(buyer=request.user,product=prd_model)
            print(model)
            if len(model)==0:
              
                new_model = wishlist.objects.create(name=prd_model.name,product=prd_model,buyer=request.user)
                new_model.save()
                return redirect('products:wishlist')



    x = Product_Model.objects.get(id=pk)
    
    c = product_comment.objects.filter(com_id=pk).order_by("-created")
    len_com = len(c)
    net = 0
    y = prod_comm(request.POST or None)

    if request.method == "POST" and "comment_button" in request.POST:
        if y.is_valid() and y.cleaned_data.get("body") != None:
            z = product_comment.objects.create(
                body=y.cleaned_data.get("body"),
                com_id=pk,
                author=request.user,
            )
            z.save()
            return redirect('products:pr_details', pk=pk)

    if request.method == "POST" and "cart_button" in request.POST:
        

        st=False
        if request.POST.get("quantity") != None:
            quantt = request.POST.get("quantity")
            net = int(x.price)*int(quantt)

            cart_data = cart_model.objects.filter(buyer=request.user)
            present = False
            for each in cart_data:
                if each.name == x:
                    st=True
                    each.quantity += int(quantt)
                    each.net_price += (x.price*int(quantt))
                    each.save()
                    return redirect('products:cart')


            if st==False:
                cart_mod = cart_model.objects.create(
                    quantity=quantt,
                    net_price=net,
                    image=x.image,
                    buyer=request.user,
                    name=x,
                    seller=x.author,
                )

                cart_mod.save()

                return redirect('products:cart')

    return render(request, "pr_details.html", {"data": x, "product_comm": c, "len_com": len_com})


@login_required
def cart_view(request):


    if request.method == "POST" and "update_cart" in request.POST:
        data = request.POST
        filter = []
        for each in data:
        
            try:
              
                if int(each):
                    filter.append([int(each),int(request.POST[each])])
            except:
                pass
        for each in filter:
            prd = Product_Model.objects.filter(id=each[0])[0]
            cart_dt = cart_model.objects.filter(buyer=request.user,name=prd)[0]
            print(cart_dt.net_price,cart_dt.quantity)
            cart_dt.quantity = each[1]
            cart_dt.net_price = each[1]*cart_dt.name.price
            cart_dt.save()
            print(cart_dt.net_price,cart_dt.quantity)

            


    x = cart_model.objects.filter(buyer=request.user)
    y = len(x)

    sum_total = 0
    pr_collect = cart_model.objects.filter(buyer=request.user)
    for each in pr_collect:
        sum_total+=each.net_price

    
    notifications = ""
   
    if request.method == "POST" and "inc_quantity" in request.POST:
        prd_id = int(request.POST["inc_quantity"])
        mdl = cart_model.objects.filter(id=prd_id)[0]   
       
        
        mdl.quantity+=1
        mdl.net_price+= mdl.name.price
        mdl.save()

        


    if request.method == "POST" and "dec_quantity" in request.POST:
        prd_id = int(request.POST["dec_quantity"])
        mdl = cart_model.objects.filter(id=prd_id)[0]

        if mdl.quantity>1:
            mdl.quantity-=1
            mdl.net_price-= mdl.name.price
            mdl.save()
        else:
            notifications = "Quantity cannot be 0"

    
    
         
        
    
   

    if request.method == "POST" and "delete_button" in request.POST:
        
        prd_id = int(request.POST["delete_button"])
        data = cart_model.objects.filter(id=prd_id)
        
        if len(data)==0:
            pass
        else:
            for each in data:
                each.delete()
                
        x = cart_model.objects.filter(buyer=request.user)
        y = len(x)

        sum_total = 0
        pr_collect = cart_model.objects.filter(buyer=request.user)
        for each in pr_collect:
            sum_total += each.net_price
        return render(request, "cart.html", {"data": x, "sum": sum_total, "num_cart": y})
    

   
    

    
    


    

    
       
    return render(request, "cart.html", {"data": x, "sum": sum_total, "num_cart": y,"notf":notifications})


@method_decorator(login_required, name='dispatch')
class cart_deleteview(DeleteView):
    model = cart_model
    template_name = "delete_cart.html"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy('products:cart')


@login_required
def confirm(request):
    return render(request, "order.html")


@login_required
def orders(request):
    a = sales_list.objects.all()
    a = a.filter(costumer=request.user).order_by("-time")
    return render(request, "order_details1.html", {"form": None, "ord_table": a})


@login_required
def ord_details(request, pk):
    x = sales_list.objects.filter(transaction_id=pk)[0]
    fet_prd = featured.objects.all()
    if len(fet_prd)>3:
        fet_prd = fet_prd[:3]


    return render(request, "order_details2.html", {"data": x,"fet_prd":fet_prd})


@login_required
def sales(request):
    
    a = sales_list.objects.filter(salesman=request.user).order_by("-time")
    return render(request, "sale_details1.html", {"form": None, "ord_table": a})


@login_required
def sale_details(request, pk):
    x = sales_list.objects.get(transaction_id=pk)
    return render(request, "sale_details2.html", {"data": x})




@login_required
def wishlist_data(request):

    if request.method=="POST" and "cart_button" in request.POST:
        print(request.POST)
        prd_id = request.POST["cart_button"]
        prd_model = Product_Model.objects.filter(id=prd_id)[0]
        cart_data = cart_model.objects.filter(buyer=request.user,name=prd_model)
        if len(cart_data)==0:
            cart_item = cart_model.objects.create(name=prd_model,buyer=request.user,net_price=prd_model.price,quantity=1,seller=prd_model.author)
            cart_item.save()
            wish_model = wishlist.objects.filter(buyer=request.user,product=prd_model)[0]
            wish_model.delete()
            return redirect('products:cart')
        else:
            wish_model = wishlist.objects.filter(buyer=request.user,product=prd_model)[0]
            wish_model.delete()
            return redirect('products:cart')
    



    ft_prd = featured.objects.all()
    if len(ft_prd)>3:
        ft_prd = ft_prd[:3]
    if request.method=="POST" and "delete_wish" in request.POST:
        wish_id = int(request.POST["delete_wish"])
        data = wishlist.objects.filter(id=wish_id)[0]
        data.delete()


    x = wishlist.objects.filter(buyer=request.user)
    return render(request, "wishlist.html", {"data": x,"ft_prd":ft_prd})




@login_required
def confirm_orders(request):

    x = cart_model.objects.filter(buyer=request.user)
    y = len(x)

    sum_total = 0
    pr_collect = cart_model.objects.filter(buyer=request.user)
    for each in pr_collect:
        sum_total+=each.net_price



    if request.method == "POST":

        salesman = []

        for each in x:
            if each.name.author not in salesman:
                salesman.append(each.name.author)
            ord_mod = order_model.objects.create(
                quantity=each.quantity,
                buyer=each.buyer,
                seller=each.seller,
                name=each.name,
                image=each.image,
                net_price=each.net_price,
            )

            ord_mod.save()

        for i in salesman:
            a = cart_model.objects.filter(seller=i)
            b = order_model.objects.all().order_by('-id')[:y][::-1]
            lii = []
            for each in b:
                if each.seller == i:
                    lii.append(each)

            print(b)
            summ = 0
            for each in a:
                summ += each.net_price

            sale = sales_list.objects.create(
                costumer=request.user,
                salesman=i,
                net_price=0,

            )
            summ = 0
            for each in a:
                summ += each.net_price
            for each in lii:
                sale.products.add(each)

            sale.net_price = sum_total
            
            sale.name = request.POST["f_name"]+request.POST["l_name"]
            sale.number = request.POST["phone"]
            sale.adress = request.POST["adress"]
            sale.save()
            

        cart_model.objects.filter(buyer=request.user).delete()

        return redirect("products:confirm")

    return render(request,"confirm_order.html",{"data": x, "sum": sum_total, "num_cart": y})
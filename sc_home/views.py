from django.shortcuts import redirect, render
from sc_home.models import feedback_model
from products.models import featured

def welcome(request):
    data = featured.objects.all()
    print(data)
    for each in data:
         print(each.product.image.url)
    return render(request, "welcome.html",{"data":data})

def contact(request):

    if request.method=="POST" and "submit_feedback" in request.POST:
        topic = request.POST["topic"]
        message = request.POST["message"]
        
        fd_model = feedback_model.objects.create(topic=topic,feed=message,author=request.user)
        fd_model.save()
        return redirect('products:all_pr')


    return render(request, "contact.html")

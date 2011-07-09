from django.http import HttpResponse

#Home is just a home, its just a single page that combines everything
#Please separate another page into a single app instead
def home(request):
    return HttpResponse(status = 200)

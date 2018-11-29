from django.http import HttpResponse


def index(request):
    return HttpResponse("List all documnets of User")

def uploadNewFile(request):
    return HttpResponse("Page to upload new document")

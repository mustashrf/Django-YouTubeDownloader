from django.shortcuts import render
from .forms import DownloaderForm
from django.http import HttpResponse, FileResponse
from .downloader import main, upgradePackage
import mimetypes

# Create your views here.
def home(request):
    upgradePackage()
    return render(request, 'home.html', {'form':DownloaderForm})

def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return str(ip)

def download(request):
    if request.GET:
        data = request.GET
        choice = data['choice']
        url = data['url']
        exceptions = data['exceptions']
        av = data['av']
        quality = data['quality']
        input = [url,av,quality,exceptions]
        ip = get_client_ip(request)

        msg, file = main(choice, input, ip)
        if msg:
            filename = file.split('/')[-1]
            f = open(file, 'rb')

            # mime_type, _ = mimetypes.guess_type(file)
            # response = HttpResponse(f, content_type=mime_type)
            # response['Content-Disposition'] = "attachment; filename=%s" % filename
            # return response
            
            return FileResponse(f, as_attachment=True)

        else:
            return HttpResponse('Error')


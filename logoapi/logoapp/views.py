import os
import shutil
import tempfile
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
import subprocess
from .src.crawler import extract_logo_image
from .src.remove_bg import remove_background
from io import BytesIO
import zipfile
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from wsgiref.util import FileWrapper
from django.shortcuts import redirect, reverse, render

def home(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        # process the text here
        url = reverse('get_images') + f'?url={text}' # create URL with query
        return redirect(url)
    return render(request, 'home.html')
@csrf_exempt
def get_images(request):
    if request.method=="GET":
        url = request.GET.get('url')
        # Call crawler.py and get the list of image paths
        cmd = ['python3', './logoapp/src/crawler.py', url]
        out=subprocess.run(cmd, stdout=subprocess.PIPE)
        image_paths = out.stdout.decode().strip().split('\n')
        image_paths = [i.strip() for i in image_paths]
        manipulated_image_paths = []
        for ori_path in image_paths:
            new_path='./static/img/'+'manipulated_' + os.path.basename(ori_path).split('.')[0]+".png"
            manipulated_image_paths.append(new_path)
            cmd = ['python3', './logoapp/src/remove_bg.py', ori_path, new_path]
            out=subprocess.run(cmd).stdout
        #return JsonResponse({'image_paths': manipulated_image_paths})
        total_images=image_paths+manipulated_image_paths
        total_images=[img[img.find("img"):] for img in total_images]
        print(f"total_images:{total_images}")
        # Load the image_template.html template and render it with the image paths
        template = loader.get_template('images.html')
        context = {'image_paths': total_images}
        html = template.render(context)
        # Return the HTML response
        return HttpResponse(html)
    
    elif request.method=="POST":
        selected_images = request.POST.getlist("selected_images")
        zip_path = os.path.join(settings.MEDIA_ROOT, "selected_images.zip")
        with zipfile.ZipFile(zip_path, "w") as zip_file:
            for image_path in selected_images:
                image_full_path ="./"+ os.path.join(settings.STATIC_URL, image_path)
                zip_file.write(image_full_path, image_path)
        with open(zip_path, "rb") as zip_file:
            response = HttpResponse(FileWrapper(zip_file), content_type="application/zip")
            response["Content-Disposition"] = f"attachment; filename=images.zip"
            return response
    
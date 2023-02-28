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

def get_images(request):
    url = request.GET.get('url')
    # Call crawler.py and get the list of image paths
    cmd = ['python3', './logoapp/src/crawler.py', url]
    out=subprocess.run(cmd, stdout=subprocess.PIPE)
    image_paths = out.stdout.decode().strip().split('\n')
    image_paths = [i.strip() for i in image_paths]
    manipulated_image_paths = []
    for ori_path in image_paths:
        new_path = '/static/img/'+'manipulated_' + os.path.basename(ori_path)
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


def download_images(request):
    url = request.GET.get('url')
    # Call crawler.py and get the list of image paths
    cmd = ['python3', './logoapp/src/crawler.py', url]    
    out=subprocess.run(cmd, stdout=subprocess.PIPE)
    image_paths = out.stdout.decode().strip().split('\n')
    image_paths = [i.strip() for i in image_paths]
    
    manipulated_image_paths = []
    for ori_path in image_paths:
        new_path = 'img/'+'manipulated_' + os.path.basename(ori_path)
        manipulated_image_paths.append(new_path)
        cmd = ['python3', './logoapp/src/remove_bg.py', ori_path, new_path]
        out=subprocess.run(cmd).stdout
    total_images=image_paths+manipulated_image_paths
    # Create a response object
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="images.zip"'
        
    # Zip the images and write to response
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        for image_path in total_images:
            z.write(image_path)
        for image_path in manipulated_image_paths:
            z.write(image_path)
    buffer.seek(0)
    response.write(buffer.read())
        
    return response    
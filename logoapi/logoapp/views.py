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
def get_images(request):
    url = request.GET.get('url')
    # Call crawler.py and get the list of image paths
    cmd = ['python', './logoapp/src/crawler.py', url]
    #p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    #out, err = p.communicate()
    
    out=subprocess.run(cmd, stdout=subprocess.PIPE)
    print(f"out.stdout: {out.stdout}")
    image_paths = out.stdout.decode().strip().split('\n')
    image_paths = [i.strip() for i in image_paths]
    # Call remove_background.py for each image and get the list of manipulated image paths
    manipulated_image_paths = []
    for ori_path in image_paths:
        print(f"input: {ori_path}")
        new_path = 'images/'+'manipulated_' + os.path.basename(ori_path)
        manipulated_image_paths.append(new_path)
        cmd = ['python', './logoapp/src/remove_bg.py', ori_path, new_path]
        # p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        # out, err = p.communicate()
        out=subprocess.run(cmd).stdout
    return JsonResponse({'image_paths': manipulated_image_paths})

def download_images(request):
    url = request.GET.get('url')
    # Call crawler.py and get the list of image paths
    cmd = ['python', './logoapp/src/crawler.py', url]
    #p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    #out, err = p.communicate()
    
    out=subprocess.run(cmd, stdout=subprocess.PIPE)
    print(f"out.stdout: {out.stdout}")
    image_paths = out.stdout.decode().strip().split('\n')
    image_paths = [i.strip() for i in image_paths]
    # Call remove_background.py for each image and get the list of manipulated image paths
    manipulated_image_paths = []
    for ori_path in image_paths:
        print(f"input: {ori_path}")
        new_path = 'images/'+'manipulated_' + os.path.basename(ori_path)
        manipulated_image_paths.append(new_path)
        cmd = ['python', './logoapp/src/remove_bg.py', ori_path, new_path]
        # p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        # out, err = p.communicate()
        out=subprocess.run(cmd).stdout
        
        
    # Create a response object
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="images.zip"'
        
        # Zip the images and write to response
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        for image_path in image_paths:
            z.write(image_path)
        for image_path in manipulated_image_paths:
            z.write(image_path)
    buffer.seek(0)
    response.write(buffer.read())
        
    return response    
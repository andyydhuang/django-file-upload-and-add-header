import tempfile
import os
import pathlib
import io

from django.shortcuts import redirect, render
from .models import Document
from .forms import DocumentForm
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    CreateView,
    FormView,
)
from django.views import View
from django.conf import settings
from zipfile import ZipFile
from os.path import basename

from django.http import JsonResponse
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from myapp.variables import *
#import myapp.variables as Variables
#from variables import *

class DocListView(ListView):
    model = Document
    template_name = 'main.html'

class DocUploadView(FormView):
    form_class = DocumentForm
    template_name = 'doc_upload.html'
    success_url = '/'   

def add_files_crc(post, f, signed_files):

    DIRNAME = str(pathlib.Path(__file__).parent.resolve())
    print(f"DIRNAME: {DIRNAME}")

    input_file_path = DIRNAME + OUTPUT_DIR + IN_FILE_NAME
    output_file_path = DIRNAME + OUTPUT_DIR + OUT_FILE_NAME

    if not os.path.exists(DIRNAME + OUTPUT_DIR):
        # if the demo_folder directory is not present 
        # then create it.
        os.makedirs(DIRNAME + OUTPUT_DIR)

    with open(input_file_path, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    #uploaded_file_index = int(post.get('file_index'))
    uploaded_file_index = 0 # Use default value 0

    add_header_exe_path = DIRNAME + '/add_crc_header.py'

    #print(f"add_header_exe_path: {add_header_exe_path}")
    cmd = "python {0} {1} {2} {3} --input {4} --output {5}".format(add_header_exe_path, 
        settings.BUILD_MAJOR, settings.BUILD_MINOR, uploaded_file_index, input_file_path, output_file_path)
    os.system(cmd)

    dest_file_path = DIRNAME + OUTPUT_DIR + f.name + "_crc"
    if os.path.isfile(dest_file_path):
        os.remove(dest_file_path)
    os.rename(output_file_path, dest_file_path)

    #print(f"dest_file_path: {dest_file_path}")
    signed_files.append(dest_file_path)

def write_file_to_db(final_signed_file, img_type):
    total_len = 0
    f_bytes = io.BytesIO()

    with  open(final_signed_file, "rb") as signed_f:
        for line in signed_f:        
            total_len =  total_len + len(line)    
            f_bytes.write(line)   
	
    file_obj = InMemoryUploadedFile(f_bytes, None, basename(final_signed_file), None, total_len, None, None)
    newdoc = Document(docfile=file_obj, doctype=img_type)
    newdoc.save()

def handle_uploaded_file(post, req_file):
    DIRNAME = str(pathlib.Path(__file__).parent.resolve())
    copy_post = post.copy() # to make it mutable

    signed_files = []
    add_files_crc(copy_post, req_file, signed_files)
    write_file_to_db(signed_files[0],"GENERAL")

    for root, dirs, files in os.walk(DIRNAME):
        for file in files:
            #if file.startswith(IN_FILE_NAME) or file.startswith(req_file.name):
            if file.startswith(IN_FILE_NAME):
                os.remove(os.path.join(root, file))

class HandleDocUploadView(ListView):
    success_url = '/' 

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            handle_uploaded_file(request.POST, request.FILES['docfile'])

        return redirect('my-view')


class DocDeleteView(ListView):
    model = Document
    template_name = 'doc_delete.html'

class HandleDocDeleteView(ListView):
    success_url = '/' 

    def post(self, request):
        doc_ids = request.POST.getlist('toDeleteDocs')

        for doc_id in doc_ids:
            document_to_delete = Document.objects.get(id=doc_id)
            document_to_delete.delete()

        return redirect('my-view')

def deleteSingleDocument (request, doc_id):
    document_to_delete = Document.objects.get(id=doc_id)
    document_to_delete.delete()

    return HttpResponseRedirect('/')

def deleteDocuments (request):
    if request.method == 'POST':
        doc_ids = request.POST.getlist('toDeleteDocs')

        for doc_id in doc_ids:
            document_to_delete = Document.objects.get(id=doc_id)
            document_to_delete.delete()

    return HttpResponseRedirect('/')
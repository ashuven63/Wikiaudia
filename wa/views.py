from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
import json
from django.core import serializers
from django.conf import settings
import os
from PIL import Image
from django.core.urlresolvers import reverse
from wa.models import User,Language,Book, Paragraph, UserHistory, Document# Create your views here.
from wa.forms import DocumentForm
from wa.tasks import soundProcessingWithAuphonicTask
# Create your views here.

def audioSelection(request):
    #languages = Language.objects.all()
	#context = {'all_languages' : all_languages}
    #return render(request, 'wa/audio.html', context)
    #return HttpResponse("You're looking at the results of poll ")
    langs = Language.objects.all()
    #context = {'langs': langs}
    context = RequestContext(request, {'langs': langs, } )
    return render(request, 'wa/audio.html', context)

def getImage(request, book_id):
	response = HttpResponse(mimetype = "image/jpg");
	path = os.path.dirname(settings.BASE_DIR) + "/" + "wastore/" + book_id + "/" + "frontcover.jpg"
	print(path);
	if(os.path.exists(path)):
		image = Image.open(path)
	else:
		image = Image.open(os.path.dirname(settings.BASE_DIR) + "/" + "wastore/" + "default/" + "frontcover.jpg")
	image.save(response, 'png');
	return response; 

def audioUpload(request, book_id):
    #print("book_id")
    #print(book_id)
    #return HttpResponse("You're looking at poll %s" %  book_id)
    #Make a function call for choosing a para for the user.
    #render ash's view
    # Handle file upload
    '''
    Add additional inputs to post to figure out the book and 
    the paragraph number so that the upload takes place in that folder
    Current working : Saves the file with a fixed name and the file sent for API processing is fixed as well. 
    Both of these should be made dynamic 
    '''
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.docfile.save('Ashu.wav',request.FILES['docfile'])
            #soundProcessWithAuphonic('documents/Ashu.wav')
            soundProcessingWithAuphonicTask.delay('../documents/ashu.mp3')
            return HttpResponseRedirect(reverse('wa.views.audio'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'wa/audioUpload.html',
        {'documents': documents, 'form': form},
       
        context_instance=RequestContext(request)
    )

def langBooks(request):
	#print(os.path.dirname(settings.BASE_DIR))
	#outside = os.path.dirname(settings.BASE_DIR)
	#if(os.path.exists())
	language = request.GET['language']
	#print(language);
	language = Language.objects.get(langName = language)
	#print(language)
	languageBooks = language.book_set.all()
	ret = serializers.serialize("json", languageBooks)
	#resp = HttpResponse(content_type = "application/json");
	#json.dump(languageBooks, resp)
	return HttpResponse(ret)


#def audioUpload(request):
    
    
def uploadBook(request):
    # Handle file upload
    if request.method == 'POST':

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('wa.views.audio'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Render list page with the documents and the form
    return render_to_response(
        'wa/uploadBook.html',
        {'form': form},
        context_instance=RequestContext(request)
    )

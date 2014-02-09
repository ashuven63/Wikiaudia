from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from wa.models import User, Language, Book, Paragraph, UserHistory, Document
from wa.forms import DocumentForm

from wa.tasks import soundProcessingWithAuphonicTask
from django.core.urlresolvers import reverse
# Create your views here.

def audio(request):
    #languages = Language.objects.all()
	#context = {'all_languages' : all_languages}
    #return render(request, 'wa/audio.html', context)
    #return HttpResponse("You're looking at the results of poll ")
    langs = Language.objects.all()
    context = {'langs': langs}
    return render(request, 'wa/audio.html', context)

def audioUpload(request):
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

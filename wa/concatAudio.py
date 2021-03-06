import logging
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
import wave
import time
from django.core.files import File
import os
def auConcat(book_id):
    from wa.models import Language,Book, Paragraph, UserHistory, Document, CustomUser# Create your views here.
    log = logging.getLogger("wa")
    log.setLevel(10)
    log.info("Concat one")
    para_no = Paragraph.objects.filter(book=Book.objects.get(pk=book_id))
    infiles_list = []
    all_files_list = []
    offset=1;
    for i in para_no:
        version_val =  i.validAudioVersionNumber 
        file_name = str(book_id) + "/chunks/" + str(i.id) + "/AudioFiles/"+str(version_val)+".wav"
        if ((i.isChapter == 1)|(offset==1)):
            infiles_list = []
        infiles_list.append(file_name)
        if(offset<=len(para_no)-1):
            if (para_no[offset].isChapter==1):
                all_files_list.append(infiles_list)
        if(offset==len(para_no)):
            all_files_list.append(infiles_list)
        offset=offset+1
        log.info("all_files_list:  "+str(all_files_list))
    #print("all_files_list")
    #print(all_files_list)
    return all_files_list

def audioConcatenation(book_id):
    log = logging.getLogger("wa")
    log.setLevel(10)
    log.info("one")
    #time.sleep(60)
    all_files_list=auConcat(book_id)
    count=1;
    for i in all_files_list:
        for j in i:
            log.info("j : " + j)
            a = default_storage.open(j)
            path_to_save='/tmp/audioFiles/'
            local_fs = FileSystemStorage(location=path_to_save)
            local_fs.save(a.name,a)
    for i in all_files_list:  
        data= []
        temp1 = 0
        outfile='/tmp/audioFiles/'+str(book_id)+'/'+str(count)+'.wav'
        #with wave.open(outfile, 'wb') as output:        
            # each chapter ka chunk
        for j in i:
            temp='/tmp/audioFiles/'+j
            w = wave.open(temp, 'rb')
            data.append( [w.getparams(), w.readframes(w.getnframes())] )
            w.close()
            temp1 = temp1+1
        log.info("Count:  "+str(count))  
        output= wave.open(outfile, 'wb')  
        output.setparams(data[0][0])
        for k in range(0,temp1): 
            output.writeframes(data[k][1])
        #output.writeframes(data[0][1])
        #output.writeframes(data[1][1])
        output.close()          
        f = open(outfile, 'rb')
        myfile = File(f)
        new_name =str(book_id) + "/AudioChapters/Chapter"+str(count)+".wav"
        log.info("new_name: "+ new_name)
        default_storage.save(new_name,myfile)
        os.remove(outfile)
        count=count+1
    log.info("done")
    '''     
    for i in all_files_list:        
        for j in i:
            temp='/tmp/audioFiles/'+j
            os.remove(temp)
    '''

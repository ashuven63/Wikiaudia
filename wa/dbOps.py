from wa.models import Language, Book, Paragraph, UserHistory, Document

def uploadDigi(book_id, para_id):
	'''
	a digitized document is uploaded
	first update the percentatge complete
	then add a row to the table specifying who read it
	then change the status of this chunk
	'''
	
	
	

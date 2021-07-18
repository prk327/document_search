# Document Digitization Engine
# digtize documents and save into elasticsearch index
import os
import uuid
import glob
import datetime
import docx2txt
from io import StringIO
#import win32com
# #from win32com import client
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def digitize_and_insert(doc_repo_path, es_client, es_index):
    """
    reads text content and insert into elasticsearch instance
    doc_repo_path = repository of document full path
    es_clinet : elasticsearch client
    es_index : name of the elasticsearch index
    return : None
    """

    data_array = []
    for f in glob.iglob(doc_repo_path+ "/*.*"): # for windwos revers slash

        if f.lower().endswith('.pdf'):
            doc = read_pdf(f)
            data_array.append(doc)

        elif f.lower().endswith('.txt'):
            doc = read_text(f)
            data_array.append(doc)

        elif f.lower().endswith('.docx'):
            doc = read_docx(f)
            data_array.append(doc)

        else:
            print("document not supported: ",os.path.basename(f))

    print("Documents to be inserted:",len(data_array))

    # insert into elasticsearh
    for data in data_array:
        res = es_client.index(index=es_index, body=data)
    # refresh es
    es_client.indices.refresh(index=es_index)

def get_file_stats(f):
    """
    get file stats
    f : filepath
    returns dict
    """
    di = {'file_name' : os.path.basename(f),
          'file_path': f,
          'file_type': f.split('.')[-1],
          'doc_id': str(uuid.uuid4().int)[:6]
          }

    def _size(f):
        n = os.path.getsize(f)
        for x in ['bytes', 'KB', 'MB', 'GB']:
            if n < 1024.0:
                return f"{n:.2f}{x}"
            n /= 1024.0

    di['file_size'] = _size(f)

    # append doc_created dt
    ts = os.path.getctime(f)
    ts = datetime.datetime.fromtimestamp(ts)
    fcd = datetime.datetime.strftime(ts, '%Y-%m-%d')
    di['document_created_dt'] = fcd

    # append doc modified dt
    ts = os.path.getmtime(f)
    ts = datetime.datetime.fromtimestamp(ts)
    fmd = datetime.datetime.strftime(ts, '%Y-%m-%d')
    di['documnet_modified_dt'] = fmd

    return di


def read_text(txt_file):
    """
    digitize text file
    txt_file: filepath
    returns : dict
    """
    di = get_file_stats(txt_file)
    with open(txt_file) as f:
        di['content'] = f.read()

    return di


def read_docx(docx_file):
    """
    digitize docx file
    """
    di = get_file_stats(docx_file)
    di['content']=docx2txt.process(docx_file)
    return di


# def read_doc(doc_file_name):
#     """
#     read and digitize .doc files
#     """
#     word = win32com.client.Dispatch("Word.Application")
#     word.Visible = False
#
#     _ = word.Documents.Open(doc_file_name)
#
#     doc = word.ActiveDocument
#     paras = doc.Range().text
#     doc.Close()
#     word.Quit()
#
#     di = get_file_stats(doc_file_name)
#     di['content'] = paras
#     return di


def read_pdf(path):
    """
    digitze pdf document
    path : filepath
    returns dict
    """
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    di = get_file_stats(path)
    di['content']= text
    return di
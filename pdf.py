#https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167
#http://www.unixuser.org/~euske/python/pdfminer/#source

from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

USER_LANGUAGES = []
LANG_LIST = ['Arduino', 'Assembly', 'BASIC', 'C', 'C#',
             'C++', 'CSS', 'CUDA', 'Curl', 'Go',
             'HTML', 'Haskell', 'Java', 'JavaScript', 'LISP',
             'MATLAB', 'Maple', 'MySQL', 'Objective-C', 'OCaml'
             'PHP', 'Perl', 'Prolog', 'Python', 'R',
             'Ruby', 'SML', 'Shell', 'Swift', 'TeX',
             'jQuery']

def list_to_string(languages):
    lang_string = ''
    for item in languages:
        if lang_string == '':
            lang_string += item
        else:
            lang_string += ', ' + item
    return lang_string

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = fname # file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

def is_programming_language(token):
    global USER_LANGUAGES, LANG_LIST
    if (token in LANG_LIST) and (token not in USER_LANGUAGES):
        return True
    else:
        return False

def find_GPA(tokens):
    GPA = ''
    for i in range(0, len(tokens)):
        if (tokens[i] == "GPA:") or (tokens[i] == "GPA-") or (tokens[i] == "GPA"):
            GPA = tokens[i + 1]
    return GPA

def verify_token(token, tokens_list):
	global USER_LANGUAGES
   	if is_programming_language(token):
   		USER_LANGUAGES.append(token)
   	else:
   		tokens_list.append(token)

def tokenize_PDF(res_str):
    token = ''
    tokens_list = []
    break_list = [' ', ',', '\n', '\t', '?',
    			  '?', '(', ')', '/']
    
    for i in range(0, len(res_str)):
        char = res_str[i]

        if char in break_list:
            if token != '':
                verify_token(token, tokens_list)
                token = ''

        elif char == '.':
            next_char = res_str[i+1]
            if next_char == " ":
                if token != '':
                    verify_token(token, tokens_list)
                    token = ''
            else:
                token += char

        else:
        	# normal character
            token += char
    
    return tokens_list

def extract_data(f):
    global USER_LANGUAGES
    resume_string = convert(f, [0])
    tokens = tokenize_PDF(resume_string)
    GPA = find_GPA(tokens)
    languages_string = list_to_string(USER_LANGUAGES)
    
    if languages_string == '':
        languages_string = 'Please See Resume'
    if GPA == '':
        GPA = 'Please See Resume'
    
    return {'languages' : languages_string,
    		'GPA' : float(GPA)}

# extract_data(file('samples/ZachWieandResume.pdf'))


import os,sys
sys.path.insert(0, os.path.abspath(os.curdir))

current_directory = os.path.dirname(os.path.abspath(__file__))
html_sample_path = os.path.join(current_directory, 'htmlSample.html')

class GetHtmlFromWhatsAppMock:        
    def extract_HTML(self):
        with open(html_sample_path, 'r', encoding='utf-8') as file:
            return file.read()
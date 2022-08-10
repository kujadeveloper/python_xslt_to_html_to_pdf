import pdfkit  
from lxml import etree
import os
import io
import openpyxl

class toPdf():
# configuring pdfkit to point to our installation of wkhtmltopdf 
    options = {
        'margin-top': '70mm',
        'page-height': 0,
        'page-width': 0,
        'orientation':'Landscape',
        'encoding': "UTF-8"
    }
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")


    HERE = os.path.dirname(__file__)

    def __init__(self,height,width,potrait,topmargin):
        self.options['page-height'] = height
        self.options['page-width'] = width
        self.options['orientation'] = potrait
        this.options['margin-top'] = topmargin

        print(self.options)


    def layout(self,src_path, dst_path):
        # load the XSL
        xsl_path = src_path
        xsl_tree = etree.parse(xsl_path)

        # load the XML source
        src_tree = etree.parse(src_path.replace('xslt','xml'))

        # transform
        transformer = etree.XSLT(xsl_tree)
        dst_tree = transformer.apply(src_tree)

        # write the result
        with io.open(dst_path, mode="wb") as f:
            f.write(etree.tostring(dst_tree, encoding="utf-8", method="html"))
        f.close()

    def replaceHtmlFile(self):
        f = open("outline.html", "r", encoding="utf8")
        string_html = f.read()
        f.close()
        string_html = string_html.replace('width="60%" align="center"','width="60%" align="left"')
        string_html = string_html.replace('notesTableTd','')
        string_html = string_html.replace('customerPartyTable', '')
        string_html = string_html.replace('budgetContainerTable', '')

        new_string_html=string_html
        # if string_html.find('İade Bölümü') == -1:
        #     new_string_html = string_html.replace('font-size: 11px;','font-size: 9px;')
        # else:
        #     new_string_html = string_html.replace('font-size: 11px;','font-size: 7px;')

        os.remove('outline.html')
        with open("outline.html", "a", encoding="utf8") as f:
             f.write(new_string_html)
        f.close()

    def readbarcode(self, s):
        wookbook = openpyxl.load_workbook("Barkodlar.xlsx")
        worksheet = wookbook.active
        cell_obj = worksheet.cell(row = s, column = 2)
        return cell_obj.value

    def main(self,filepath,outputpath,name,i):
        self.layout(filepath ,"outline.html")
        self.replaceHtmlFile()
        barcode = self.readbarcode(i)
        pdfkit.from_file("outline.html",
                         outputpath+'/'+str(barcode)+"_"+name.replace('xslt','pdf'),
                         options=self.options, configuration=self.config)
        if not os.path.exists(outputpath+'/barcode/'):
            os.makedirs(outputpath+'/barcode/')
        pdfkit.from_file("outline.html",
                         outputpath+'/barcode/'+str(barcode)+'.pdf',
                         options=self.options, configuration=self.config)

        #os.remove('outline.html')
    # storing string to pdf file  
    #pdfkit.from_file("index.html", 'output3.pdf',options=options)  
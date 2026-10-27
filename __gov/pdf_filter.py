from __gov.helpers import data, parse_number, clean_legal, is_yes, filter_system
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
import os


parent_folder = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
pdf_folder = os.path.join(parent_folder, "Customed Filter PDFs")
os.makedirs(pdf_folder, exist_ok=True)




class NumberedCanvas(canvas.Canvas):
    def __init__(self,*args,**kwargs):
        canvas.Canvas.__init__(self,*args,**kwargs)
        self._saved_page_states=[]
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        total=len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.drawRightString(580,20,f"{self._pageNumber}/{total}")
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

# ----------------Steven Cleanup Functions ----------------

def say(name, text):
    elements.append(Paragraph(f"<b>{name}: {text}</b>", styles['Normal']))

def space():
    elements.append(Spacer(1,10))


# --------------------------------------------------------
def save_property_pdf(data, county_name, amount):
    filename = os.path.join(pdf_folder, f"{county_name}_Custom_Filter.pdf")
    global styles
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename)
    global elements
    elements = []
    count = 0
    page_count = 0
    
    cls()
    print("a. Filter By Owner")
    print("b. Filter By Not the Owner")
    choice = input(">>>")






    
    for r in data:
        # -------------Intrested Propertys ----------------------------------------------------------
        if is_yes(r) and parse_number(r.get("True Improvements",""))==0:
            if filter_system(r, choice):
                if page_count==0:
                    elements.append(Paragraph(f"<b>{county_name.upper()} COUNTY</b>", styles['Title']))
                    elements.append(Spacer(1,6))
                    # --------------------------------------------------------------------------------------------

                count += 1
                # PROPERTY NAME
                elements.append(Paragraph(f"<b>Property #{count}</b>", styles['Heading2']))

                say("PIN", r.get("Unique #"))
                say("Owner", r.get("Owner"))
                say("Address 1", r.get("Address 1"))
                say("County", r.get("Address 4"))
                say("State", r.get("Address 5"))
                say("Zip", r.get("Address 6"))
                space()

                page_count += 1
                if page_count >= amount:
                    elements.append(PageBreak())
                    page_count = 0

    doc.build(elements, canvasmaker=NumberedCanvas)
   


def custom():
    info = data()
    amount = int(input("How many Per Page? (1 thru 4): "))
    if amount >= 4:
        amount = 4
    save_property_pdf(info[0], info[1], amount)
            

        
        
    

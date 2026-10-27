from __gov.helpers import data, parse_number, clean_legal, is_yes
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
import os


parent_folder = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
pdf_folder = os.path.join(parent_folder, "tax_info")
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




# --------------------------------------------------------
def save_property_pdf(data, county_name, amount):
    filename = os.path.join(pdf_folder, f"{county_name}_interested_properties.pdf")
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename)
    elements = []
    count = 0
    page_count = 0
    # -------------------FRONT COVER ------------------------
    elements.append(Paragraph(f"<b>{county_name.upper()} COUNTY</b>", styles['Title']))
    elements.append(Spacer(1,20))
    elements.append(Paragraph(f"<b>Tax's sale year:</b>   __________________", styles['Heading3']))
    elements.append(Spacer(1,50))
    elements.append(Paragraph(f"<b>Tax's year Held:</b>   __________________", styles['Heading3']))
    elements.append(PageBreak())
    elements.append(PageBreak())
    #--------------------SECOND COVER -----------------------------
    elements.append(Paragraph(f"<b>{county_name.upper()} COUNTY</b>", styles['Title']))
    elements.append(Spacer(1,20))
    elements.append(Paragraph(f"<b>Tax's sale year:</b>   __________________", styles['Heading3']))
    elements.append(Spacer(1,50))
    elements.append(Paragraph(f"<b>Tax's year Held:</b>   __________________", styles['Heading3']))
    elements.append(PageBreak())
    elements.append(PageBreak())






    for r in data:
        # -------------Intrested Propertys ----------------------------------------------------------
        if is_yes(r) and parse_number(r.get("True Improvements",""))==0:
            if page_count==0:
                elements.append(Paragraph(f"<b>{county_name.upper()} COUNTY</b>", styles['Title']))
                elements.append(Spacer(1,6))
        # --------------------------------------------------------------------------------------------

            count += 1
            parcel = r.get("Parcel Number", "N/A")
            pinn = r.get("Unique #","N/A")
            owner = r.get("Owner", "N/A")
            building_value = parse_number(r.get("True Improvements",""))
            face = parse_number(r.get("True Land",""))
            legal = clean_legal(r.get("Legal Text",""))

            elements.append(Paragraph(f"<b>Property #{count}</b>", styles['Heading2']))
            elements.append(Paragraph(f"<b>Owner:</b> {owner}", styles['Normal']))
            elements.append(Paragraph(f"<b>Building Value:</b> ${building_value:,.2f}", styles['Normal']))
            elements.append(Paragraph(f"<b>Parcel:</b> {parcel}", styles['Normal']))
            elements.append(Paragraph(f"<b>PINN:</b> {pinn}", styles['Normal']))
            elements.append(Paragraph(f"<b>Face Value:</b> ${face:,.2f}", styles['Normal']))
            elements.append(Paragraph(f"<b>Legal Description:</b> {legal}", styles['Normal']))
            elements.append(Spacer(1,10))

            page_count += 1
            if page_count >= amount:
                elements.append(PageBreak())
                page_count = 0

    doc.build(elements, canvasmaker=NumberedCanvas)
   


def create():
    info = data()
    amount = int(input("How many Per Page? (1 thru 4): "))
    if amount >= 4:
        amount = 4
    save_property_pdf(info[0], info[1], amount)
            

        
        
    

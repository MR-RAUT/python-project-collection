import os, re, json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether
import glob
import hashlib

class ReportGenerator:
    def __init__(self):
        os.makedirs('output', exist_ok=True)
        self.output_path='output/final_report.pdf'
        s=getSampleStyleSheet()
        self.title=ParagraphStyle('title',parent=s['Title'],fontSize=24,leading=28,textColor=colors.HexColor('#003366'),alignment=1)
        self.h1=ParagraphStyle('h1',parent=s['Heading1'],fontSize=18,textColor=colors.HexColor('#003366'),spaceAfter=8)
        self.h2=ParagraphStyle('h2',parent=s['Heading2'],fontSize=12,textColor=colors.HexColor('#00897B'),spaceAfter=4)
        self.normal=ParagraphStyle('normal',parent=s['BodyText'],fontSize=10,leading=13,spaceAfter=4)
        self.small=ParagraphStyle('small',parent=s['BodyText'],fontSize=8,textColor=colors.grey)

    def page_style(self,canvas,doc):
        canvas.saveState(); w,h=A4
        canvas.setStrokeColor(colors.HexColor('#003366'))
        canvas.line(15*mm,h-12*mm,w-15*mm,h-12*mm)
        canvas.line(15*mm,12*mm,w-15*mm,12*mm)
        canvas.setFont('Helvetica-Bold',9)
        canvas.drawRightString(w-15*mm,h-8*mm,'Detailed Diagnostic Report')
        canvas.setFont('Helvetica',8)
        canvas.drawString(15*mm,7*mm,'DDR AI System | Confidential')
        canvas.drawRightString(w-15*mm,7*mm,f'Page {doc.page}')
        canvas.restoreState()

    def safe(self,t): return '' if not t else str(t).replace('\n','<br/>')
    
    def folder_images(self, keyword):
        out = []
        for root, dirs, files in os.walk("output"):
            for f in files:
                low = f.lower()
                if low.endswith((".png", ".jpg", ".jpeg")):
                    full = os.path.join(root, f)
                    if keyword.lower() in full.lower():
                        out.append(full)
        return out
    
    def clean_images(self, imgs, findings=[], mode="inspection"):
        final = []
        used = set()

        for img in imgs:
            try:
                if not os.path.exists(img):
                    continue

                low = img.lower()
                name = os.path.basename(low)

                # remove duplicates
                if name in used:
                    continue

                # remove small useless images
                if os.path.getsize(img) < 15000:
                    continue

                # 🔥 KEY FIX
                if mode == "thermal":
                    if not any(k in low for k in ["thermal", "heat", "temp", "ir", "flir"]):
                        continue
                else:
                    if any(k in low for k in ["thermal", "heat", "temp"]):
                        continue

                used.add(name)
                final.append(img)

            except:
                pass

        return final[:4]

    def md_images(self,text):
        out=[]
        for p in re.findall(r'!\[.*?\]\((.*?)\)',text or ''):
            p=p.strip().replace('/',os.sep)
            a=p if os.path.exists(p) else os.path.join('output',p)
            if os.path.exists(a): out.append(a)
        return out

    def json_images(self,path):
        if not os.path.exists(path): return []
        with open(path,'r',encoding='utf-8') as f: data=json.load(f)
        out=[]
        def scan(x):
            if isinstance(x,dict):
                for v in x.values(): scan(v)
            elif isinstance(x,list):
                for v in x: scan(v)
            elif isinstance(x,str) and x.lower().endswith(('.png','.jpg','.jpeg')):
                a=x if os.path.exists(x) else os.path.join('output',x)
                if os.path.exists(a): out.append(a)
        scan(data)
        return out

    def best_images(self, imgs):
        seen = []
        names = set()

        for i in imgs:
            low = i.lower()

            if low.endswith(('.png','.jpg','.jpeg')):
                nm = os.path.basename(low)

                if nm not in names:
                    names.add(nm)
                    seen.append(i)

        return seen[:4]

    def findings(self,text):
        keys=['dampness','crack','leak','seepage','moisture','spalling','tile joint','hotspot','corrosion']
        out=[]; used=set()
        for line in (text or '').splitlines():
            t=line.strip(); low=t.lower()
            if len(t)>10 and any(k in low for k in keys) and t not in used:
                used.add(t); out.append(t)
        return out[:20]

    def severity(self,t):
        x=t.lower()
        if 'critical' in x: return 'Critical'
        if 'crack' in x or 'hotspot' in x: return 'High'
        if 'damp' in x or 'moisture' in x: return 'Medium'
        return 'Low'

    def findings_table(self,items):
        data=[['#','Observation','Severity']]
        for n,v in enumerate(items,1): data.append([str(n),v[:95],self.severity(v)])
        tb=Table(data,colWidths=[12*mm,145*mm,25*mm])
        tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#003366')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),0.4,colors.grey),('FONTSIZE',(0,0),(-1,-1),8),('VALIGN',(0,0),(-1,-1),'TOP')]))
        return tb

    def image_page(self,story,title,imgs):
        story.append(PageBreak()); story.append(Paragraph(title,self.h1)); story.append(Spacer(1,6))
        imgs=self.best_images(imgs)
        if not imgs:
            story.append(Paragraph('No images found.',self.normal)); return
        cells=[]
        for p in imgs:
            try: 
                img = Image(p,width=82*mm,height=55*mm) 
                cells.append([img, Paragraph(os.path.basename(p), self.small)])
            except: cells.append(Paragraph('Image Error',self.small))
        while len(cells)<4: cells.append('')
        tb=Table([[cells[0],cells[1]],[cells[2],cells[3]]],colWidths=[87*mm,87*mm])
        tb.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.4,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP')]))
        story.append(tb)

    def create_pdf(self,ai_text='',inspection_md='',thermal_md=''):
        doc=SimpleDocTemplate(self.output_path,pagesize=A4,rightMargin=15*mm,leftMargin=15*mm,topMargin=18*mm,bottomMargin=18*mm)
        story=[]
        story+=[Spacer(1,80),Paragraph('Detailed Diagnostic Report',self.title),Spacer(1,10),Paragraph('AI Powered Inspection Analysis',self.h1),Spacer(1,10),Paragraph(datetime.now().strftime('%d %B %Y'),self.normal),Spacer(1,20),Paragraph('Generated by DDR AI System',self.small),PageBreak()]
        txt=inspection_md+'\n'+thermal_md+'\n'+ai_text
        items=self.findings(txt)
        raw_ins = self.md_images(inspection_md) + \
                self.json_images("output/inspection.json") + \
                self.folder_images("inspection")

        raw_th = self.md_images(thermal_md) + \
                self.json_images("output/thermal.json") + \
                self.folder_images("thermal")

        ins = self.clean_images(raw_ins, items, mode="inspection")
        th  = self.clean_images(raw_th, items, mode="thermal")
        story.append(Paragraph('1. Executive Summary',self.h1))
        story.append(Paragraph('Combined inspection, thermal evidence and AI reasoning used to identify probable defects and corrective actions.',self.normal))
        story.append(Paragraph(f'Total Findings Detected: <b>{len(items)}</b>',self.normal))
        story.append(PageBreak())
        story.append(Paragraph('2. Issue Summary Table',self.h1))
        story.append(self.findings_table(items))
        self.image_page(story,'3. Inspection References',ins)
        self.image_page(story,'4. Thermal References',th)
        story.append(PageBreak()); story.append(Paragraph('5. Detailed Findings',self.h1))
        for i,v in enumerate(items,1): story.append(KeepTogether([Paragraph(f'{i}. Observation',self.h2),Paragraph(self.safe(v),self.normal)]))
        story.append(PageBreak())
        story.append(Paragraph("6. Thermal Analysis", self.h1))
        story.append(Paragraph(
            "Thermal report data reviewed for hidden moisture zones, heat signatures, "
            "water ingress paths and temperature anomalies.",
            self.normal
        ))
        story.append(Paragraph(
            f"Thermal Images Detected: <b>{len(th)}</b>",
            self.normal
        ))

        story.append(Spacer(1,8))
        story.append(Paragraph("7. AI Root Cause Analysis", self.h1))
        story.append(Paragraph(self.safe(ai_text), self.normal))
        story.append(PageBreak()); story.append(Paragraph("8. Disclaimer", self.h1))
        story.append(Paragraph('This report is AI-assisted. Final execution decisions should be verified by qualified professionals.',self.normal))
        doc.build(story,onFirstPage=self.page_style,onLaterPages=self.page_style)

    def run(self,data):
        self.create_pdf(data.get('ai_report',''),data.get('inspection_md',''),data.get('thermal_md',''))
        print('Saved:',self.output_path)
        return {'pdf_path':self.output_path}

if __name__=='__main__':
    sample={'ai_report':'Wall dampness due to crack ingress. Immediate waterproofing advised.','inspection_md':'Observed cracks on wall\n![](sample1.png)','thermal_md':'Thermal hotspot near wet wall\n![](sample2.png)'}
    ReportGenerator().run(sample)
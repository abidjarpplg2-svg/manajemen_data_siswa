from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape,A4
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet
def export_excel(path,rows):
 wb=Workbook();ws=wb.active;ws.title="Data Siswa"
 ws.append(["LAPORAN DATA SISWA"]);ws.merge_cells("A1:F1");ws["A1"].font=Font(bold=True,size=15,color="FFFFFF");ws["A1"].fill=PatternFill("solid",fgColor="1E40AF")
 ws.append(["NIS","Nama","Kelas","Jurusan","Jenis Kelamin","Telepon"])
 for c in ws[2]:c.font=Font(bold=True,color="FFFFFF");c.fill=PatternFill("solid",fgColor="2563EB")
 for r in rows:ws.append(list(r))
 for i in range(1,7):ws.column_dimensions[get_column_letter(i)].width=20
 ws.freeze_panes="A3";wb.save(path)
def export_pdf(path,rows):
 doc=SimpleDocTemplate(path,pagesize=landscape(A4),rightMargin=24,leftMargin=24,topMargin=24,bottomMargin=24)
 styles=getSampleStyleSheet();story=[Paragraph("Laporan Data Siswa",styles["Title"]),Spacer(1,14)]
 data=[["NIS","Nama","Kelas","Jurusan","Jenis Kelamin","Telepon"]]+[list(r) for r in rows]
 table=Table(data,repeatRows=1,colWidths=[75,150,90,110,95,100])
 table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2563eb")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("GRID",(0,0),(-1,-1),.4,colors.HexColor("#cbd5e1")),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#eff6ff")]),("PADDING",(0,0),(-1,-1),7)]))
 story.append(table);doc.build(story)

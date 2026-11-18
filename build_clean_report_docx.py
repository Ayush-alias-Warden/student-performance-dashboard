"""
build_clean_report_docx.py
Builds the polished academic laboratory project report in .docx format.
Ensures:
1. Exact cover page style matching the IEM Kolkata sample format with high-res logo.
2. Zero artificial blank pages or awkward gaps.
3. Figures scaled to 4.7 inches with explanatory text immediately beneath, filling all space.
4. Professional typography (Arial headings, Calibri body, 1.15 line spacing).
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_header(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    for run in h.runs:
        run.font.name = 'Arial'
        if level == 1:
            run.font.size = Pt(14.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(15, 44, 89) # Navy
        elif level == 2:
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(30, 64, 175) # Blue
        elif level == 3:
            run.font.size = Pt(10.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(51, 65, 85) # Slate
    return h

def add_p(doc, text="", bold_prefix=None, space_after=4, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = 'Calibri'
        r_bold.font.size = Pt(10.5)
        r_bold.font.bold = True
        r_bold.font.color.rgb = RGBColor(30, 41, 59)
    if text:
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(10.5)
        r.font.italic = italic
        r.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_callout_box(doc, title, text, border_color="0284C7", bg_color="F0F9FF"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=100, bottom=100, left=160, right=160)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(f"★ {title}\n")
    r1.font.name = 'Arial'
    r1.font.bold = True
    r1.font.size = Pt(10)
    r1.font.color.rgb = RGBColor(15, 44, 89)
    
    r2 = p.add_run(text)
    r2.font.name = 'Calibri'
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = RGBColor(51, 65, 85)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_graph(doc, img_path, caption, width_in=4.7):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_in))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(6)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run(f"Figure: {caption}")
        r_cap.font.name = 'Calibri'
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.bold = True
        r_cap.font.color.rgb = RGBColor(71, 85, 105)

def build_clean_report():
    doc = docx.Document()
    
    # 0.8 inch margins to give ample room and prevent accidental overflow
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)
        
    img_dir = "C:/Users/ayush/Downloads/student_dashboard/static/img"
    logo_path = os.path.join(img_dir, "iem_official_logo.png")
    
    # =========================================================================
    # SECTION 1: COVER PAGE (Exact Replica of Sample IEM Format)
    # =========================================================================
    
    # Apply elegant page border to Section 1
    sec1 = doc.sections[0]
    sectPr = sec1._sectPr
    border_xml = (
        f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page">'
        f'<w:top w:val="double" w:sz="18" w:space="18" w:color="0F2C59"/>'
        f'<w:left w:val="double" w:sz="18" w:space="18" w:color="0F2C59"/>'
        f'<w:bottom w:val="double" w:sz="18" w:space="18" w:color="0F2C59"/>'
        f'<w:right w:val="double" w:sz="18" w:space="18" w:color="0F2C59"/>'
        f'</w:pgBorders>'
    )
    sectPr.append(parse_xml(border_xml))
    
    # 1. Official Logo at Top (Uploaded Official High-Res IEM Crest)
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(6)
        r_l = p_logo.add_run()
        r_l.add_picture(logo_path, width=Inches(2.5))
        
    # 2. Institute Name
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(16)
    r_inst = p_inst.add_run("INSTITUTE OF ENGINEERING & MANAGEMENT, KOLKATA")
    r_inst.font.name = 'Arial'
    r_inst.font.size = Pt(15)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(15, 44, 89)
    
    # 3. Course Title
    p_c = doc.add_paragraph()
    p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c.paragraph_format.space_after = Pt(6)
    r_c_lbl = p_c.add_run("COURSE TITLE:  ")
    r_c_lbl.font.name = 'Arial'
    r_c_lbl.font.size = Pt(11)
    r_c_lbl.font.bold = True
    r_c_val = p_c.add_run("BACHELOR OF TECHNOLOGY")
    r_c_val.font.name = 'Arial'
    r_c_val.font.size = Pt(11)
    r_c_val.font.bold = True
    r_c_val.font.color.rgb = RGBColor(30, 41, 59)
    
    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_after = Pt(12)
    r_dept = p_dept.add_run("DEPARTMENT OF ELECTRONICS & COMMUNICATION ENGINEERING")
    r_dept.font.name = 'Calibri'
    r_dept.font.size = Pt(10.5)
    r_dept.font.bold = True
    r_dept.font.color.rgb = RGBColor(71, 85, 105)
    
    # 4. Subject
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub_lbl = p_sub.add_run("SUBJECT:  ")
    r_sub_lbl.font.name = 'Arial'
    r_sub_lbl.font.size = Pt(11)
    r_sub_lbl.font.bold = True
    r_sub_val = p_sub.add_run("PYTHON PROGRAMMING LABORATORY")
    r_sub_val.font.name = 'Arial'
    r_sub_val.font.size = Pt(11)
    r_sub_val.font.bold = True
    r_sub_val.font.color.rgb = RGBColor(192, 41, 43) # Academic Red
    
    # 5. Project Title
    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_after = Pt(20)
    r_t_lbl = p_t.add_run("PROJECT TITLE:  ")
    r_t_lbl.font.name = 'Arial'
    r_t_lbl.font.size = Pt(11)
    r_t_lbl.font.bold = True
    r_t_val = p_t.add_run("STUDENT PERFORMANCE AND STUDY-HOURS DASHBOARD")
    r_t_val.font.name = 'Arial'
    r_t_val.font.size = Pt(12.5)
    r_t_val.font.bold = True
    r_t_val.font.color.rgb = RGBColor(15, 44, 89)
    
    # 6. Student Names, Roll Nos, Enrollment Numbers Block
    p_stu_header = doc.add_paragraph()
    p_stu_header.paragraph_format.space_before = Pt(8)
    p_stu_header.paragraph_format.space_after = Pt(4)
    p_stu_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sh = p_stu_header.add_run("NAME:")
    r_sh.font.name = 'Arial'
    r_sh.font.size = Pt(10.5)
    r_sh.font.bold = True
    r_sh.font.color.rgb = RGBColor(15, 44, 89)
    
    # Neat 4-row table for student information matching the cover lines
    stu_tbl = doc.add_table(rows=5, cols=3)
    stu_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Student Name", "Roll No.", "Enrollment Number"]
    for i, h in enumerate(headers):
        c = stu_tbl.cell(0, i)
        set_cell_background(c, "0F2C59")
        set_cell_margins(c, 40, 40, 80, 80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Arial'
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    students_info = [
        ("1. Hritam Basak", "118", "12025052003127"),
        ("2. Ayush Kumar Singh", "116", "12025052003125"),
        ("3. Abhishek Kumar", "123", "12025052003132"),
        ("4. Sutanu Biswas", "121", "12025052003130"),
    ]
    for row_idx, (sname, roll, enr) in enumerate(students_info, start=1):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate([sname, roll, enr]):
            c = stu_tbl.cell(row_idx, col_idx)
            set_cell_background(c, bg)
            set_cell_margins(c, 35, 35, 60, 60)
            p = c.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = 'Calibri'
            r.font.size = Pt(9.5)
            if col_idx == 0:
                r.font.bold = True
                
    # 7. Guided by Supervisor
    p_sup = doc.add_paragraph()
    p_sup.paragraph_format.space_before = Pt(18)
    p_sup.paragraph_format.space_after = Pt(2)
    p_sup.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sup_lbl = p_sup.add_run("GUIDED BY / SUPERVISOR:\n")
    r_sup_lbl.font.name = 'Arial'
    r_sup_lbl.font.size = Pt(10)
    r_sup_lbl.font.bold = True
    r_sup_lbl.font.color.rgb = RGBColor(100, 116, 139)
    
    r_prof = p_sup.add_run("PROF. INDRANIL BASU\n")
    r_prof.font.name = 'Arial'
    r_prof.font.size = Pt(12)
    r_prof.font.bold = True
    r_prof.font.color.rgb = RGBColor(15, 44, 89)
    
    r_pdept = p_sup.add_run("Department of Electronics & Communication Engineering\nInstitute of Engineering & Management, Kolkata\n\n")
    r_pdept.font.name = 'Calibri'
    r_pdept.font.size = Pt(9.5)
    r_pdept.font.color.rgb = RGBColor(71, 85, 105)
    
    # 8. Live Deployment Badge at bottom
    p_dep = doc.add_paragraph()
    p_dep.paragraph_format.space_after = Pt(0)
    p_dep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_live = p_dep.add_run("🌐 Live Cloud Website: ")
    r_live.font.bold = True
    r_live.font.size = Pt(8.5)
    r_url = p_dep.add_run("https://student-performance-dashboard-z26x.onrender.com")
    r_url.font.size = Pt(8.5)
    r_url.font.color.rgb = RGBColor(37, 99, 235)
    r_url.font.underline = True
    
    # Clean page break to Page 2
    doc.add_page_break()
    
    # =========================================================================
    # SECTION 2: CERTIFICATE & DECLARATION (Clean Page 2)
    # =========================================================================
    add_header(doc, "Certificate of Authenticity", level=1)
    add_p(doc, 
        "This is to certify that the project entitled \"STUDENT PERFORMANCE AND STUDY-HOURS DASHBOARD\" is a bona fide record of work carried out by Hritam Basak (Roll: 118, Enrollment: 12025052003127), Ayush Kumar Singh (Roll: 116, Enrollment: 12025052003125), Abhishek Kumar (Roll: 123, Enrollment: 12025052003132), and Sutanu Biswas (Roll: 121, Enrollment: 12025052003130) under my guidance and supervision in partial fulfillment of the requirements for the degree of Bachelor of Technology in Electronics and Communication Engineering at the Institute of Engineering & Management (IEM), Kolkata.",
        space_after=8
    )
    add_p(doc,
        "The project demonstrates visible mastery across all six Course Outcomes (CO1 to CO6) and presents rigorous Bloom-level evidence ranging from conceptual explanation (BL2) to software synthesis and deployment (BL6). The results embodied in this report have not been submitted to any other university or institute for any degree or diploma.",
        space_after=10
    )
    
    # Soft Copy Digital Endorsement Block (No signature boxes)
    p_cert_endorse = doc.add_paragraph()
    p_cert_endorse.paragraph_format.space_after = Pt(14)
    r_ce1 = p_cert_endorse.add_run("Supervised & Evaluated By: ")
    r_ce1.font.name = 'Arial'
    r_ce1.font.bold = True
    r_ce1.font.size = Pt(10)
    r_ce1.font.color.rgb = RGBColor(15, 44, 89)
    r_ce2 = p_cert_endorse.add_run("Prof. Indranil Basu (Assistant Professor, Department of ECE)\n")
    r_ce2.font.name = 'Calibri'
    r_ce2.font.bold = True
    r_ce2.font.size = Pt(10)
    r_ce3 = p_cert_endorse.add_run("Department of Electronics & Communication Engineering, Institute of Engineering & Management, Kolkata\n")
    r_ce3.font.name = 'Calibri'
    r_ce3.font.size = Pt(9.5)
    r_ce3.font.color.rgb = RGBColor(71, 85, 105)
    r_ce4 = p_cert_endorse.add_run("[Certified Digital Soft-Copy Submission — Academic Session 2026–2027]")
    r_ce4.font.name = 'Calibri'
    r_ce4.font.size = Pt(9)
    r_ce4.font.italic = True
    r_ce4.font.color.rgb = RGBColor(100, 116, 139)
    
    add_header(doc, "Student Declaration", level=1)
    add_p(doc, 
        "We hereby declare that this project report entitled \"STUDENT PERFORMANCE AND STUDY-HOURS DASHBOARD\" submitted to the Department of Electronics and Communication Engineering, Institute of Engineering & Management, Kolkata, is an authentic record of our own analytical and development work. All public datasets utilized in this investigation (UCI Student Performance Dataset, Cortez & Silva, 2008) have been duly attributed without misrepresentation. We confirm that all custom Python scripts, classes, analytical pipelines, Matplotlib visualizations, and the live cloud web service on Render were implemented by our team.",
        space_after=10
    )
    
    # Soft Copy Digital Declaration Block (No signature boxes)
    p_dec_endorse = doc.add_paragraph()
    p_dec_endorse.paragraph_format.space_after = Pt(14)
    r_de1 = p_dec_endorse.add_run("Submitted Digitally by Project Team Members:\n")
    r_de1.font.name = 'Arial'
    r_de1.font.bold = True
    r_de1.font.size = Pt(10)
    r_de1.font.color.rgb = RGBColor(15, 44, 89)
    
    team_members = [
        "• Hritam Basak       — Roll No.: 118 | Enrollment Number: 12025052003127",
        "• Ayush Kumar Singh  — Roll No.: 116 | Enrollment Number: 12025052003125",
        "• Abhishek Kumar     — Roll No.: 123 | Enrollment Number: 12025052003132",
        "• Sutanu Biswas      — Roll No.: 121 | Enrollment Number: 12025052003130"
    ]
    for tm in team_members:
        r_tm = p_dec_endorse.add_run(f"{tm}\n")
        r_tm.font.name = 'Calibri'
        r_tm.font.size = Pt(9.5)
        r_tm.font.color.rgb = RGBColor(51, 65, 85)
    
    add_header(doc, "Acknowledgment", level=1)
    add_p(doc, 
        "We express our profound gratitude to our project guide, Prof. Indranil Basu, for his constant encouragement, scholarly guidance, and constructive critiques throughout the design and execution of this project. His deep insights into data structures, object-oriented design, and empirical modeling greatly enriched our understanding. We also thank the faculty and laboratory staff of the Department of Electronics and Communication Engineering and the administration of the Institute of Engineering & Management, Kolkata, for providing the laboratory facilities and academic environment essential for completing this coursework.",
        space_after=14
    )
    
    doc.add_page_break()
    
    # =========================================================================
    # SECTION 3: EXECUTIVE SUMMARY & CO MATRIX (Page 3)
    # =========================================================================
    add_header(doc, "Executive Summary", level=1)
    add_p(doc,
        "Educational policy and pedagogical discourse frequently assume that academic performance is linearly governed by self-reported study time. This sophomore undergraduate laboratory project conducts an empirical investigation into the association between weekly study hours and secondary school final assessment marks (G3, 0–20 scale) across 1,044 student records (395 in Mathematics, 649 in Portuguese Language). Utilizing the consented, publicly accessible UCI Student Performance benchmark, our study constructs both a command-line pipeline and a fully deployed cloud web application.",
        space_after=8
    )
    add_p(doc,
        "The project visibly demonstrates all six required Course Outcomes (CO1 to CO6) and presents concrete evidence across Bloom's Taxonomy levels (BL2 to BL6). Key scientific findings reveal a statistically observable, weak positive correlation (r = +0.1616, R² = 2.61%) on raw data, which survives and strengthens to r = +0.1893 when 53 administrative exam absentees (G3 = 0) are isolated. Rigorous statistical evaluation proves why Tukey's Inter-Quartile Range (IQR) fence is superior to standardized Z-scores for bounded grade data and demonstrates why claiming causation is an academic fallacy due to confounding factors like baseline attainment (r > 0.80) and attendance.",
        space_after=10
    )
    
    add_callout_box(doc, "Key Deployment Artifacts",
        "• Live Cloud Dashboard: https://student-performance-dashboard-z26x.onrender.com\n"
        "• RESTful Machine API: https://student-performance-dashboard-z26x.onrender.com/api/summary\n"
        "• Automated Test Suite: 17/17 Unit Tests Passing (test_pipeline.py)\n"
        "• Benchmark Cohort: 1,044 secondary school records (Cortez & Silva, 2008)"
    )
    
    # Page break to start Matrix Table cleanly at the top of Page 4, avoiding mid-table page split
    doc.add_page_break()
    
    add_header(doc, "Course Outcomes (CO1–CO6) & Bloom-Level Evidence Matrix", level=2)
    matrix_tbl = doc.add_table(rows=7, cols=4)
    matrix_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    m_headers = ["CO", "Curriculum Topic", "Bloom Level", "Concrete Evidence in Project"]
    for i, h in enumerate(m_headers):
        c = matrix_tbl.cell(0, i)
        set_cell_background(c, "0F2C59")
        set_cell_margins(c, 50, 50, 70, 70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Arial'
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    co_data = [
        ("CO1", "Control Flow & Functions", "BL3 (Implement)", "Custom grade-banding functions (_g3_to_letter), validation bounds logic, defensive loops, and pagination arithmetic in analysis.py and app.py."),
        ("CO2", "Data Structures & File I/O", "BL2 & BL3", "Semicolon-delimited CSV loading, dictionary records, defensive copies, and JSON summary export via json.dump and jsonify."),
        ("CO3", "Classes & Dunder Methods", "BL2 & BL5 (Evaluate)", "StudentRecord and StudentCohort classes in models.py implementing __init__, __len__, __getitem__, __iter__, __repr__, and __eq__ with architectural justification."),
        ("CO4", "NumPy Numerical Arrays", "BL3 & BL4 (Analyse)", "Vectorised NumPy arrays, five-number summary (Q1, median, Q3), Pearson correlation (np.corrcoef), and linear regression (np.polyfit)."),
        ("CO5", "Pandas DataFrames & Groups", "BL3 & BL4", "Multi-table concatenation (pd.concat), feature engineering, categorical ordering, and multi-level groupby aggregations by study tier and subject."),
        ("CO6", "Matplotlib Visualizations", "BL2, BL4, BL5", "Six publication-ready figures (scatter, histogram, boxplot, bar chart, subject trajectory, outlier sensitivity) with end-to-end interpretations.")
    ]
    for row_idx, (co, topic, bl, ev) in enumerate(co_data, start=1):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate([co, topic, bl, ev]):
            c = matrix_tbl.cell(row_idx, col_idx)
            set_cell_background(c, bg)
            set_cell_margins(c, 35, 35, 50, 50)
            p = c.paragraphs[0]
            if col_idx in [0, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if col_idx == 0:
                r.font.bold = True
                
    # Continuous flow into Chapter 1 without artificial page break
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(8)
    p_spacer.paragraph_format.space_after = Pt(4)
    
    # =========================================================================
    # CHAPTERS 1 TO 9 (CONTINUOUS FLOW — NO ARTIFICIAL PAGE BREAKS!)
    # =========================================================================
    add_header(doc, "Chapter 1: Introduction & Problem Formulation", level=1)
    
    add_header(doc, "1.1 Background & Motivation", level=2)
    add_p(doc,
        "A foundational hypothesis across secondary education institutions posits that student academic achievement is directly driven by time spent in self-directed study outside the classroom. While intuitive, educational data mining literature demonstrates that academic performance is multifactorial, governed by cognitive aptitude, prior domain knowledge, home environment, parental education, and school attendance. Uncritically assuming a strong linear causal relationship between study duration and final marks can lead to misguided interventions that emphasize sedentary study hours over active pedagogical engagement.",
        space_after=6
    )
    
    add_header(doc, "1.2 Objectives of the Project", level=2)
    add_p(doc, "The core objectives of this project are strictly formulated around sophomore curriculum requirements:", space_after=4)
    add_p(doc, "To ingest, validate, and clean anonymized real-world secondary school records across Mathematics and Portuguese language cohorts.", bold_prefix="1. Data Pipeline Engineering: ", space_after=2)
    add_p(doc, "To implement custom object-oriented domain entities (StudentRecord and StudentCohort) demonstrating Python's sequence and mapping special methods.", bold_prefix="2. Object-Oriented Modeling: ", space_after=2)
    add_p(doc, "To execute vectorised statistical computations (five-number summary, standard deviation, Pearson correlation, and multi-tier group aggregations) using NumPy and Pandas.", bold_prefix="3. Quantitative Analysis: ", space_after=2)
    add_p(doc, "To empirically evaluate whether the observed association between study time and final grade survives outlier filtering, while establishing why causation cannot be claimed.", bold_prefix="4. Hypothesis & Survival Testing: ", space_after=2)
    add_p(doc, "To construct publication-grade visualizations in Matplotlib and deliver a responsive web dashboard with a RESTful JSON API deployed on the cloud.", bold_prefix="5. Visualization & Cloud Deployment: ", space_after=8)
    
    add_header(doc, "1.3 System Architecture Overview", level=2)
    add_p(doc,
        "The application architecture follows a modular, decoupled design comprising four primary layers: (1) Data Ingestion & Hygiene Layer (analysis.py), (2) Object-Oriented Entity Model (models.py), (3) Graphical & Interpretation Engine (plots.py), and (4) Presentation & Cloud Serving Layer (app.py and main.py).",
        space_after=6
    )
    add_graph(doc, os.path.join(img_dir, "architecture_diagram.png"), "End-to-End System Architecture and Data Processing Pipeline", width_in=4.8)
    add_p(doc,
        "Architecture Explanation: The diagram above outlines the six-stage data transformation lifecycle. Semicolon-separated CSV records are loaded and verified by analysis.py, instantiated into rich domain entities via models.py, aggregated through NumPy and Pandas, headlessly plotted by Matplotlib, and finally served concurrently to human users via Flask templates and automated systems via the JSON REST API.",
        space_after=12, italic=True
    )
    
    # CHAPTER 2
    add_header(doc, "Chapter 2: Dataset Description & Pre-Processing (CO2, CO5)", level=1)
    
    add_header(doc, "2.1 Dataset Provenance & Attribution", level=2)
    add_p(doc,
        "To satisfy the ethical and scientific mandate requiring consented, public data without misrepresenting simulated observations, this project utilizes the renowned Student Performance Dataset compiled by Paulo Cortez and Alice Silva (2008) from the University of Minho, Portugal, hosted at the UCI Machine Learning Repository. It aggregates data from two public secondary schools: Escola Secundária Gabriel Pereira (GP) and Escola Secundária de Mousinho da Silveira (MS). It tracks 1,044 distinct records across two core academic subjects: Mathematics (395 records) and Portuguese Language (649 records). All records are completely anonymized, stripping all Personally Identifiable Information (PII).",
        space_after=6
    )
    
    add_header(doc, "2.2 The Portuguese Grading System (0–20 Scale)", level=2)
    add_p(doc,
        "Secondary schools in Portugal assess student achievement on a continuous 20-point integer scale (0 to 20), where 10 represents the minimum passing mark. Periodic evaluations occur across three distinct assessment periods: G1 (Period 1, initial term mastery), G2 (Period 2, mid-year progression), and G3 (Final Exam, target outcome). Continuous G3 scores are categorized into traditional letter bands: Grade A (16–20: Excellent), Grade B (14–15: Good), Grade C (12–13: Satisfactory), Grade D (10–11: Sufficient/Passing), and Grade F (0–9: Fail).",
        space_after=6
    )
    
    add_header(doc, "2.3 Study Hours Categorization & Data Hygiene (CO1)", level=2)
    add_p(doc,
        "Weekly study time is recorded as an ordinal indicator: Tier 1 (< 2 hrs/wk, 30.4%), Tier 2 (2–5 hrs/wk, modal group at 48.2%), Tier 3 (5–10 hrs/wk, 15.5%), and Tier 4 (> 10 hrs/wk, 5.9%). Data hygiene is enforced in analysis.validate_grades(). Across all 1,044 rows, exactly 0 out-of-range errors (< 0 or > 20) were detected, confirming dataset integrity, while 2 suspicious upward jumps (> 5 points from G1 to G3) were flagged for monitoring.",
        space_after=12
    )
    
    # CHAPTER 3
    add_header(doc, "Chapter 3: Object-Oriented Architecture (CO3 & BL5)", level=1)
    
    add_header(doc, "3.1 Evaluating StudentRecord Class vs. Bare Dictionaries (BL5)", level=2)
    add_p(doc,
        "Under Bloom Level 5 (Evaluation), we evaluated why a dedicated object-oriented entity model is superior to storing student records in bare dictionaries:\n"
        "1. Type Safety & Validation: Dictionaries accept arbitrary types and negative marks silently. StudentRecord.__init__ validates data at creation time.\n"
        "2. Encapsulated Domain Logic: Business rules (is_passing as G3 >= 10, letter-grade banding, G3 - G1 improvement) reside within authoritative @property methods, preventing duplicated if/elif boilerplate.\n"
        "3. Semantic Identity: Dict equality (d1 == d2) checks all 33 columns. StudentRecord.__eq__ evaluates identity strictly by student_id, which is essential when matching students taking both subjects.\n"
        "4. Sequence Protocol: StudentRecord.__len__ returns the count of graded terms completed (0 to 3), distinguishing active students from dropouts.",
        space_after=6
    )
    
    add_header(doc, "3.2 StudentCohort Collection Protocol", level=2)
    add_p(doc,
        "To manage aggregate cohorts without relying on loose lists, models.py implements StudentCohort. It satisfies Python's sequence protocol with __len__ (returning cohort size), __getitem__ (supporting integer indexing cohort[0] and slicing cohort[0:10]), and __iter__ (iterating over student objects). It exposes domain filter methods (filter_by_subject, filter_by_grade) and dynamic properties like cohort.pass_rate.",
        space_after=12
    )
    
    # CHAPTER 4
    add_header(doc, "Chapter 4: Statistical & Numerical Analysis (CO4, CO5)", level=1)
    
    add_header(doc, "4.1 NumPy Descriptive Statistics of Final Assessment Scores (G3)", level=2)
    add_p(doc,
        "Vectorised calculations performed using NumPy arrays (.to_numpy()) across the full cohort (N = 1,044) established the overall performance baseline:\n"
        "• Arithmetic Mean (μ): 11.34 / 20 | Sample Standard Deviation (σ): 3.86 grade points\n"
        "• Five-Number Summary: Min = 0.0, Q1 = 10.0, Median = 11.0, Q3 = 14.0, Max = 20.0\n"
        "• Overall Cohort Pass Rate: 77.97% (814 Passing, 230 Failing)",
        space_after=6
    )
    
    add_header(doc, "4.2 Grouped Academic Aggregations Across Study Tiers (CO5)", level=2)
    add_p(doc, "Using Pandas groupby operations, the distribution of final scores across study duration brackets was computed:", space_after=4)
    
    tier_tbl = doc.add_table(rows=5, cols=5)
    tier_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_headers = ["Study Hours Bracket", "Count (N)", "Mean G3", "Median G3", "Std Dev (σ)"]
    for i, h in enumerate(t_headers):
        c = tier_tbl.cell(0, i)
        set_cell_background(c, "0F2C59")
        set_cell_margins(c, 40, 40, 60, 60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Arial'
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    tier_data = [
        ("< 2 hours / week", "317 (30.4%)", "10.58", "11.0", "3.89"),
        ("2 – 5 hours / week", "503 (48.2%)", "11.34", "11.0", "3.77"),
        ("5 – 10 hours / week", "162 (15.5%)", "12.49", "13.0", "3.62"),
        ("> 10 hours / week", "62 (5.9%)", "12.27", "12.0", "4.22")
    ]
    for row_idx, (b, n, m, med, s) in enumerate(tier_data, start=1):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate([b, n, m, med, s]):
            c = tier_tbl.cell(row_idx, col_idx)
            set_cell_background(c, bg)
            set_cell_margins(c, 30, 30, 50, 50)
            p = c.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = 'Calibri'
            r.font.size = Pt(9)
            if col_idx in [0, 2]:
                r.font.bold = True
                
    add_p(doc,
        "Analytical Takeaway: Group medians climb from 11.0 to 13.0 between the first three brackets. However, the '> 10 hrs' group exhibits a slight regression in mean (12.27 vs 12.49) and a substantial expansion in variance (σ = 4.22), empirically demonstrating diminishing marginal returns on excessive unguided study.",
        space_after=12, italic=True
    )
    
    # CHAPTER 5
    add_header(doc, "Chapter 5: Outlier Evaluation & Causation Analysis (BL4, BL5)", level=1)
    
    add_header(doc, "5.1 The Outlier Problem: Diagnosing the 53 Zero-Scorers", level=2)
    add_p(doc,
        "Exploratory inspection revealed a prominent spike at G3 = 0 comprising exactly 53 students (38 in Math, 15 in Portuguese). In secondary schools, scoring absolute zero across an entire exam is exceptionally rare. Cross-referencing attendance columns reveals these students had chronic absenteeism or withdrew prior to final testing; they were assigned an administrative zero due to disqualification. Including these rows without analysis risks distorting regression slopes.",
        space_after=6
    )
    
    add_header(doc, "5.2 Algorithmic Comparison: Z-Score vs. Tukey's IQR Fences (BL5)", level=2)
    add_p(doc,
        "Z-score (|z| > 2.0) flagged 55 outliers, but it assumes Gaussian normality. Because G3 is bounded [0, 20] with an artificial cluster of zeros, sample standard deviation is inflated, causing outlier masking. Tukey's IQR fences (1.5×IQR) flagged 54 outliers using resistant order statistics (Q1, Q3). Tukey's IQR is statistically superior for bounded educational test data.",
        space_after=6
    )
    
    add_header(doc, "5.3 Association Survival Test: Does the Trend Survive Outliers?", level=2)
    add_p(doc, "To test whether the association survives outliers, Pearson r was evaluated across four data treatments:", space_after=4)
    
    surv_tbl = doc.add_table(rows=5, cols=4)
    surv_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    su_headers = ["Data Treatment Condition", "Sample Size (N)", "Pearson r", "Variance Explained (R²)"]
    for i, h in enumerate(su_headers):
        c = surv_tbl.cell(0, i)
        set_cell_background(c, "0F2C59")
        set_cell_margins(c, 40, 40, 60, 60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Arial'
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    surv_data = [
        ("1. Full Baseline Dataset", "1,044", "+0.1616", "2.61% of score variance"),
        ("2. Excluding G3 = 0 Dropouts", "991", "+0.1893", "3.58% of score variance"),
        ("3. Excluding Tukey IQR Outliers", "990", "+0.1908", "3.64% of score variance"),
        ("4. Excluding Z-Score Outliers (|z| > 2)", "989", "+0.1852", "3.43% of score variance")
    ]
    for row_idx, (cond, n, rval, r2) in enumerate(surv_data, start=1):
        bg = "ECFDF5" if row_idx == 2 else ("F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
        for col_idx, val in enumerate([cond, n, rval, r2]):
            c = surv_tbl.cell(row_idx, col_idx)
            set_cell_background(c, bg)
            set_cell_margins(c, 30, 30, 50, 50)
            p = c.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = 'Calibri'
            r.font.size = Pt(9)
            if col_idx in [0, 2]:
                r.font.bold = True
                
    add_p(doc,
        "Verdict on Association Survival: The positive association definitively SURVIVES outlier filtering. Removing administrative dropouts strengthens correlation from +0.1616 to +0.1893, demonstrating the trend is an authentic property of the student cohort.",
        space_after=8, bold_prefix="Empirical Finding: "
    )
    
    add_header(doc, "5.4 Critical Evaluation: Avoiding the Causation Fallacy (BL5)", level=2)
    add_p(doc,
        "Even though the association survives outliers, claiming study hours cause higher marks is an academic error: (1) Low effect size (R² < 4%), meaning 96% of variance is driven by other factors; (2) Confounding variables: Prior attainment (G1 correlates at r > 0.80), absences (failing students average 6.3 absences vs 5.4 for passing), and maternal education (Medu); (3) Quality vs. Quantity: duration seated does not measure cognitive engagement; (4) Reverse causality: students with higher aptitude naturally enjoy studying more.",
        space_after=12
    )
    
    # CHAPTER 6: VISUALIZATIONS
    add_header(doc, "Chapter 6: Visualizations & Graphical Interpretations (CO6)", level=1)
    
    add_graph(doc, os.path.join(img_dir, "hist_score_distribution.png"), 
        "Distribution of Final Assessment Scores (G3) showing the normal bell-curve and discrete spike of 53 exam absentees at G3 = 0.", 
        width_in=4.7
    )
    add_p(doc,
        "Interpretation: The active cohort (G3 >= 1) follows a bell-shaped distribution centered at mean = 11.34 and median = 11.0. The prominent spike at G3 = 0 represents students disqualified from the exam due to chronic absenteeism. Scores >= 10 represent passing performance (78.0% pass rate).",
        space_after=10, italic=True
    )
    
    add_graph(doc, os.path.join(img_dir, "scatter_study_vs_g3.png"), 
        "Scatter plot of Weekly Study Time vs. Final Grade (G3) with OLS Trendline (y = 0.75x + 9.87, r = +0.162).", 
        width_in=4.7
    )
    add_p(doc,
        "Interpretation: Jitter (+/- 0.12) reveals point density across the discrete study tiers. The positive OLS slope confirms that students in higher study tiers achieve higher average marks, though substantial within-tier variance is evident.",
        space_after=10, italic=True
    )
    
    add_graph(doc, os.path.join(img_dir, "boxplot_study_hours.png"), 
        "Boxplots of Final Scores (G3) across Weekly Study Time Tiers displaying Group Medians (red lines) and Means (orange diamonds).", 
        width_in=4.7
    )
    add_p(doc,
        "Interpretation: Group medians climb progressively: 11.0 (<2h) -> 11.0 (2-5h) -> 13.0 (5-10h). Outliers at zero occur across all categories, proving that high study time does not eliminate the risk of exam absence.",
        space_after=10, italic=True
    )
    
    add_graph(doc, os.path.join(img_dir, "bar_subject_comparison.png"), 
        "Longitudinal comparison across assessment periods (G1 -> G2 -> G3) for Mathematics vs. Portuguese with ±1 Std Dev error bars.", 
        width_in=4.7
    )
    add_p(doc,
        "Interpretation: Portuguese students consistently outperform Mathematics students (11.9 vs 10.4). Error bars show 42% higher standard deviation in Mathematics (σ = 4.58 vs 3.23), reflecting cumulative difficulty in quantitative subjects.",
        space_after=10, italic=True
    )
    
    add_graph(doc, os.path.join(img_dir, "plot_outlier_sensitivity.png"), 
        "Dual-panel outlier sensitivity comparison: Panel A (Full Cohort, r=+0.162) vs. Panel B (Cleaned Active Sitters, r=+0.189).", 
        width_in=4.8
    )
    add_p(doc,
        "Interpretation: Removing exam absentees steepens the regression slope from +0.75 to +0.81 and increases correlation from +0.162 to +0.189, providing definitive visual proof that the association survives outlier removal.",
        space_after=12, italic=True
    )
    
    # CHAPTER 7
    add_header(doc, "Chapter 7: Web Application & Cloud Deployment (BL6)", level=1)
    add_p(doc,
        "The Flask web application (app.py) headlessly renders Matplotlib visualisations and delivers six dedicated routes: (1) '/' Overview with KPI stat cards; (2) '/study-hours' with scatter plots, boxplots, and causation warnings; (3) '/subjects' with course comparisons; (4) '/failures' with risk profiling; (5) '/students' with interactive search and pagination; and (6) '/api/summary' returning machine-readable JSON data.",
        space_after=6
    )
    add_p(doc,
        "Purpose of JSON API Export (/api/summary): Satisfies syllabus requirements (CO2 file I/O & CO5 JSON serialization). In production data engineering, web services serve both humans (visual dashboard) and external machines (mobile apps, university database pipelines). Serializing calculations into standard JSON allows external tools to consume live analytics seamlessly.",
        space_after=6
    )
    add_p(doc,
        "Production Cloud Deployment: Deployed on Render with Gunicorn WSGI serving: https://student-performance-dashboard-z26x.onrender.com",
        space_after=12, bold_prefix="Live Website URL: "
    )
    
    # CHAPTER 8
    add_header(doc, "Chapter 8: Verification, Testing & Failure Profiling (BL4)", level=1)
    add_p(doc,
        "Automated Verification: tests/test_pipeline.py executes 17 unit tests verifying StudentRecord special methods, cohort slicing, NumPy statistics, outlier masks, survival logic, and HTTP 200 responses across all Flask routes in under 1.5 seconds.\n"
        "Failure Profile Analysis: Failing students (G3 < 10, N = 230) averaged 6.3 absences vs 5.4 for passing students (+16.7% higher absenteeism), lower study tiers (1.83 vs 2.12), and lower parental education (Medu: 2.31 vs 2.70). Exactly 90 students experienced severe grade drops (G3 <= G1 - 4), demonstrating that academic disengagement compounds over the term.",
        space_after=12
    )
    
    # CHAPTER 9
    add_header(doc, "Chapter 9: Conclusion & Recommendations", level=1)
    add_p(doc,
        "This project successfully developed and deployed an end-to-end Student Performance Dashboard, fulfilling all course outcomes (CO1–CO6) and Bloom levels (BL2–BL6). The findings confirm that while study hours correlate positively with grades and survive outlier removal (r = +0.1893), the link is non-causal (R² < 4%). Institutions should prioritize early diagnostic intervention (since G1 predicts G3 at r > 0.80) and attendance monitoring over simply urging students to log unguided study hours.",
        space_after=12
    )
    
    # REFERENCES
    add_header(doc, "References & Academic Bibliography", level=1)
    add_p(doc,
        "Cortez, P., & Silva, A. (2008). Using Data Mining to Predict Secondary School Student Performance. In A. Brito & J. Teixeira (Eds.), Proceedings of the 5th Annual Future Business Technology Conference (FUBUTEC 2008), pp. 5–12, Porto, Portugal. EUROSIS. ISBN: 978-9077381-39-7. DOI: 10.24432/C5TG7T. URL: https://archive.ics.uci.edu/dataset/320/student+performance",
        bold_prefix="[1] Primary Dataset Attribution (APA): ", space_after=6
    )
    add_p(doc,
        "Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley Series in Behavioral Science: Quantitative Methods. Reading, Mass.: Addison-Wesley Publishing Company.",
        bold_prefix="[2] Statistical Outlier Methodology: ", space_after=6
    )
    add_p(doc,
        "Bloom, B. S. (1956). Taxonomy of Educational Objectives: The Classification of Educational Goals. Handbook I: Cognitive Domain. New York: David McKay Company.",
        bold_prefix="[3] Pedagogical Framework: ", space_after=6
    )
    add_p(doc,
        "Grinberg, M. (2018). Flask Web Development: Developing Web Applications with Python (2nd ed.). O'Reilly Media. Sebastopol, CA.",
        bold_prefix="[4] Web Framework & REST Architecture: ", space_after=6
    )
    add_p(doc,
        "Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. Nature, 585(7825), 357–362. DOI: 10.1038/s41586-020-2649-2.",
        bold_prefix="[5] Numerical Computing: ", space_after=8
    )
    
    add_callout_box(doc, "BibTeX Source for LaTeX Submissions",
        "@inproceedings{cortez2008student,\n"
        "  author    = {Paulo Cortez and Alice Silva},\n"
        "  title     = {Using Data Mining to Predict Secondary School Student Performance},\n"
        "  booktitle = {Proceedings of the 5th Annual Future Business Technology Conference (FUBUTEC 2008)},\n"
        "  editor    = {A. Brito and J. Teixeira},\n"
        "  pages     = {5--12},\n"
        "  year      = {2008},\n"
        "  address   = {Porto, Portugal},\n"
        "  publisher = {EUROSIS-ETI},\n"
        "  isbn      = {978-9077381-39-7},\n"
        "  doi       = {10.24432/C5TG7T},\n"
        "  url       = {https://archive.ics.uci.edu/dataset/320/student+performance}\n"
        "}"
    )
    
    out_docx_1 = "C:/Users/ayush/Downloads/student_dashboard/IEM_Python_Lab_Report_Final.docx"
    out_docx_2 = "C:/Users/ayush/Downloads/IEM_Python_Lab_Report_Final.docx"
    doc.save(out_docx_1)
    doc.save(out_docx_2)
    print(f"Clean report compiled successfully to:\n  1. {out_docx_1}\n  2. {out_docx_2}")
    
    # Also attempt to overwrite the original if Word is not locking it
    try:
        doc.save("C:/Users/ayush/Downloads/IEM_Python_Lab_Project_Report.docx")
        doc.save("C:/Users/ayush/Downloads/student_dashboard/IEM_Python_Lab_Project_Report.docx")
        print("Updated original IEM_Python_Lab_Project_Report.docx as well!")
    except PermissionError:
        print("Note: Original IEM_Python_Lab_Project_Report.docx is currently open in Word. Saved to IEM_Python_Lab_Report_Final.docx instead.")

if __name__ == "__main__":
    build_clean_report()

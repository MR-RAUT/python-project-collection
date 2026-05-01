#  AI-Powered Detailed Diagnostic Report (DDR) Generator

##  Overview

The **AI-Powered DDR Generator** is a Python-based system designed to automate the analysis of inspection and thermal reports and generate a structured **Detailed Diagnostic Report (DDR)**.

The system processes raw PDF reports, extracts relevant information (text, images, and metadata), identifies key issues, and produces a clean, professional, client-ready report.

---

##  Key Features

*  **PDF Processing**

  * Supports inspection and thermal reports
  * Extracts structured data using Markdown/JSON conversion

*  **AI-Based Analysis**

  * Identifies defects such as dampness, cracks, leakage, and thermal anomalies
  * Generates root cause analysis and recommendations

*  **Smart Image Handling**

  * Extracts images from reports
  * Filters irrelevant images (logos, duplicates, low-quality)
  * Separates inspection and thermal images
  * Displays only relevant problem-related visuals

*  **Structured Report Generation**

  * Executive Summary
  * Issue Summary Table with severity classification
  * Detailed Findings
  * Thermal Analysis
  * AI Root Cause Analysis
  * Disclaimer

*  **Metadata Extraction**

  * Automatically extracts:

    * Inspection Date
    * Inspector Name
    * Property Details (if available)
  * Supports AI fallback for unstructured formats

*  **Professional PDF Output**

  * Clean layout using ReportLab
  * Header/footer with pagination
  * Organized sections and tables
  * 2×2 image grid layout

---

##  Tech Stack

* **Python**
* **ReportLab** – PDF generation
* **OpenDataLoader PDF** – document extraction
* **Groq (LLaMA 3)** – AI analysis and metadata extraction
* **Regex + Rule-based parsing**

---

##  Project Structure

```
project/
│
├── input/
│   ├── inspection.pdf
│   └── thermal.pdf
│
├── output/
│   ├── inspection.md
│   ├── thermal.md
│   ├── inspection.json
│   ├── thermal.json
│   └── final_report.pdf
│
├── report_generator.py
├── main.py
└── README.md
```

---

##  Installation

```bash
pip install reportlab groq opendataloader-pdf
```

---

## ▶ Usage

### 1. Convert PDF to structured data

```python
import opendataloader_pdf

opendataloader_pdf.convert(
    input_path=["input/inspection.pdf", "input/thermal.pdf"],
    output_dir="output/",
    format="markdown,json"
)
```

---

### 2. Run Report Generator

```python
from report_generator import ReportGenerator

sample = {
    "ai_report": "Generated AI analysis...",
    "inspection_md": open("output/inspection.md").read(),
    "thermal_md": open("output/thermal.md").read()
}

ReportGenerator().run(sample)
```

---

### 3. Output

```
output/final_report.pdf
```

---

##  Report Sections

1. Cover Page
2. Executive Summary
3. Issue Summary Table
4. Inspection Image Evidence
5. Thermal Image Evidence
6. Detailed Findings
7. Thermal Analysis
8. AI Root Cause Analysis
9. Disclaimer

---

##  Limitations

* Metadata extraction depends on report formatting
* Missing values in source documents cannot be inferred
* Image relevance is based on filename and context filtering

---

##  Future Improvements

* Image-to-finding mapping
* Severity visualization (charts/graphs)
* Multi-page dynamic layouts
* Web interface for report generation
* Advanced AI-based defect classification

---

##  License

This project is intended for educational and research purposes.
For commercial use, ensure compliance with third-party libraries and APIs.

---
 Author

**Mahesh Raut**
B.Tech AI & Data Science
Pune, India

---

##  Note

This system is designed to assist inspection workflows.
Final decisions should always be validated by qualified professionals.
S
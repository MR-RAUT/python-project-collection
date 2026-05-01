from src.extractor import PDFExtractor
from src.merger import ReportMerger
from src.analyzer import AIAnalyzer
from src.report_generator import ReportGenerator
import time
start = time.time()
...
print("Completed in", round(time.time()-start,2), "sec")

def main():
    try:
        print("=" * 50)
        print("DDR AI PROJECT STARTED")
        print("=" * 50)

        # STEP 1 - Extract PDFs
        print("\n[1] Extracting PDF data...")
        extractor = PDFExtractor()
        extracted_data = extractor.run()

        # STEP 2 - Merge Findings
        print("\n[2] Merging inspection + thermal findings...")
        merger = ReportMerger(extracted_data)
        merged_result = merger.run()

        # STEP 3 - AI Analysis
        print("\n[3] Running AI root cause analysis...")
        analyzer = AIAnalyzer()
        analysis_result = analyzer.run(merged_result)

        # STEP 4 - Generate Final PDF
        print("\n[4] Generating final DDR report...")
        generator = ReportGenerator()
        final_result = generator.run(analysis_result)

        print("\n" + "=" * 50)
        print("PROJECT COMPLETED SUCCESSFULLY")
        print("Final Report:", final_result["pdf_path"])
        print("=" * 50)

    except Exception as e:
        print("\nERROR:", str(e))


if __name__ == "__main__":
    main()
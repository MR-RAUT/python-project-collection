import os
import json
import shutil
import opendataloader_pdf


class PDFExtractor:
    def __init__(self):
        self.input_dir = "input"
        self.output_dir = "output/extracted"

        os.makedirs(self.output_dir, exist_ok=True)

    def clean_old_output(self):
        """Delete old extracted files"""
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

        os.makedirs(self.output_dir, exist_ok=True)

    def extract_pdfs(self):
        """
        Extract both PDFs into markdown + json
        """
        inspection_path = os.path.join(self.input_dir, "inspection.pdf")
        thermal_path = os.path.join(self.input_dir, "thermal.pdf")

        files = []

        if os.path.exists(inspection_path):
            files.append(inspection_path)

        if os.path.exists(thermal_path):
            files.append(thermal_path)

        if not files:
            raise FileNotFoundError("No PDF files found in input folder.")

        print("Starting PDF extraction...")

        opendataloader_pdf.convert(
            input_path=files,
            output_dir=self.output_dir,
            format="markdown,json"
        )

        print("Extraction completed.")

    def get_file_paths(self):
        """
        Return extracted file paths
        """
        data = {
            "inspection_json": os.path.join(self.output_dir, "inspection.json"),
            "inspection_md": os.path.join(self.output_dir, "inspection.md"),
            "thermal_json": os.path.join(self.output_dir, "thermal.json"),
            "thermal_md": os.path.join(self.output_dir, "thermal.md"),
        }

        return data

    def read_json(self, file_path):
        """
        Read JSON file safely
        """
        if not os.path.exists(file_path):
            return {}

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def read_markdown(self, file_path):
        """
        Read markdown file safely
        """
        if not os.path.exists(file_path):
            return ""

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def run(self):
        """
        Full extraction process
        """
        self.clean_old_output()
        self.extract_pdfs()

        files = self.get_file_paths()

        result = {
            "inspection_json": self.read_json(files["inspection_json"]),
            "inspection_md": self.read_markdown(files["inspection_md"]),
            "thermal_json": self.read_json(files["thermal_json"]),
            "thermal_md": self.read_markdown(files["thermal_md"]),
        }

        return result


# test run
if __name__ == "__main__":
    extractor = PDFExtractor()
    data = extractor.run()

    print("\nInspection Markdown Preview:\n")
    print(data["inspection_md"][:1000])

    print("\nThermal Markdown Preview:\n")
    print(data["thermal_md"][:1000])
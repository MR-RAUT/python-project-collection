import re


class ReportMerger:
    def __init__(self, extracted_data):
        self.inspection_text = extracted_data.get("inspection_md", "")
        self.thermal_text = extracted_data.get("thermal_md", "")

    def clean_text(self, text):
        """
        Remove extra spaces and repeated lines
        """
        lines = text.splitlines()
        clean_lines = []

        seen = set()

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if line.lower() in seen:
                continue

            seen.add(line.lower())
            clean_lines.append(line)

        return "\n".join(clean_lines)

    def split_sections(self, text):
        """
        Convert markdown/text into sections
        """
        sections = re.split(r'\n(?=[A-Z0-9 .,&()/-]{5,}$)', text)

        final_sections = []

        for sec in sections:
            sec = sec.strip()

            if len(sec) > 20:
                final_sections.append(sec)

        return final_sections

    def find_keywords(self, text):
        """
        Detect issue keywords
        """
        keywords = [
            "leakage",
            "dampness",
            "seepage",
            "crack",
            "moisture",
            "tile joint",
            "thermal",
            "hotspot",
            "paint",
            "spalling",
            "corrosion",
            "vegetation",
            "roof",
            "terrace",
            "wall",
            "bathroom",
            "balcony"
        ]

        found = []

        lower = text.lower()

        for word in keywords:
            if word in lower:
                found.append(word)

        return found

    def merge_sections(self):
        """
        Merge inspection + thermal sections
        """
        inspection_sections = self.split_sections(
            self.clean_text(self.inspection_text)
        )

        thermal_sections = self.split_sections(
            self.clean_text(self.thermal_text)
        )

        merged = []

        for sec in inspection_sections:
            merged.append({
                "source": "inspection",
                "text": sec,
                "keywords": self.find_keywords(sec)
            })

        for sec in thermal_sections:
            merged.append({
                "source": "thermal",
                "text": sec,
                "keywords": self.find_keywords(sec)
            })

        return merged

    def create_summary(self, merged_data):
        """
        Make compact combined text for AI
        """
        summary = []

        for item in merged_data:
            summary.append(
                f"[{item['source'].upper()}]\n{item['text']}\n"
            )

        return "\n".join(summary)

    def run(self):
        merged_data = self.merge_sections()

        final_result = {
            "merged_sections": merged_data,
            "combined_text": self.create_summary(merged_data)
        }

        return final_result


# test run
if __name__ == "__main__":
    sample = {
        "inspection_md": """
        BEDROOM WALL
        Dampness observed on wall surface.
        Crack near window.
        """,

        "thermal_md": """
        BEDROOM AREA
        Moisture signature found near wall corner.
        """
    }

    merger = ReportMerger(sample)
    result = merger.run()

    print(result["combined_text"])
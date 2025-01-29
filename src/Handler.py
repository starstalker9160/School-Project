import os, json
import re
import pypdf
DOWNLOADS_PATH = path.join(path.expanduser("~"), "Downloads") #! temporarily using Downloads folder

def handle():
    """Handles the uploaded pdf file and performs operation"""
    with open("uploads/metadata.json", 'r') as f:
        metadata = json.load(f)
        f.close()
    match metadata["operation"]:
        case "split":
            PDFHandler.split(metadata["file name"], int(metadata["operationSpecificInfo"]["splitOnPage"]))
        case "to-docx":
            PDFHandler.to_docx(metadata["file name"])
        case "from-docx":
            PDFHandler.from_docx(metadata["file name"])
        case "merge":
            PDFHandler.merge(metadata["file name"])
    

class PDFHandler:
    @staticmethod
    def split(file_name: str, page_number: int) -> None:
        # relevant functionality
        
        reader = pypdf.PdfReader(f"uploads/{file_name}")
        total_pages = len(reader.pages)
        writer1 = pypdf.PdfWriter()
        writer2 = pypdf.PdfWriter()

        for i in range(total_pages):
            if i < page_number:
                writer1.add_page(reader.pages[i])
            else:
                writer2.add_page(reader.pages[i])
    
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads") #! temporarily using Downloads folder
        output_filename1 = os.path.join(downloads_path, f"{file_name}_part_1.pdf")
        with open(output_filename1, "wb") as output_file1:
            writer1.write(output_file1)
        
        if total_pages > page_number:
            output_filename2 = os.path.join(downloads_path, f"{file_name}_part_2.pdf")
            with open(output_filename2, "wb") as output_file2:
                writer2.write(output_file2)
        
        PDFHandler.cleanup()
    
    @staticmethod
    def merge(files: list[str]) -> None:
        merger = PdfWriter()

        for file in files:
            merger.append(os.path.join("uploads", file))

        merger.write(path.join(DOWNLOADS_PATH, "merged.pdf"))
        merger.close()
        PDFHandler.cleanup()
    
    @staticmethod
    def to_docx(file_name: str) -> None:
        # relevant functionality
        PDFHandler.cleanup()

    @staticmethod
    def from_docx(file_name: str) -> None:
        # relevant functionality
        PDFHandler.cleanup()
    
    @staticmethod
    def cleanup() -> None:
        if os.path.exists("uploads/"):
            for r, d, f in os.walk("uploads/", topdown=False):
                for i in f:
                    os.remove(os.path.join(r, i))
                for j in d:
                    os.rmdir(os.path.join(r, j))
            os.rmdir("uploads/")
        
        os.makedirs("uploads/")

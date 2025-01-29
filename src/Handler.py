import os, json


def handle():
    """Handles the uploaded pdf file and performs operation"""
    with open("uploads/metadata.json", 'r') as f:
        metadata = json.load(f)
        f.close()
    match metadata["operation"]:
        case "split":
            PDFHandler.split(metadata["file name"], metadata["operationSpecificInfo"]["splitOnPage"])
        case "to-docx":
            PDFHandler.to_docx(metadata["file name"])
        case "from-docx":
            PDFHandler.from_docx(metadata["file name"])
    

class PDFHandler:
    @staticmethod
    def split(fileName: str, page: int) -> None:
        # relevant functionality
        

        PDFHandler.cleanup()
    
    @staticmethod
    def merge(file1: str, file2: str, order: list) -> None:
        # relevant functionality
        PDFHandler.cleanup()
    
    @staticmethod
    def to_docx(fileName: str) -> None:
        # relevant functionality
        PDFHandler.cleanup()

    @staticmethod
    def from_docx(fileName: str) -> None:
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

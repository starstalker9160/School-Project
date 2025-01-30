from json import load
from pypdf import PdfReader, PdfWriter
from os import path, remove, rmdir, makedirs, walk
from errno import errorcode, ENOSPC

DOWNLOADS_PATH = path.join(
    path.expanduser("~"), "Downloads"
)  #! temporarily using Downloads folder


def handle():
    """Handles the uploaded pdf file and performs operation"""
    with open("uploads/metadata.json", "r") as f:
        metadata = load(f)
        f.close()

    match metadata["operation"]:
        case "split":
            PDFHandler.split(
                metadata["file name"],
                metadata["operationSpecificInfo"]["splitOnPage"],
            )

        case "merge":
            PDFHandler.merge(metadata["file name"])


class PDFHandler:
    @staticmethod
    def split(file_name: str, page_number: int):
        reader = PdfReader(f"uploads/{file_name}")
        total_pages = len(reader.pages)

        try:
            page_number = int(page_number)
        except ValueError:
            raise InvalidPageNumberException(f"{page_number} is not a valid page number to split by.")

        if not 0 < page_number < total_pages:
            raise InvalidPageNumberException(f"{page_number} is not a valid page number to split by.")

        writer1 = PdfWriter()
        writer2 = PdfWriter()

        for i in range(total_pages):
            if i < page_number:
                writer1.add_page(reader.pages[i])
            else:
                writer2.add_page(reader.pages[i])

        output_filename1 = path.join(DOWNLOADS_PATH, f"{file_name}_part_1.pdf")

        try:
            with open(output_filename1, "wb") as output_file1:
                writer1.write(output_file1)

            if total_pages > page_number:
                output_filename2 = path.join(DOWNLOADS_PATH, f"{file_name}_part_2.pdf")
                with open(output_filename2, "wb") as output_file2:
                    writer2.write(output_file2)
        except OSError as e:
            if e.errno == errorcode[ENOSPC]:
                raise Exception("Device is out of storage")

        PDFHandler.cleanup()

    @staticmethod
    def merge(files: list[str]):
        merger = PdfWriter()

        for file in files:
            merger.append(path.join("uploads", file))

        try:
            merger.write(path.join(DOWNLOADS_PATH, "merged.pdf"))
            merger.close()
            PDFHandler.cleanup()
        except OSError as e:
            if e.errno == errorcode[ENOSPC]:
                raise Exception("Device is out of storage")

    @staticmethod
    def cleanup() -> None:
        if path.exists("uploads/"):
            for r, d, f in walk("uploads/", topdown=False):
                for i in f:
                    remove(path.join(r, i))
                for j in d:
                    rmdir(path.join(r, j))
            rmdir("uploads/")

        makedirs("uploads/")


class InvalidPageNumberException(Exception):
    def __init__(self, message="Invalid page number provided", *args: object) -> None:
        super().__init__(*args)
        self.message = message

    def __str__(self) -> str:
        return self.message

#  heyyyyy
#  so the pdfs will be located in /uploads
#  the metadata.json will contain the info on what you need to do to the pdf
#  
#  example metadata.json:
#  
#  {
#      "operation": "split",
#      "file name": "asdf.pdf",
#      "operationSpecificInfo": {
#          "SplitOnPage": 5
#      }
#  }
# 
#  there can only be one metadata file at a time, please load the metadata into a dict obj and then delete the file

def handle():
    """Handles the uploaded pdf file and performs operation"""
    # go
    pass
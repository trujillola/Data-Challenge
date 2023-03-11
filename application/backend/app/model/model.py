#  
from joblib import dump, load
from app.objects.manager import Datasets

class OCRmodel:
    """
        Create an OCR Model object and methods to interact with it
    """

    model : None
    filepath : str

    def __init__(self,save_file_name : str):
        """
            Initialize the Random Forest
            args : model file path 
        """
        self.filepath = save_file_name
        self.model = None

   
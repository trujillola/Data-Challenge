from fastapi import APIRouter, UploadFile
from app.objects.launcher import Launcher

"""
    Describe the parameters of this api file
"""
router = APIRouter(
    prefix='/api',
    tags = ['api']
)

launcher = Launcher()


################
## API ROUTES ##
################

@router.get("/get_files_list/")
async def get_files_list():
    """
        Get the list of files

        Returns: the list of files
    """ 
    return launcher.get_files_list()


@router.post("/upload_file/")
async def create_upload_file(uploaded_file: UploadFile):
    """Upload in the database a new file given by the user, runs the model on it and returns a message notifying the user of the result.

    Args:
        file (UploadFile): _description_

    Returns:
        message: message error in case the upload failed of a success message.
    """
    return launcher.upload_file(uploaded_file)



@router.get("/get_well_composition/")
async def get_well_composition(file_name : str):
    """Get the composition of a well given its name 

    Args:
        file_name (str): string of the required filename

    Returns:
        dict_composition : a dictionnary of the composition of the well
    """
    dict_composition = {"sand" : 10, "clay" : 20 , "stone" : 90}
    return dict_composition


@router.get("/get_well_description/")
async def get_well_composition(file_name : str):
    """
        Get the description of a well given its name

    Args:
        file_name (str): string of the required filename
    
    Returns:
        description : string of the description of the well

    """
    description = ""
    return description


@router.get("/get_well_position/")
async def get_well_position(file_name : str):
    """
        Get the position of a well given its name

    Args:
        file_name (str): string of the required filename
    
    Returns:
        position : 

    """
    position = ""
    return position


@router.post("/update_well_name/")
async def update_well_name(file_name : str, new_file_name : str):
    """
       Change the name of a well given the new name

    Args:
        file_name (str): string of the required filename
        new_file_name (str): string of the name of the file
    
    Returns:
        a validation message

    """
    message = ""
    return message

import os
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


# @router.post("/upload_file/")
# async def create_upload_file(uploaded_file: UploadFile):
#     """Upload in the database a new file given by the user, runs the model on it and returns a message notifying the user of the result.

#     Args:
#         file (UploadFile): _description_

#     Returns:
#         message: message error in case the upload failed of a success message.
#     """
#     return launcher.upload_file(uploaded_file)

@router.post("/upload_column_legend/")
async def upload_column_legend(well_name : str, column_file: UploadFile, legend_file: UploadFile):
    """Upload in the database the new files given by the user
    """
    column_path = "./app/data/results/" + well_name + "/"
    column_file.filename = "completion_log.png"
    legend_path = "./app/data/results/" + well_name + "/"
    legend_file.filename = "legend.png"
    return (launcher.file_manager.upload_file(column_path,column_file) and launcher.file_manager.upload_file(legend_path,legend_file))


@router.get("/get_well_composition/")
async def get_well_composition(well_name : str) :
    """Get the composition of a well given its name 

    Args:
        file_name (str): string of the required filename

    Returns:
        dict_composition : a dictionnary of the composition of the well
    """
    #dict_composition = {"sand" : 10, "clay" : 20 , "stone" : 90}
    # colors : ['#ffc800', '#96e600', '#28c896', '#32c8c8', '#009bff', '#285aff', '#ff0000']
    # --color-yellow : #ffc800;
    # --color-light-green : #96e600;
    # --color-green : #28c896;
    # --color-light-blue: #32c8c8;
    # --color-blue : #009bff;
    # --color-dark-blue : #285aff;
    # --color-red: #ff0000;

    tab_labels, tab_valeurs = launcher.get_composition(well_name)
    tab_colors = ['#ffc800', '#96e600', '#28c896', '#32c8c8', '#009bff']
    # dict_composition = [{ 'value': 10, 'label': 'sand', 'color': '#ffc800' }, 
    #     { 'value': 20, 'label': 'clay', 'color': '#28c896'  },
    #     { 'value': 90, 'label': 'stone', 'color': '#96e600'  }]
    dict_composition = []
    for i in range(len(tab_labels)):
        dict_composition.append({'value': tab_valeurs[i], 'label': tab_labels[i], 'color': tab_colors[i]})
    return dict_composition


@router.get("/get_well_description/")
async def get_well_description(file_name : str):
    """
        Get the description of a well given its name

    Args:
        file_name (str): string of the required filename
    
    Returns:
        description : string of the description of the well

    """


    description = launcher.get_well_description(file_name)

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

    #position = {'name' : 'Pau', 'coordinates': [1, 58] }

    position = launcher.get_well_position(file_name)
    #print("position = ", position['NS'].split('°')[0])
    return {'name': '', 'coordinates': [position['EW'].split('°')[0], position['NS'].split('°')[0]]}


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

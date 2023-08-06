import pathlib
import datetime as dt
import json
from tabulate import tabulate
from PIL import Image

from stoffel.settings import *
from stoffel.core import msft, ggl
from stoffel.core.utils.paths import path_leaf
from stoffel.core.utils.project import SOURCES, DESTINATIONS

class Source:
    def __init__(self, sheet, rng, **kwargs):
        self.sheet = sheet
        self.rng = rng
        for key, value in kwargs.items():
            self.__dict__[key] = value

    @staticmethod
    def temp_image_name(filename, sheet, rng, datetime=False):
        if datetime:
            save_to = f"{filename}_{sheet}_{rng.replace(':', '_')}_{dt.datetime.now().strftime('%Y_%m_%dT%H_%M_%S')}.jpg"
        else:
            save_to = f"{filename}_{sheet}_{rng.replace(':', '_')}.jpg"
        return save_to

class Excel(Source):
    tp = "excel"
    excel_path = None
    temp_directory = pathlib.Path(__file__).parent.parent.absolute() / "files"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(str(pathlib.Path(self.excel_path)))
        self.file_name, self.file_extension = str(pathlib.Path(path_leaf(self.excel_path))).split(".")

    def get(self):
        temp_image_name = self.temp_image_name(self.file_name, self.sheet, self.rng)
        wb = msft.Excel(self.excel_path)
        wb.get_image(self.sheet, self.rng, str(self.temp_directory / temp_image_name))
        if self.delete:
            wb.delete()
        return str(self.temp_directory / temp_image_name)

class Sheets(Source):
    tp = "sheets"
    sheet_id = None
    temp_directory = pathlib.Path(__file__).parent.parent.absolute() / "files"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drive = ggl.Drive()

    def get(self):
        temp_excel_path = str(self.temp_directory / f"{self.sheet_id}.xlsx")
        self.drive.download_file(self.sheet_id, temp_excel_path)
        ex = Excel(self.sheet, self.rng, excel_path=temp_excel_path, delete=True)
        return ex.get()

class Destination:
    
    def __init__(self, w, h, x, y, resize,**kwargs):
        self.w=w
        self.h=h
        self.x=x
        self.y=y
        self.resize=resize
        for key, value in kwargs.items():
            self.__dict__[key] = value

class Slides(Destination):
    tp = "slides"
    presentation_id = None
    page_id = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slides = ggl.Slides(self.presentation_id)
        self.drive = ggl.Drive()

    def upload(self, image_path):
        if self.resize=="checked": #Not resized, it matches the width. 
            im = Image.open(image_path)
            im = im.resize((int(self.w * 72), int(self.h * 72)))
            im.save(image_path)
        folder = self.drive.find_file(PROJECT_NAME + "Temp")
        if not folder:
            folder_id = self.drive.create_folder(PROJECT_NAME + "Temp").get("id")
        else:
            folder_id = folder[0].get("id")
        image_id = self.drive.create_image(image_path, parent=folder_id).get("id")
        self.drive.make_shareable(image_id)
        self.slides.add_image(image_id, self.page_id, self.w, self.h, self.x, self.y)
        self.drive.delete_file(image_id)
        
class Powerpoint(Destination):
    tp = "powerpoint"
    presentation_path = None
    slide_index = None
    slide_id = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def upload(self, image_path):
        pt = msft.Powerpoint(self.presentation_path)
        pt.open()
        print(self.slide_index)
        if self.slide_index:
            self.slide_id = pt.get_slide_id(self.slide_index)
        print(self.slide_id)
        pt.close()
        pt.add_image(image_path, self.slide_id, self.w, self.h, self.x, self.y)

class Connection:

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def run(self):
        image_path = self.source.get()
        self.destination.upload(image_path)

class Project:
    sources = SOURCES
    sources["objects"] =  {
        "excel" : Excel, 
        "sheets" : Sheets,
    }
    destinations = DESTINATIONS
    destinations["objects"] = {
        "slides" : Slides, 
        "powerpoint" : Powerpoint
    }

    def __init__(self, name):
        self.name=name
        self.connections = {}
        with open(CONNECTIONS_PATH, "r") as f:
            data = json.load(f)
        
        if name in data:
            self.project = data[name]
            for id, connection in self.project.items():
                source_data = connection.get("source")
                source = self.sources["objects"][source_data.get("tp")](**source_data)
                destination_data = connection.get("destination")
                destination = self.destinations["objects"][destination_data.get("tp")](**destination_data)
                self.connections[id] = Connection(
                    source=source, 
                    destination=destination, 
                )
        else:
            self.project = {}
        
    def add_connection(self, connection_object):
        self.project[len(self.connections.keys())] = {
            "source" : {**{"tp" : connection_object.source.tp}, **{k : v for k, v in connection_object.source.__dict__.items() if k in self.sources["fields"][connection_object.source.tp]}}, 
            "destination" : {**{"tp" : connection_object.destination.tp}, **{k : v for k, v in connection_object.destination.__dict__.items() if k in self.destinations["fields"][connection_object.destination.tp]}}
        }
        self.connections[len(self.connections.keys())] = connection_object

    def show_connections(self):
        table = []
        for id, connection in self.project.items():
            source = connection.get("source")
            source_type = source.get("tp")
            source_file = path_leaf(source.get("excel_path")) if source_type == "excel" else source.get("sheet_id")
            source_sheet = source.get("sheet")
            source_range = source.get("rng")
            dest = connection.get("destination")
            dest_type = dest.get("tp")
            dest_file = path_leaf(dest.get("presentation_path")) if dest_type == "powerpoint" else dest.get("presentation_id")
            table.append([id, source_type, source_file, source_sheet, source_range, dest_type, dest_file])
        print(tabulate(table, ["id", "source_type", "source_file", "source_sheet", "source_range", "dest_type", "dest_file"], tablefmt="github"))
            
    def update(self):
        with open(CONNECTIONS_PATH, 'r+') as f:
            data = json.load(f)
            data[self.name] = self.project
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()  

    def remove_connection(self, id):
        self.project.pop(str(id))

    def run(self):
        for id, connection in self.connections.items():
            connection.run()

if __name__=="__main__":
    project = Project("test")

    '''
    #Connection 1
    directory = pathlib.Path(__file__).parent.parent.absolute() / "test"
    source = Excel("Sheet1", "B2:D6", excel_path=str(directory / "test.xlsx"))
    destination = Slides(3.79, 1.83, 3.1, 1.38, 
        presentation_id="1FJkzWBdb2AHL2-PKgu3BWFYtW9k1TK7OewTzvXX-BLI", 
        page_id="g7d4b0c9081_0_74", 
    )
    connection = Connection(source, destination)
    
    project.add_connection(connection)
    

    #Connection 2
    source = Sheets("Sheet2", "B3:E7", sheet_id="1Q1cm8MxDq0bzmok9PYzQc2ZjGSzNYRvjg5Yqggi_0f4")
    destination = Powerpoint(-1, -1, 3.1, 1.38, 
        presentation_path=str(directory / "Presentation1.pptx"), 
        slide_index=2
    )
    connection = Connection(source, destination)
    '''
    project.show_connections()
    project.run()

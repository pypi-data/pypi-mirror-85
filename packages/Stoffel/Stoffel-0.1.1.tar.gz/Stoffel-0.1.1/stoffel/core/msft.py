import PIL
import os
import pathlib
import xlwings as xw
import datetime as dt

from win32com.client import DispatchEx
import pythoncom

from stoffel.core.utils.vba import RANGE_TO_IMAGE
from stoffel.core.utils.paths import path_leaf

class Excel:
    def __init__(self, file_path):
        self.file_path = file_path

    def open(self, visible=False):
        print(f"Opening file: {self.file_path}")
        pythoncom.CoInitialize()
        self.app = xw.App(visible=visible, add_book=False)
        self.wb = self.app.books.open(self.file_path)

    def add_vba(self):
        print(f"Adding VBA")
        xlmodule = self.wb.api.VBProject.VBComponents.Add(1)
        xlmodule.CodeModule.AddFromString(RANGE_TO_IMAGE.strip())

    def run_vba(self, macro_name, *args):
        print(f"Running VBA")
        self.app.api.Run(macro_name, *args)

    def close(self):
        print("Closing file")
        self.wb.close()

    def get_image(self, sht, rng, file_path):
        self.open()
        self.add_vba()
        self.run_vba("RangetoImage", sht, rng, file_path)
        print(f"Saved image to: {file_path}")
        self.close()

    def find_images(self):
        self.open()
        for sheet in self.wb.sheets:
            print(sheet.name)
            myCell = self.wb.sheets[sheet.name].api.UsedRange.Find('x', LookAt=1)
            print(myCell.address)

    def delete(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path) 

class Powerpoint:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name, self.file_extension = path_leaf(file_path).split(".")
        self.directory = pathlib.Path(__file__).parent.absolute()

    def open(self):
        print(self.file_path)
        pythoncom.CoInitialize()
        self.app = DispatchEx('PowerPoint.Application')
        self.pt = self.app.Presentations.Open(self.file_path, WithWindow=False)

    def close(self):
        self.pt.Close()

    def save(self):
        self.pt.Save()

    def add_image(self, picture_path, slide_id, w, h, x, y):
        self.open()
        slide = self.pt.Slides.FindBySlideID(slide_id)
        slide.Shapes.AddPicture(FileName=picture_path, LinkToFile=False, SaveWithDocument=True, Left=x*72, Top=y*72, Width=w*72, Height=h*72)
        self.save()
        self.close()

    def get_slide_id(self, slide_index):
        return self.pt.Slides(int(slide_index)).SlideID

if __name__=="__main__":
    
    directory = pathlib.Path(__file__).parent.parent.absolute()
    '''
    wb = Excel(str(directory / "test" / "1Q1cm8MxDq0bzmok9PYzQc2ZjGSzNYRvjg5Yqggi_0f4.xlsx"))
    wb.open(visible=False)
    wb.add_vba()
    wb.run_vba("RangetoImage", "Sheet2", "B3:E7", str(directory / "test.jpg"))
    '''
    pt = Powerpoint(str(directory / "test" / "Presentation1.pptx"))
    pt.open()
    print(pt.Slides)




    
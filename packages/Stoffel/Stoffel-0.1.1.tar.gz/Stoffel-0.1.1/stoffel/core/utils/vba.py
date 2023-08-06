RANGE_TO_IMAGE = """
Sub RangetoImage(sheet_string As String, rng_string As String, save_path as String)
    Dim tmpChart As Chart, n As Long, shCount As Long, sht As Worksheet, sh As Shape
    Dim fileSaveName As Variant, pic As Variant
    Dim rng As Range
    
    'Create temporary chart as canvas
    Set sht = Worksheets(sheet_string)
    sht.Activate
    Set rng = sht.Range(rng_string)
    rng.Select
    Selection.Copy
    sht.Pictures.Paste.Select
    Set sh = sht.Shapes(sht.Shapes.Count)
    Set tmpChart = Charts.Add
    tmpChart.ChartArea.Clear
    tmpChart.Name = "PicChart" & (Rnd() * 10000)
    Set tmpChart = tmpChart.Location(Where:=xlLocationAsObject, Name:=sht.Name)
    tmpChart.ChartArea.Width = sh.Width
    tmpChart.ChartArea.Height = sh.Height
    tmpChart.Parent.Border.LineStyle = 0
    
    'Paste range as image to chart
    sh.Copy
    tmpChart.ChartArea.Select
    tmpChart.Paste
    
    'Save chart image to file
    tmpChart.Export Filename:=save_path, FilterName:="jpg"
    
    'Clean up
    sht.Cells(1, 1).Activate
    sht.ChartObjects(sht.ChartObjects.Count).Delete
    sh.Delete
    
End Sub
"""
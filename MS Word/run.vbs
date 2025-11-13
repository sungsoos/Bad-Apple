Sub BadApple()
    Dim filePath As String
    ' Put file path below!
    filePath = "Put Location here!" ' !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ' ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    Dim fileNum As Integer
    Dim fileContent As String
    Dim frameArray() As String
    Dim i As Long
    Dim startTime As Single
    Dim frameDuration As Single
    
    ' 15 fps for smoother playback
    frameDuration = 1 / 60
    
    ' Check if file exists
    If Dir(filePath) = "" Then
        MsgBox "File not found!", vbCritical
        Exit Sub
    End If
    
    ' Open file in Binary mode and read everything at once
    fileNum = FreeFile
    Open filePath For Binary As #fileNum
        If LOF(fileNum) > 0 Then
            fileContent = Space$(LOF(fileNum))
            Get #fileNum, , fileContent
        Else
            MsgBox "File is empty!", vbExclamation
            Close #fileNum
            Exit Sub
        End If
    Close #fileNum
    
    ' Remove null characters
    fileContent = Replace(fileContent, vbNullChar, "")
    fileContent = Trim(fileContent)
    
    ' Split frames by delimiter
    frameArray = Split(fileContent, "===FRAME===")
    
    ' Play frames by replacing all content at once per frame
    For i = LBound(frameArray) To UBound(frameArray)
        ' Replace all document text with the frame content
        ActiveDocument.Content.Text = frameArray(i)
        DoEvents
        
        ' Wait for the frame duration
        startTime = Timer
        Do While Timer < startTime + frameDuration
            DoEvents
        Loop
    Next i
End Sub



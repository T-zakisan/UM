Attribute VB_Name = "表リスト作成"
Public Sub 表リスト作成(dumy As String)
  
  Dim wb As Workbook: Set wb = ThisWorkbook
  
  '初期化
  With wb.Worksheets("表リスト")
    .Range("A:B") = ""
    .Cells.Borders.LineStyle = xlLineStyleNone
    .Cells.Interior.Color = RGB(255, 255, 255)
    .Range("A1:B1").Interior.Color = RGB(217, 217, 217)
    .Cells(1, "A") = "シート名"
    .Cells(1, "B") = "ファイル名(.tex)"
  End With
  

  '表タイトル，タイプの読み込み
  Dim ii As Long, jj As Long
  For ii = 1 To wb.Worksheets.Count
    If ii > 3 Then
      
      With wb.Worksheets("表リスト")
        '値取得：シート名
        .Cells(ii, "A").Offset(-2, 0).Value = wb.Worksheets(ii).Name 'シート名
        '値取得：ファイル名
        .Cells(ii, "B").Offset(-2, 0).Value = wb.Worksheets(ii).Range("A2").Value 'ファイル名
      
        '罫線
        .Range("A1:B1").Offset(ii - 3, 0).Borders(xlEdgeBottom).LineStyle = xlDash  '破線
        .Range("A1:B1").Offset(ii - 3, 0).Borders(xlEdgeBottom).Weight = xlHairline '極細
        
        'シート名をパタン次行に反映
        wb.Worksheets(ii).Range("A1").Value = wb.Worksheets(ii).Name
        wb.Worksheets(ii).Range("A1").Font.Bold = ture
        wb.Worksheets(ii).Range("A1").Font.Size = 14
                
      End With
    

'      'パタンごとに色分け
'      With wb.Worksheets("表リスト").Cells(ii, "A").Offset(-2, 0)
'        If .Value = "a" Then
'          .Interior.Color = RGB(255, 243, 204) '黄
'        ElseIf .Value = "b" Then
'          .Interior.Color = RGB(237, 237, 237) '灰
'        ElseIf .Value = "c" Then
'          .Interior.Color = RGB(221, 235, 247) '青
'        ElseIf .Value = "d" Then
'          .Interior.Color = RGB(252, 228, 214) '赤
'        ElseIf .Value = "e" Then
'          .Interior.Color = RGB(226, 239, 218) '緑
'        ElseIf .Value = "f" Then
'          .Interior.Color = RGB(255, 221, 255) '桃
'        End If
'      End With
      
    End If
  Next ii
  
  wb.Worksheets("表リスト").Columns("A:B").AutoFit '列幅自動調整
  
  
  Set wb = Nothing
End Sub

Attribute VB_Name = "シートリンク"
'■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
Public Function シートリンク(Sh As Object, target As Range) As Boolean
  シートリンク = False
  Dim NumSheet As Long: NumSheet = 0
  If Sh.Name = "表リスト" Then
    NumSheet = 表リスト(Sh, target)
  Else
    NumSheet = 表(Sh, target)
  End If

  
  '対象シートのアクティベート
  If NumSheet > 0 Then
    ThisWorkbook.Worksheets(NumSheet).Activate
    シートリンク = True
  End If
  
End Function



'■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
Private Function 表リスト(Sh As Object, target As Range) As Integer
  ' 即終了
  表リスト = -1
  If target.Value = "" Then Exit Function 'Wクリックした場所が"文字がないと場合
  If target.Row = 1 Then Exit Function    '1行目(項目)の場合
  If target.Column > Range("C1").Column Then Exit Function    '1行目(項目)の場合
  

  表リスト = target.Row + 2
End Function





'■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
Private Function 表(Sh As Object, target As Range) As Integer

  ' 即終了：1行目の1列目（パタン）以外
    表 = -1
    If target.Row <> 1 Then Exit Function   '1行目以外の場合
    If target.Column = 1 Then Exit Function '1列目の場合
  
    Dim NumList As Long: NumList = 0
    Dim ii As Long
    For ii = 1 To ThisWorkbook.Worksheets.Count
      
      If ThisWorkbook.Worksheets(ii).Name = "表リスト" Then
        NumList = ii ' [表リスト]のシート番号
      End If
      
      If ThisWorkbook.Worksheets(ii).Name = Sh.Name Then
        表 = NumList ' [表リスト]のシート番号
        Exit For
      End If
    Next
    
End Function

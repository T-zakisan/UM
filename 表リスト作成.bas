Attribute VB_Name = "�\���X�g�쐬"
Public Sub �\���X�g�쐬(dumy As String)
  
  Dim wb As Workbook: Set wb = ThisWorkbook
  
  '������
  With wb.Worksheets("�\���X�g")
    .Range("A:B") = ""
    .Cells.Borders.LineStyle = xlLineStyleNone
    .Cells.Interior.Color = RGB(255, 255, 255)
    .Range("A1:B1").Interior.Color = RGB(217, 217, 217)
    .Cells(1, "A") = "�V�[�g��"
    .Cells(1, "B") = "�t�@�C����(.tex)"
  End With
  

  '�\�^�C�g���C�^�C�v�̓ǂݍ���
  Dim ii As Long, jj As Long
  For ii = 1 To wb.Worksheets.Count
    If ii > 3 Then
      
      With wb.Worksheets("�\���X�g")
        '�l�擾�F�V�[�g��
        .Cells(ii, "A").Offset(-2, 0).Value = wb.Worksheets(ii).Name '�V�[�g��
        '�l�擾�F�t�@�C����
        .Cells(ii, "B").Offset(-2, 0).Value = wb.Worksheets(ii).Range("A2").Value '�t�@�C����
      
        '�r��
        .Range("A1:B1").Offset(ii - 3, 0).Borders(xlEdgeBottom).LineStyle = xlDash  '�j��
        .Range("A1:B1").Offset(ii - 3, 0).Borders(xlEdgeBottom).Weight = xlHairline '�ɍ�
        
        '�V�[�g�����p�^�����s�ɔ��f
        wb.Worksheets(ii).Range("A1").Value = wb.Worksheets(ii).Name
        wb.Worksheets(ii).Range("A1").Font.Bold = ture
        wb.Worksheets(ii).Range("A1").Font.Size = 14
                
      End With
    

'      '�p�^�����ƂɐF����
'      With wb.Worksheets("�\���X�g").Cells(ii, "A").Offset(-2, 0)
'        If .Value = "a" Then
'          .Interior.Color = RGB(255, 243, 204) '��
'        ElseIf .Value = "b" Then
'          .Interior.Color = RGB(237, 237, 237) '�D
'        ElseIf .Value = "c" Then
'          .Interior.Color = RGB(221, 235, 247) '��
'        ElseIf .Value = "d" Then
'          .Interior.Color = RGB(252, 228, 214) '��
'        ElseIf .Value = "e" Then
'          .Interior.Color = RGB(226, 239, 218) '��
'        ElseIf .Value = "f" Then
'          .Interior.Color = RGB(255, 221, 255) '��
'        End If
'      End With
      
    End If
  Next ii
  
  wb.Worksheets("�\���X�g").Columns("A:B").AutoFit '�񕝎�������
  
  
  Set wb = Nothing
End Sub

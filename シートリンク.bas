Attribute VB_Name = "�V�[�g�����N"
'��������������������������������������������������������������������������������������������������������������������������������������������������������������������
Public Function �V�[�g�����N(Sh As Object, target As Range) As Boolean
  �V�[�g�����N = False
  Dim NumSheet As Long: NumSheet = 0
  If Sh.Name = "�\���X�g" Then
    NumSheet = �\���X�g(Sh, target)
  Else
    NumSheet = �\(Sh, target)
  End If

  
  '�ΏۃV�[�g�̃A�N�e�B�x�[�g
  If NumSheet > 0 Then
    ThisWorkbook.Worksheets(NumSheet).Activate
    �V�[�g�����N = True
  End If
  
End Function



'��������������������������������������������������������������������������������������������������������������������������������������������������������������������
Private Function �\���X�g(Sh As Object, target As Range) As Integer
  ' ���I��
  �\���X�g = -1
  If target.Value = "" Then Exit Function 'W�N���b�N�����ꏊ��"�������Ȃ��Əꍇ
  If target.Row = 1 Then Exit Function    '1�s��(����)�̏ꍇ
  If target.Column > Range("C1").Column Then Exit Function    '1�s��(����)�̏ꍇ
  

  �\���X�g = target.Row + 2
End Function





'��������������������������������������������������������������������������������������������������������������������������������������������������������������������
Private Function �\(Sh As Object, target As Range) As Integer

  ' ���I���F1�s�ڂ�1��ځi�p�^���j�ȊO
    �\ = -1
    If target.Row <> 1 Then Exit Function   '1�s�ڈȊO�̏ꍇ
    If target.Column = 1 Then Exit Function '1��ڂ̏ꍇ
  
    Dim NumList As Long: NumList = 0
    Dim ii As Long
    For ii = 1 To ThisWorkbook.Worksheets.Count
      
      If ThisWorkbook.Worksheets(ii).Name = "�\���X�g" Then
        NumList = ii ' [�\���X�g]�̃V�[�g�ԍ�
      End If
      
      If ThisWorkbook.Worksheets(ii).Name = Sh.Name Then
        �\ = NumList ' [�\���X�g]�̃V�[�g�ԍ�
        Exit For
      End If
    Next
    
End Function

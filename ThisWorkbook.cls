VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ThisWorkbook"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
'��������������������������������������������������������������������������������������������������������������������������������������������������������������������
Private Sub Workbook_Open()
  Call �\���X�g�쐬.�\���X�g�쐬("")
End Sub



'��������������������������������������������������������������������������������������������������������������������������������������������������������������������
Private Sub Workbook_SheetActivate(ByVal Sh As Object)
  Call �\���X�g�쐬.�\���X�g�쐬("")
End Sub



'��������������������������������������������������������������������������������������������������������������������������������������������������������������������
Private Sub Workbook_SheetBeforeDoubleClick(ByVal Sh As Object, ByVal target As Range, Cancel As Boolean)
  Cancel = �V�[�g�����N.�V�[�g�����N(Sh, target)
End Sub





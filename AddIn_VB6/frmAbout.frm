VERSION 5.00
Begin VB.Form frmAbout 
   BackColor       =   &H00FFFFFF&
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Acerca de..."
   ClientHeight    =   2295
   ClientLeft      =   45
   ClientTop       =   390
   ClientWidth     =   3105
   ControlBox      =   0   'False
   BeginProperty Font 
      Name            =   "Tahoma"
      Size            =   8.25
      Charset         =   0
      Weight          =   400
      Underline       =   0   'False
      Italic          =   0   'False
      Strikethrough   =   0   'False
   EndProperty
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   2295
   ScaleWidth      =   3105
   ShowInTaskbar   =   0   'False
   StartUpPosition =   1  'CenterOwner
   Begin VB.PictureBox PicL1 
      Appearance      =   0  'Flat
      AutoSize        =   -1  'True
      BackColor       =   &H80000005&
      BorderStyle     =   0  'None
      ForeColor       =   &H80000008&
      Height          =   240
      Left            =   1920
      Picture         =   "frmAbout.frx":0000
      ScaleHeight     =   240
      ScaleWidth      =   870
      TabIndex        =   6
      TabStop         =   0   'False
      Top             =   645
      Width           =   870
   End
   Begin VB.PictureBox Picture2 
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      BorderStyle     =   0  'None
      FillColor       =   &H00FFFFFF&
      FillStyle       =   0  'Solid
      ForeColor       =   &H80000008&
      Height          =   315
      Left            =   255
      Picture         =   "frmAbout.frx":0B42
      ScaleHeight     =   315
      ScaleWidth      =   2310
      TabIndex        =   2
      TabStop         =   0   'False
      Top             =   1860
      Width           =   2310
   End
   Begin VB.Label Label2 
      AutoSize        =   -1  'True
      BackStyle       =   0  'Transparent
      Caption         =   "con apoyo"
      Height          =   195
      Left            =   225
      TabIndex        =   5
      Top             =   1605
      Width           =   750
   End
   Begin VB.Label lblVers 
      AutoSize        =   -1  'True
      BackStyle       =   0  'Transparent
      Caption         =   "V0.0.0"
      Height          =   195
      Left            =   2205
      TabIndex        =   4
      Top             =   150
      Width           =   480
   End
   Begin VB.Label Label1 
      AutoSize        =   -1  'True
      BackStyle       =   0  'Transparent
      Caption         =   "VB6-IA Addon"
      BeginProperty Font 
         Name            =   "Courier"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   240
      Left            =   165
      TabIndex        =   3
      Top             =   120
      Width           =   1815
   End
   Begin VB.Label lblLabel12 
      AutoSize        =   -1  'True
      BackStyle       =   0  'Transparent
      Caption         =   "Axio Soft. && Tech., Inc ©1997-2026"
      Height          =   390
      Left            =   225
      TabIndex        =   1
      Top             =   1140
      Width           =   1695
      WordWrap        =   -1  'True
   End
   Begin VB.Label lblLabel11 
      BackStyle       =   0  'Transparent
      Caption         =   "Creado por:           David Rojas Arraño  [Axio.UK]"
      Height          =   585
      Left            =   225
      TabIndex        =   0
      Top             =   480
      Width           =   1755
      WordWrap        =   -1  'True
   End
End
Attribute VB_Name = "frmAbout"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private Sub Form_Click()
  Unload Me
End Sub

Private Sub Form_Load()
  On Error Resume Next
  Me.Caption = T("TITLE_ABOUT", "Acerca de...")
  Label2.Caption = T("LBL_ABOUT_SUPPORT", "con apoyo")
  lblVers.Caption = "v" & App.Major & "." & App.Minor & "." & App.Revision
End Sub

Private Sub lblLabel11_Click()
  Unload Me
End Sub

Private Sub lblLabel12_Click()
  Unload Me
End Sub

Private Sub PicL0_Click()
  Unload Me
End Sub

Private Sub PicL1_Click()
  Unload Me
End Sub

Private Sub Picture2_Click()
  Unload Me
End Sub

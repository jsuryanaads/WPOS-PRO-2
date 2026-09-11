; WPOS PRO 2 Inno Setup
#define MyAppName "WPOS PRO 2"
#define MyAppVersion "2.7.5"
#define MyAppPublisher "WPOS PRO"
#define MyAppExeName "WPOS PRO 2.exe"

[Setup]
AppId={{B7D0E6A8-7B7A-4D74-9A4D-9C6C5E9E1A10}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\WPOS PRO 2
DefaultGroupName=WPOS PRO 2
OutputDir=installer
OutputBaseFilename=WPOS_PRO_2_Setup
SetupIconFile=assets\branding\wpos_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayName=WPOS PRO 2

[Files]
Source: "dist\WPOS PRO 2\WPOS PRO 2.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\WPOS PRO 2\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\WPOS PRO 2"; Filename: "{app}\WPOS PRO 2.exe"
Name: "{autodesktop}\WPOS PRO 2"; Filename: "{app}\WPOS PRO 2.exe"

[Run]
Filename: "{app}\WPOS PRO 2.exe"; Description: "Jalankan WPOS PRO 2"; Flags: nowait postinstall skipifsilent

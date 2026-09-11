; WPOS PRO V2 Inno Setup
#define MyAppName "WPOS PRO V2"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "WPOS PRO"
#define MyAppExeName "WPOS PRO V2.exe"

[Setup]
AppId={{B7D0E6A8-7B7A-4D74-9A4D-9C6C5E9E1A10}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\WPOS PRO V2
DefaultGroupName=WPOS PRO V2
OutputDir=installer
OutputBaseFilename=WPOS_PRO_V2_Setup
SetupIconFile=assets\branding\wpos.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayName=WPOS PRO V2

[Files]
Source: "dist\WPOS PRO V2\WPOS PRO V2.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\WPOS PRO V2\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\WPOS PRO V2"; Filename: "{app}\WPOS PRO V2.exe"
Name: "{autodesktop}\WPOS PRO V2"; Filename: "{app}\WPOS PRO V2.exe"

[Run]
Filename: "{app}\WPOS PRO V2.exe"; Description: "Jalankan WPOS PRO V2"; Flags: nowait postinstall skipifsilent

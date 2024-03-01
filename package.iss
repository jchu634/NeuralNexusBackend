#define AppName "NeuralNexus"
#define AppVersion "1.0.0"
#define AppPublisher "Joshua Chung"
#define AppExeName "NeuralNexus"
; #define AppIcon "library\static\favicon.ico"

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={pf}\{#AppPublisher}\{#AppName}
DefaultGroupName={#AppName}
OutputDir=.
OutputBaseFilename={#AppExeName}-Setup
Compression=lzma2
SolidCompression=yes
UninstallDisplayIcon={app}\{#AppExeName}.exe

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "Do you want to create desktop icon?"; Flags: checkablealone

[Files]
Source: "dist\{#AppExeName}\library\static\uploads\*"; DestDir: "{userappdata}\{#AppPublisher}\{#AppName}\library\static\uploads"; Flags: recursesubdirs createallsubdirs
Source: "dist\{#AppExeName}\library\static\storage\*"; DestDir: "{userappdata}\{#AppPublisher}\{#AppName}\library\static\storage"; Flags: recursesubdirs createallsubdirs
Source: "dist\{#AppExeName}\*"; DestDir: "{app}"; Flags: recursesubdirs

[Registry]
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{#AppExeName}.exe"; ValueType: string; ValueName: ""; ValueData: {app}\{#AppExeName}.exe Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{#AppExeName}.exe"; ValueType: string; ValueName: "Path"; ValueData: {app}; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{#AppExeName}.exe"; ValueType: string; ValueName: "Version"; ValueData: {#AppVersion}; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Flags: uninsdeletevalue


[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\{#AppExeName}.exe"
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon; IconFilename: "{app}\{#AppExeName}.exe"
Name: "{commonprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\{#AppExeName}.exe"
[Setup]
AppName=CenturyPly QA WebApp
AppVersion=4.2
DefaultDirName={pf}\CenturyPly QA WebApp
DefaultGroupName=CenturyPly QA WebApp
OutputBaseFilename=CenturyPly_QA_WebApp_Setup_v4.2
SetupIconFile=static\logo.ico

[Files]
Source: "dist\centuryply_audit_webapp.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "static\*"; DestDir: "{app}\static"; Flags: recursesubdirs
Source: "templates\*"; DestDir: "{app}\templates"; Flags: recursesubdirs

[Icons]
Name: "{group}\CenturyPly QA Portal"; Filename: "{app}\centuryply_audit_webapp.exe"; IconFileName: "{app}\static\logo.ico"
Name: "{commondesktop}\CenturyPly QA Portal"; Filename: "{app}\centuryply_audit_webapp.exe"; IconFileName: "{app}\static\logo.ico"

[Run]
Filename: "{app}\centuryply_audit_webapp.exe"; Flags: nowait postinstall skipifsilent

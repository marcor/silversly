cd %1
%7 open %2

%7 pull
%7 co "%3" --force
xcopy "%4\*.*" "%5" /D /Y /S 

copy /b "%6" +,,
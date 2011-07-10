cd %1
fossil open %2

fossil pull
fossil co "$3" --force
xcopy "$4\*.*" "$5" /D /Y  

copy /b "$6" +,,
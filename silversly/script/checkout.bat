cd %1
fossil open %2

fossil pull
fossil co "%3" --force
xcopy "%4\*.*" "%5" /D /Y /S

python manage.py migrate --noinput
touch "%6"


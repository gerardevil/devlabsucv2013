El siguiente directorio contiene :

1.- settings.py - archivo de configuraciones para correr el proyecto con servidor local, manage.py runserver.

2.- view-example.html - una vista de ejemplo mostrando como deber ser ahora el acceso a datos estaticos, desde el proyecto como localhost.

3.- Para que los datos estaticos puedan ser encontrados :
    
    Crear un directorio static en la carpeta views y colocar el directorio assets en dicha carpeta.

[ WARNING ]
- Recuerde que antes de correo el proyecto en el servidor local debe hacer uso del comando 'manage.py syncdb' para mantener su Base de Datos local actualizada.
- Cabe destacar que al momento de realizar 'git push' desde su repositorio local, debe primero verificar que las configuraciones setting.py sean las establecidas para el servidor remoto, al igual que el metodo de acceso a los recursos estaticos.

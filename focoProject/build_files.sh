echo "Iniciando el proceso de construcción..."
echo "Versión de Python instalada:"
python3 --version

# Instalar dependencias
echo "Instalando dependencias..."
python3 -m pip install -r requirements.txt

# Realizar migraciones
echo "Aplicando migraciones..."
python3 manage.py migrate

# Recoger archivos estáticos
echo "Recogiendo archivos estáticos..."
python3 manage.py collectstatic

echo "Proceso de construcción completado."
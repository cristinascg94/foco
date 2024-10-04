echo "Iniciando el proceso de construcción..."
echo "Versión de Python instalada:"
python --version

# Instalar dependencias
echo "Instalando dependencias..."
python -m pip install -r requirements.txt

# Realizar migraciones
echo "Aplicando migraciones..."
python manage.py migrate

# Recoger archivos estáticos
echo "Recogiendo archivos estáticos..."
python manage.py collectstatic

echo "Proceso de construcción completado."
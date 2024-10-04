echo "Iniciando el proceso de construcción..."
echo "Versión de Python instalada:"
python --version

# Instalar dependencias
echo "Instalando dependencias..."
python3.10 -m pip install -r requirements.txt

# Realizar migraciones
echo "Aplicando migraciones..."
python3.10 manage.py migrate

# Recoger archivos estáticos
echo "Recogiendo archivos estáticos..."
python3.10 manage.py collectstatic

echo "Proceso de construcción completado."
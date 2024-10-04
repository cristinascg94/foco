echo "Iniciando el proceso de construcción..."

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Realizar migraciones
echo "Aplicando migraciones..."
python manage.py migrate

# Recoger archivos estáticos
echo "Recogiendo archivos estáticos..."
python manage.py collectstatic

echo "Proceso de construcción completado."
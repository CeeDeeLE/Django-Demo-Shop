# Create a virtual environment
# echo "Creating a virtual environment..."
# python3.11 -m venv venv
# source venv/bin/activate

echo "Installing the latest version of pip..."
python -m pip install --upgrade pip

echo "Installing the latest version of pipenv..."
python -m pip install pipenv

# integrate the Django framework
python -m pip install Django

# Build the project
echo "Building the project..."
python -m pip install -r requirements.txt

# collect Models
echo "Make Migration..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
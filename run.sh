set -e


echo "Starting frontend..."
cd client || { echo "Client folder not found"; exit 1; }
echo "Running server vvia 'yarn dev' in client folder..."
yarn dev &
FRONTEND_PID=$!


cd ..
echo "Setting up backend..."
cd backend || { echo "Backend folder not found"; exit 1; }

echo "Creating virtual environment..."
python3 -m venv virtualenvironment
source virtualenvironment/bin/activate
echo "Installing requirements..."
pip install -r requirements.txt
echo "Please enter the following environment variables:"

read -p "GEMINI_API_KEY: " GEMINI_API_KEY
read -p "GEMINI_API_URL: " GEMINI_API_URL
read -p "GEMINI_MODEL: " GEMINI_MODEL
read -p "AZURE_OPENAI_KEY: " AZURE_OPENAI_KEY
read -p "AZURE_OPENAI_ENDPOINT: " AZURE_OPENAI_ENDPOINT
read -p "AZURE_OPENAI_DEPLOYMENT: " AZURE_OPENAI_DEPLOYMENT

export GEMINI_API_KEY
export GEMINI_API_URL
export GEMINI_MODEL
export AZURE_OPENAI_KEY
export AZURE_OPENAI_ENDPOINT
export AZURE_OPENAI_DEPLOYMENT

echo "Running app.py..."
python3 app.py

wait $FRONTEND_PID

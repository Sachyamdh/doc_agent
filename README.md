# Running the Project

This guide explains how to run the automated setup and start scripts for both Linux/macOS and Windows.


## Linux / macOS

1. Open a terminal and navigate to the project root folder.

2. Make sure the run script has execute permissions:

```bash
chmod +x run.sh
```

3. Run the script:

```bash
./run.sh
```

4. The script will:

   * Start the frontend (`yarn dev`) in the `client` folder.

   * Set up the backend virtual environment in the `backend` folder.

   * Install Python requirements.

   * Prompt you to enter required environment variables:

     * `GEMINI_API_KEY`
     * `GEMINI_API_URL`
     * `GEMINI_MODEL`
     * `AZURE_OPENAI_KEY`
     * `AZURE_OPENAI_ENDPOINT`
     * `AZURE_OPENAI_DEPLOYMENT`

   * Launch `app.py` in the backend.


## Windows

1. Open Command Prompt and navigate to the project root folder.

2. Run the batch script:

```cmd
run.bat
```

3. The script will:

   * Start the frontend (`yarn dev`) in the `client` folder.
   * Set up the backend virtual environment in the `backend` folder.
   * Install Python requirements.
   * Prompt you to enter the required environment variables.
   * Launch `app.py` in the backend.

### Notes

* Make sure **Node.js**, **Yarn**, and **Python 3** are installed and available in your system PATH.
* Environment variables entered will only persist while the script is running. Restarting the script will require re-entering them unless you save them permanently in your system environment.

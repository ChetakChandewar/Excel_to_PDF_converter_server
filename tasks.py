import subprocess
import os
from celery import Celery

# Setup Flask and Celery
app = Flask(__name__)

# Celery configuration
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"  # Redis as the broker
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

UPLOAD_FOLDER = "/app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@celery.task
def convert_excel_to_pdf(input_path, output_path):
    """
    Task to convert an Excel file to PDF using LibreOffice CLI
    """
    try:
        # Command to call LibreOffice in headless mode for conversion
        command = [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            UPLOAD_FOLDER,
            input_path
        ]
        
        # Run the conversion command
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("LibreOffice Output:", result.stdout)  # Debugging

        if not os.path.exists(output_path):
            raise Exception("Conversion failed. Output file not found.")

        print(f"File converted successfully to {output_path}")

    except subprocess.CalledProcessError as e:
        print("LibreOffice Error:", e.stderr)  # Debugging
        raise Exception(f"Conversion failed: {e.stderr}")

    return output_path

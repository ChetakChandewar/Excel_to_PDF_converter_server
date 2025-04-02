import os
from flask import Flask, request, jsonify, send_file
from celery import Celery
import subprocess

app = Flask(__name__)

# Configuration for Celery
app.config['CELERY_BROKER_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

UPLOAD_FOLDER = "/app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@celery.task(bind=True)
def convert_excel_to_pdf(self, filename):
    """ Convert Excel file to PDF using LibreOffice CLI """
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = input_path.replace(".xlsx", ".pdf")

    try:
        subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", input_path, "--outdir", UPLOAD_FOLDER], check=True)
        return {"status": "success", "pdf_path": output_path}
    except subprocess.CalledProcessError:
        return {"status": "failed", "message": "Conversion error"}

@app.route("/convert", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    task = convert_excel_to_pdf.apply_async(args=[file.filename])
    return jsonify({"task_id": task.id, "status": "processing"}), 202

@app.route("/status/<task_id>", methods=["GET"])
def task_status(task_id):
    task = convert_excel_to_pdf.AsyncResult(task_id)
    if task.state == "PENDING":
        response = {"state": task.state, "status": "Pending..."}
    elif task.state == "SUCCESS":
        response = {"state": task.state, "result": task.result}
    else:
        response = {"state": task.state, "status": "Failed"}

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

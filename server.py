import os
import subprocess
from flask import Flask, request, send_file

app = Flask(__name__)

UPLOAD_FOLDER = "/app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/convert", methods=["POST"])
def convert_excel_to_pdf():
    if "file" not in request.files:
        return {"error": "No file part"}, 400

    file = request.files["file"]
    if file.filename == "":
        return {"error": "No selected file"}, 400

    # Save the uploaded file
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Convert Excel to PDF using LibreOffice CLI
    output_path = input_path.replace(".xls", ".pdf").replace(".xlsx", ".pdf")
    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        UPLOAD_FOLDER,
        input_path
    ], check=True)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

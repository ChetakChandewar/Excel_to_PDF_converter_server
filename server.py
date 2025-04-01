from flask import Flask, request, send_file
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "converted"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_excel_to_pdf():
    if 'file' not in request.files:
        return {"error": "No file uploaded"}, 400

    file = request.files['file']
    
    if file.filename == '':
        return {"error": "No file selected"}, 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Define output PDF file path
    output_filename = filename.rsplit('.', 1)[0] + ".pdf"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    # Convert using LibreOffice CLI
    try:
        subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf",
            filepath, "--outdir", OUTPUT_FOLDER
        ], check=True)

        return send_file(output_path, as_attachment=True)
    except subprocess.CalledProcessError:
        return {"error": "Conversion failed"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

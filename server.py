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

    # Ensure filenames with spaces are handled correctly
    output_path = input_path.rsplit(".", 1)[0] + ".pdf"
    input_path_escaped = f'"{input_path}"'  # Add quotes to prevent space issues

    try:
        # Convert Excel to PDF using LibreOffice CLI
        result = subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            UPLOAD_FOLDER,
            input_path_escaped
        ], capture_output=True, text=True, check=True)

        print("LibreOffice Output:", result.stdout)  # Debugging

        # Ensure the output file exists
        if not os.path.exists(output_path):
            return {"error": "Conversion failed. Output file not found."}, 500

        return send_file(output_path, as_attachment=True)

    except subprocess.CalledProcessError as e:
        print("LibreOffice Error:", e.stderr)  # Debugging
        return {"error": "Conversion failed", "details": str(e.stderr)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

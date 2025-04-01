from flask import Flask, request, jsonify
from tasks import convert_excel_to_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "/app/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Max upload size 16MB

# Create uploads folder if it doesn't exist
import os
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/convert", methods=["POST"])
def convert_file():
    # Check if the file is part of the request
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save the file to the upload folder
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(input_path)

    # Start the conversion process in the background
    output_path = input_path.rsplit(".", 1)[0] + ".pdf"
    
    # Call the Celery task asynchronously
    convert_excel_to_pdf.apply_async(args=[input_path, output_path])

    return jsonify({"message": "Conversion started"}), 202

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

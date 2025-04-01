from flask import Flask, request, jsonify
from tasks import convert_excel_to_pdf

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    input_path = f'/tmp/{file.filename}'
    file.save(input_path)

    output_path = f'/tmp/{file.filename}.pdf'
    task = convert_excel_to_pdf.apply_async(args=[input_path, output_path])

    return jsonify({"task_id": task.id, "status": "Conversion started"}), 202

@app.route('/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = convert_excel_to_pdf.AsyncResult(task_id)
    if task.state == 'PENDING':
        return jsonify({"task_id": task.id, "status": "Pending"})
    elif task.state == 'SUCCESS':
        return jsonify({"task_id": task.id, "status": "Success", "result": task.result})
    else:
        return jsonify({"task_id": task.id, "status": task.state})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define the upload folders
UPLOAD_FOLDER = '/data'
LOCATIONS_FOLDER = '/locations'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOCATIONS_FOLDER, exist_ok=True)

# Define allowed extensions
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'json', 'png'}

# Check if the file has one of the allowed extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    # Upload a file to the /home/ubuntu/data directory.
    
    # Request: 
    # - POST request
    # - Multipart form-data with a file
    
    # Response:
    # - Success: {"message": "File uploaded successfully", "filename": filename}, 200
    # - Failure: {"error": "No file part"}, 400
    #            {"error": "No selected file"}, 400
    #            {"error": "File type not allowed"}, 400
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({"message": "File uploaded successfully", "filename": filename}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

@app.route('/getnewestfile', methods=['GET'])
def get_newest_file():
    # Get the newest file containing a specific filename part from the /home/ubuntu/data directory.
    
    # Request: 
    # - GET request
    # - Query parameter: filename (part of the filename to search for)
    
    # Response:
    # - Success: {"newest_file": newest_file}, 200
    # - Failure: {"error": "No filename provided"}, 400
    #            {"error": "No matching files found"}, 404
    filename_part = request.args.get('filename')
    if not filename_part:
        return jsonify({"error": "No filename provided"}), 400
    
    matching_files = [f for f in os.listdir(UPLOAD_FOLDER) if filename_part in f]
    if not matching_files:
        return jsonify({"error": "No matching files found"}), 404
    
    matching_files.sort(key=lambda f: f.split('_')[2], reverse=True)
    newest_file = matching_files[0]
    
    return jsonify({"newest_file": newest_file}), 200

@app.route('/getdatafromlocation', methods=['GET'])
def get_data_from_location():
    # Get all files from a specific location, returning only the newest file 
    # for each unique filename and file type.
    
    # Request: 
    # - GET request
    # - Query parameter: locationname (location name to search for)
    
    # Response:
    # - Success: {"files": list_of_files}, 200
    # - Failure: {"error": "No location name provided"}, 400
    #            {"error": "No matching files found"}, 404
    locationname = request.args.get('locationname')
    if not locationname:
        return jsonify({"error": "No location name provided"}), 400
    
    matching_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.split('_')[1] == locationname]
    if not matching_files:
        return jsonify({"error": "No matching files found"}), 404
    
    file_dict = {}
    for file in matching_files:
        base_name = '_'.join(file.split('_')[3:])
        if base_name not in file_dict or file_dict[base_name].split('_')[2] < file.split('_')[2]:
            file_dict[base_name] = file
    
    return jsonify({"files": list(file_dict.values())}), 200

@app.route('/sendtolocation', methods=['POST'])
def send_to_location():
    # Upload a file to a specific location directory under /home/ubuntu/locations.
    
    # Request: 
    # - POST request
    # - Multipart form-data with a file and a locationname
    
    # Response:
    # - Success: {"message": "File uploaded successfully", "locationname": locationname, "filename": filename}, 200
    # - Failure: {"error": "No file part"}, 400
    #            {"error": "No location name provided"}, 400
    #            {"error": "No selected file"}, 400
    #            {"error": "File type not allowed"}, 400
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    locationname = request.form.get('locationname')
    if not locationname:
        return jsonify({"error": "No location name provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        location_folder = os.path.join(LOCATIONS_FOLDER, locationname)
        os.makedirs(location_folder, exist_ok=True)
        filename = secure_filename(file.filename)
        file.save(os.path.join(location_folder, filename))
        return jsonify({"message": "File uploaded successfully", "locationname": locationname, "filename": filename}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5462, debug=True)

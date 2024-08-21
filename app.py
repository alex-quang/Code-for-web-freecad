from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-box', methods=['POST'])
def generate_box():
    try:
        data = request.json
        length = data.get('length')
        width = data.get('width')
        height = data.get('height')
        material = data.get('material')
        color = data.get('color')

        if not all([length, width, height, material, color]):
            raise ValueError("All dimensions, material, and color must be provided.")

        result = subprocess.run(
            ['python3', 'generate_box.py', str(length), str(width), str(height), material, color],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        response = {'success': True, 'file_url': 'box.stl'}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return jsonify(response)

@app.route('/api/generate-pipeline', methods=['POST'])
def generate_pipeline():
    try:
        data = request.json
        length = data.get('pipeline_length')
        diameter = data.get('pipeline_diameter')
        thickness = data.get('pipeline_thickness')

        if not all([length, diameter, thickness]):
            raise ValueError("All dimensions must be provided.")

        result = subprocess.run(
            ['python3', 'generate_pipeline.py', str(length), str(diameter), str(thickness)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        response = {'success': True, 'file_url': 'pipeline.stl'}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return jsonify(response)

@app.route('/api/generate-staircase', methods=['POST'])
def generate_staircase():
    try:
        data = request.json
        num_steps = data.get('num_steps')
        step_length = data.get('step_length')
        step_width = data.get('step_width')
        step_height = data.get('step_height')

        if not all([num_steps, step_length, step_width, step_height]):
            raise ValueError("All dimensions must be provided.")

        result = subprocess.run(
            ['python3', 'generate_staircase.py', str(num_steps), str(step_length), str(step_width), str(step_height)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        response = {'success': True, 'file_url': 'staircase.stl'}
    except Exception as e:
        response = {'success': False, 'error': str(e)}
    return jsonify(response)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


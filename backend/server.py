from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)

DATA_FILE = '../data/proyectos.json'

def load_projects():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_projects(projects):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2)

@app.route('/api/projects', methods=['GET'])
def get_projects():
    return jsonify(load_projects())

@app.route('/api/vote/<int:project_id>', methods=['POST'])
def vote_project(project_id):
    projects = load_projects()
    for project in projects:
        if project['id'] == project_id:
            project['votes'] += 1
            save_projects(projects)
            return jsonify({'success': True, 'votes': project['votes']})
    return jsonify({'error': 'Project not found'}), 404

@app.route('/api/execute', methods=['POST'])
def execute_code():
    code = request.json.get('code', '')
    try:
        with open('temp.py', 'w', encoding='utf-8') as f:
            f.write(code)
        output = subprocess.check_output(['python', 'temp.py'], stderr=subprocess.STDOUT, timeout=5)
        return jsonify({'output': output.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        return jsonify({'output': e.output.decode('utf-8')})
    except Exception as e:
        return jsonify({'output': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


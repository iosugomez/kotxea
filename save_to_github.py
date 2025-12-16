import os
import json
from flask import Flask, request, jsonify
from github import Github
from datetime import datetime

# Configuración
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')  # Debes exportar tu token como variable de entorno
REPO_NAME = 'iosugomez/kotxea'
DATA_PATH = 'datos/datos.json'  # Ruta dentro del repo donde guardar los datos

app = Flask(__name__)

def get_github_repo():
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    return repo

@app.route('/save', methods=['POST'])
def save_data():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    repo = get_github_repo()
    try:
        # Leer el archivo actual (si existe)
        try:
            contents = repo.get_contents(DATA_PATH)
            sha = contents.sha
        except Exception:
            contents = None
            sha = None
        # Guardar los nuevos datos
        commit_message = f"Update datos.json {datetime.now().isoformat()}"
        content_str = json.dumps(data, indent=2, ensure_ascii=False)
        if sha:
            repo.update_file(DATA_PATH, commit_message, content_str, sha)
        else:
            repo.create_file(DATA_PATH, commit_message, content_str)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

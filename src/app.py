import os
import uuid
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DATABASE'] = 'images.db'
apikeys = ['913219372139493298439478932']
def create_table():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                upload_date DATETIME NOT NULL,
                title TEXT,
                hexcolor TEXT,
                description TEXT
            )
        ''')
        conn.commit()

create_table()

def insert_image(filename, title, hexcolor, description):
    image_id = str(uuid.uuid4())
    upload_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO images (id, filename, upload_date, title, hexcolor, description) VALUES (?, ?, ?, ?, ?, ?)', (image_id, filename, upload_date, title, hexcolor, description))
        conn.commit()


def get_images():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM images ORDER BY upload_date DESC')
        return cursor.fetchall()

@app.route('/')
def index():
    images = get_images()
    return render_template('index.html', images=images)
def get_image_id(filename):
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM images WHERE filename = ?', (filename,))
        result = cursor.fetchone()
        return result[0] if result else None
    
@app.route('/upload', methods=['POST'])
def upload():
    APIKEY = request.headers.get('apikey', '')
    if APIKEY in apikeys:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if not file or file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        title = request.headers.get('title', 'Default Title')
        hexcolor = request.headers.get('hexcolor', '#000000')
        description = request.headers.get('description', '')

        insert_image(filename, title, hexcolor, description)

        image_id = get_image_id(filename)
        unique_url = url_for('get_image', image_id=image_id, _external=True)

        return unique_url
    else:
        return jsonify({'error': 'Access Denied'}), 404

@app.route('/image/<image_id>')
def get_image(image_id):
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT filename, title, hexcolor, description FROM images WHERE id = ?', (image_id,))
        result = cursor.fetchone()

        if result:
            filename, title, hexcolor, description = result
            app.logger.debug(f"Debug: Retrieved title from database: {title}")

            if title is not None:
                return render_template('image.html', image_url=url_for('uploaded_file', filename=filename), title=title, hexcolor=hexcolor, description=description)
            else:
                return render_template('image.html', image_url=url_for('uploaded_file', filename=filename), title="No Title Available", hexcolor="#FFFFFF", description="")
        else:
            return jsonify({'error': 'Image not found'}), 404
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

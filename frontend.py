# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from filesystem import FileSystem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Provide the root directory path when creating the FileSystem instance
fs = FileSystem(root='C:/Users/ishwa/OneDrive/Desktop/OS_mini_project')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_file', methods=['POST'])
def create_file():
    file_path = request.form['file_path']
    data = request.form['data']
    
    try:
        fs.insert_file(file_path, data)
        flash('File created successfully!', 'success')
    except FileNotFoundError:
        flash('Error creating file: Directory not found.', 'danger')
    except Exception as e:
        flash(f'Error creating file: {str(e)}', 'danger')

    return redirect(url_for('index'))

@app.route('/create_directory', methods=['POST'])
def create_directory():
    directory_path = request.form['directory_path']
    
    try:
        fs.create_directory(directory_path)
        flash('Directory created successfully!', 'success')
    except FileNotFoundError:
        flash('Error creating directory: Parent directory not found.', 'danger')
    except Exception as e:
        flash(f'Error creating directory: {str(e)}', 'danger')

    return redirect(url_for('index'))

@app.route('/view_dir', methods=['POST'])
def view_dir():
    directory_path = request.form['view_directory']
    files = fs.list_files(directory_path)
    return render_template('index.html', files=files, directory_path=directory_path)

@app.route('/search_file', methods=['POST'])
def search_file():
    file_name = request.form['search_file']
    target_directory = request.form['search_directory']
    found_files = fs.search_file(file_name, target_directory)
    return render_template('index.html', found_files=found_files)

if __name__ == '__main__':
    app.run(debug=True)

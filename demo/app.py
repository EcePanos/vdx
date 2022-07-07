from flask import Flask, render_template, request, send_file
import hybrid
import avg
import history
import module_elimination
import dynamic_threshold
import time
import group
import combo

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/"

@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/display', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = 'input.csv'
        algorithm = request.form['algorithm']
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        start_time = time.time()
        if algorithm == 'average':
            avg.merge(app.config['UPLOAD_FOLDER'] + filename)
        elif algorithm == 'HBWA':
            history.merge(app.config['UPLOAD_FOLDER'] + filename)
        elif algorithm == 'MEWA':
            module_elimination.merge(app.config['UPLOAD_FOLDER'] + filename)
        elif algorithm == 'DTHBWA':
            dynamic_threshold.merge(app.config['UPLOAD_FOLDER'] + filename)
        elif algorithm == "HHBWA":
            hybrid.merge(app.config['UPLOAD_FOLDER'] + filename)
        elif algorithm == 'CMM':
            group.merge(app.config['UPLOAD_FOLDER'] + filename)
        elif algorithm == 'HCMM':
            combo.merge(app.config['UPLOAD_FOLDER'] + filename)

        exec_time = round(time.time() - start_time, 4) * 1000
        file = open(app.config['UPLOAD_FOLDER'] + 'output.csv',"r")
        content = file.read()


    return render_template('content.html', content=content, algorithm=algorithm, exec_time=exec_time)

@app.route('/download')
def download_file():
	path = app.config['UPLOAD_FOLDER'] + 'output.csv'
	return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug = True)

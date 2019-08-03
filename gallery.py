#!/usr/bin/env python3
from flask import Flask, render_template, request
import time
from pathlib import Path
app = Flask(__name__)

@app.route('/gallery/', defaults={'path': ''})
@app.route('/gallery/<path:path>')
def overview(path):
    #directory to watch
    location = 'gallery'
    
    p = Path(location+"/"+path)
    #recursively find all files in directory
    files = []
    for f in p.rglob('**/*.*'):
      files.append({
         "name" : f.name,
         "location" : str(f.relative_to(location).parents[0]),
         "age" : int(time.time() - f.stat().st_ctime),
      })

    #sort found files by age
    files = sorted(files, key = lambda x: x['age'])

    #generate directory listing                                                                           
    dirs = []
    for f in (p.glob('./*')):
        if f.is_dir():
            dirs.append(str(f).replace(location+"/"+path,"").strip("/"))

    #render template with files
    return(render_template('index.html', files = files[:6*4], dirs = dirs, path = path))

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, True)

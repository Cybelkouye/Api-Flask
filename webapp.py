from flask import Flask, make_response, request
import hashlib as hsh

app = Flask(__name__)

def transform(text_file_contents):
    return text_file_contents.replace("=", ",")

def cypher(text_file_contents,key): 
    keys = hsh.sha256(key.encode('utf-8')).digest()
    test = ''
    f_entree = "motdepasse"
    i=0
    for car in text_file_contents: 
        c = ord(car)
        j = i % len(keys)
        #coeur de la fonction de chiffrement, chiffrement pas XOR, on XOR ce qu'on a lu précédemment 
        b = bytes([c^keys[j]]) 
        s = ''.join(map(chr, b))
        test = test + s
        i=i+1
    return test

def decypher():
    key ='test'
    keys = hsh.sha256(key.encode('utf-8')).digest()
    test1 = ''
    f_sortie = 'òé¤åí<\x1c\x16éJ'
    i=0
    for car in f_sortie:
        c = ord(car)
        j = i % len(keys)
        #coeur de la fonction de chiffrement, déchiffrement par XOR, on XOR ce qu'on a lu précédemment 
        b = bytes([keys[j]^c])
        s = ''.join(map(chr, b))
        test1 = test1 + s
        i=i+1 
    return test1

@app.route('/')
def form():
    return """
        <html>
            <body>
                <h1>Transform a file demo</h1>

                <form action="/transform" method="post" enctype="multipart/form-data">
                    <input type="file" name="data_file" />
                    <input type="text" name="key" />
                    <input type="submit" />
                </form>
            </body>
        </html>
    """

@app.route('/transform', methods=["POST"])
def transform_view():
    key = request.form["key"]
    file = request.files['data_file']
    if not file:
        return "No file"

    file_contents = file.stream.read().decode("utf-8")

    result = cypher(file_contents,key)
    

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.txt"
    return response
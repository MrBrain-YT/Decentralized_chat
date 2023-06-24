from flask import Flask, request

oldText = ""

def GetMessangeServer():
    app = Flask(__name__)
    @app.route('/')
    def ReciveMessage():
        global oldText
        Text = request.args.get('Text')
        if Text is None:
            return oldText
        else:
            oldText = Text
            return oldText
        
    @app.route('/Delete')
    def DeleteMessage():
        global oldText
        oldText = ""
        return oldText

    app.run()

# GetMessangeServer()
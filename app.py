import os
from flask import Flask, render_template, request, url_for
from lark import Lark 


app = Flask(__name__)

grammar = r'''
    start : [colorn] SHAPE ["at " pair] ["size of " pair]
    pair  : NUMBER","NUMBER
    colorn: COLOR
          | hex
    hex   : "#"(DIGIT|LETTER)(DIGIT|LETTER)(DIGIT|LETTER)(DIGIT|LETTER)(DIGIT|LETTER)(DIGIT|LETTER)

    COLOR : LETTER+
    SHAPE : LETTER+
    DIGIT : ("0".."9")
    %import common.LETTER
    %import common.INT -> NUMBER
    %import common.WS
    %ignore WS
    '''
parser = Lark(grammar)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        statement = request.form.get('statement')
        print(parser.parse(statement).pretty())
    return render_template('index.html');


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

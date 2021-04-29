import os
from flask import Flask, render_template
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

@app.route('/')
def index():
    return render_template('index.html', message='by Kyle Brown');


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8000, debug=True)
    parser = Lark(grammar)

    print(parser.parse('#fff000 oval at 50,50 size of 400,300').pretty())

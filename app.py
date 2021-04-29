import os
from flask import Flask, render_template, request, url_for
from lark import Lark 


app = Flask(__name__)

grammar = r'''
    start : [colorn] shapen ["at " pair] ["size of " pair]
    pair  : NUMBER","NUMBER
    colorn: COLOR
          | hex
    hex   : "#"(DIGIT|LETTER)(DIGIT|LETTER)(DIGIT|LETTER)(DIGIT|LETTER)(DIGIT|LETTER)(DIGIT|LETTER)
    shapen: SHAPE

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
        color='#000000'
        x = 0
        y = 0
        w = 100
        h = 100
        shape = None

        statement = request.form.get('statement')
        parsed = parser.parse(statement)

        # print(parsed.children[1].children[1])
        if parsed.children[0].data == 'colorn':
            color_name = parsed.children[0].children[0]
            if color_name == 'red':
                color = '#ff0000'
            elif color_name == 'blue':
                color = '#0000ff'
            elif color_name == 'green':
                color = '#00ff00'
            elif color_name == 'yellow':
                color = '#ffff00'
            else:
                color = color_name
        elif parsed.children[0].data == 'shapen':
            shape = parsed.children[0].children[0]

        if len(parsed.children) > 1:
            x = int(parsed.children[1].children[0])
            y = int(parsed.children[1].children[1])
        elif len(parsed.children) > 2:
            w = int(parsed.children[2].children[0])
            h = int(parsed.children[2].children[1])

    return render_template('index.html');


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

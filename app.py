import os
from flask import Flask, render_template, request, url_for
from lark import Lark 


app = Flask(__name__)

grammar = r'''
    start : [colorn] shapen [at] [sizeof]
    pair  : NUMBER","NUMBER
    at    : "at" pair      -> position
    sizeof: "size of" pair -> size
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
        js_draw_command = None

        statement = request.form.get('statement')
        if statement:
            parsed = parser.parse(statement)

            for tree in parsed.children:
                if tree.data == 'colorn':
                    color_name = tree.children[0]
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
                elif tree.data == 'shapen':
                    shape = tree.children[0]
                elif tree.data == 'position':
                    x = tree.children[0].children[0]
                    y = tree.children[0].children[1]
                elif tree.data == 'size':
                    x = tree.children[0].children[0]
                    y = tree.children[0].children[1]

            print(f'x: {x} y: {y} w: {w} h: {h} color: {color}')
            # Generate shapes
            if shape == 'rectangle':
                js_draw_command = f'''
                ctx.fillStyle = {color};
                ctx.fillRect({x}, {y}, {w}, {h});
                '''
    return render_template('index.html', js_draw_command=js_draw_command);


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

import sys
from os import path
import re
from pathlib import Path
from textwrap import dedent


def get_html_tags(string, start_tag='>', end_tag='>'):
    tags = list()
    for s in string.split(start_tag):
        tags.append(s.split(end_tag, 1)[0])

    return tags


def get_tags(string, start_tag, end_tag, include_tags=False):
    tags = list()

    for ss in string.split(start_tag)[1:]:
        content = ss.split(end_tag)[0]
        if include_tags:
            content = start_tag + content + end_tag
        tags.append(content)

    return tags


# --------------------------------------------------------------------
path = Path('.')
ignore = '_*'
for arg in sys.argv:
    if arg.startswith('--ignore='):
        ignore = arg.split('=')[1]


if len(list(path.glob('*.txt'))) == 0:
    print('no text file found')
    sys.exit('no text file found')

for txt in path.glob('*.txt'):
    #  skip ignored files
    if ignore.endswith('*'):
        if txt.name.startswith(ignore[:-1]):
            print('skip file:', txt)
            continue
    if txt.name == ignore:
        print('skip file:', txt)
        continue

    # print(txt.stem)
    with open(txt, 'r', encoding='utf-8') as t:
        text = t.read()

    new_text = ''
    new_text += dedent('''
        <!--generated with sswg-->
        <style>
            html {max-width: 100%; margin: auto; color: #333333;}
            a.button {padding: 15px 32px; background-color: #555; border-radius: 2em; border-width: 0px; text-decoration: none; color: white; font-size: 25.0px; line-height: 2.5em;}
            a.button:hover {background-color: #777}
            a.button_big {padding: 0.5em; background-image: linear-gradient(to top, #427b0e, #9ba97d); background-color: lightgray; background-blend-mode: multiply; border-radius: .75em; border-width: 0px; text-decoration: none; min-width: 150px; max-width: 150px; min-height: 150px; max-height: 150px; display: inline-block; vertical-align: top; margin: 4px 4px 10px 4px; color: white; font-size: 25.0px; background-size: auto 100%; background-position-x: center;}
            a.button_big:hover {background-color: white; color: #e6d23f; text-decoration: underline;}
            mark {background: #ccff99;}
            span {background-color: rgba(0, 0, 0, 0.55); padding: .1em; line-height: 1.35em;}
            img {max-width: 100%; vertical-align: top;}
            .code_block {background-color: whitesmoke; padding: 10px; margin: 0; font-family: monospace; font-size: 20; font-weight: normal; white-space: pre;}
    ''')
    if text.startswith('# style'):
        new_text += text.split('\n')[0].split('# style ')[1]

    new_text += dedent('''
        </style>
        <html>
        <left>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    ''')

    if '# title' in text:
        title = text.split('# title')[1].split('\n',1)[0]
    else:
        title = txt.stem

    new_text += '<title>' + title + '</title>\n<br>\n\n'

    # parse tags and ignore commented lines
    current_alignment = 'left'
    current_scale = 5
    current_font_weight = 'normal'
    current_font_style = 'normal'
    is_code_block = False
    inline_images = list()

    lines = text.split('\n')

    # add support for markdown inspired tags
    new_lines = list()
    for l in lines:
        if l.startswith('### '):
            new_lines.extend(['# size 3, bold', f'<div id="{l[4:]}"/>', l[4:], '# size 1, normal'])
            continue

        if l.startswith('## '):
            new_lines.extend(['# size 2, bold', f'<div id="{l[3:]}"/>', l[3:], '# size 1, normal'])
            continue

        elif l.startswith('# insert') or l.startswith('#insert'):
            path = l.split('insert', 1)[1].strip()
            if path.startswith('Path('):
                path = eval(path)

            with open(path, 'r', encoding='utf-8') as text_file:
                new_lines.extend(text_file.readlines())
            continue

        new_lines.append(l)

    lines = new_lines

    for i, line in enumerate(lines):
        # print(line)
        original_line = line
        if line.strip().startswith('#'):
            indent = len(line) - len(line.lstrip())
            line = line.strip()[1:].strip()
            tags = [tag.strip() for tag in line.split(',')]

            div_class = ''
            style = ''
            for tag in tags:
                if tag.startswith('width'):
                    tag = tag.split(' ')[1]
                    style += f'max-width: {tag}px; margin: auto;'

                elif tag in ('left', 'right', 'center'):
                    # print('tag', tag)
                    if tag != current_alignment:
                        style += 'text-align: ' + tag + ';'
                        current_alignment = tag

                elif tag.startswith('scale') or tag.startswith('size'):
                    new_scale = tag.split(' ')[1]
                    # print('tag', new_scale)
                    if tag != new_scale:
                        style += 'font-size: ' + str(float(new_scale)*20) + 'px;'
                        current_scale = new_scale

                elif tag in ('normal', 'bold', 'bolder', 'lighter'):
                    if tag != current_font_weight:
                        style += 'font-weight: ' + tag + ';'
                        current_font_weight = tag

                elif (tag.lower() in
                    ('arial', 'times', 'helvetica', 'courier', 'courier new', 'verdana', 'tahoma', 'bookman', 'monospace')):
                    style += f'font-family: {tag.lower()};'


                elif tag.startswith('image'):
                    image_name = tag[len(tag.split(' ')[0]):].strip()
                    print('.............', image_name)
                    for ft in ('.jpg', '.png', '.gif'):
                        if image_name.endswith(ft):
                            new_text += f'<img src="{image_name}"></img> <br>\n'
                            inline_images.append(image_name)

                elif tag.startswith('background'):
                    style += 'background-color: ' + tag.split(' ')[1] + ';'

                elif tag.startswith('code'):
                    is_code_block = True
                    style += f'margin-left: {indent//4}em;'
                    div_class = 'code_block'

                elif tag.startswith('text'):  # end code block
                    new_text += '</div>'
                    is_code_block = False


            if style:
                if div_class:
                    div_class = f'class="{div_class}" '

                new_text += f'<div {div_class}style="{style}">'

                if not is_code_block:
                    new_text += '\n'

            elif is_code_block: # keep comments in code blocks
                new_text += '<font color="gray">' + original_line.lstrip() + '</font>' + '\n'

        else:
            is_image_button = False
            if is_code_block:
                # purple olive green
                line = line[indent:]
                line = line.replace('def ', '<font color="purple">def</font> ')
                line = line.replace('from ', '<font color="purple">from</font> ')
                line = line.replace('import ', '<font color="purple">import</font> ')
                line = line.replace('Entity', '<font color="olive">Entity</font>')

                quotes = re.findall('\'(.*?)\'', line)
                quotes = ['\'' + q + '\'' for q in quotes]
                for q in quotes:
                    line = line.replace(q, '<font color="green">' + q + '</font>')

                if original_line.endswith('# +'): # highlight line in code block
                    line = '<mark>' + line.replace('# +', '</mark>')
                elif line.endswith('# -'): # highlight line in code block
                    line = '<mark style="background:#ff9999;"> ' + line.replace('# -', '</mark>')

                elif ' #' in line:
                    line = line.replace(' #', ' <font color="gray">#')
                    line += '</font>'

            else:
                buttons = get_tags(line, '[', ']')

                for b in buttons:
                    if not ',' in b:
                        print(line)
                        continue

                    # print('button:', b)
                    number_of_commas = b.count(',')
                    name, link, image = b, '', None

                    if number_of_commas == 1:
                        name, link = b.split(',')
                        line = line.replace(f'[{b}]', f'''<a href="{link}" class="button">{name}</a>''')

                    elif number_of_commas == 2:
                        name, link, image = b.split(',')
                        is_image_button = True
                        image_code = ''
                        if len(image.strip()) > 0:
                            image_code = f'''style="background-image: url('{image.strip()}')"'''
                        # line += f'''<a href="{link}" class="button_big" {image_code}><span>{name}</span></a>'''
                        line = line.replace(f'[{b}]', f'''<a href="{link}" class="button_big" {image_code}><span>{name}</span></a>''')

                # line += '<br>'
                line = line.replace('  ', '&nbsp;&nbsp;')


            if 'http' in line and not 'class="button' in line:  # find urls and convert them to links
                words = line.split(' ')
                words = [f'<a href="{w}">{w}</a>' if w.startswith('http') else w for w in words]
                line = ' '.join(words)


            new_text += line
            if not is_image_button:
                new_text += '<br>'
            if not is_code_block:
                new_text += '\n'


    new_text += '\n</html>'


    with open(txt.stem + '.html', 'w', encoding='utf-8') as text_file:
        text_file.write(new_text)
        print('finished building:', txt.stem + '.html')

# Sentinel.py
"""
Parses screenplays into subsections: headings, transitions, actions, paretheticals, and dialogue,
to be further prepared into Markov models.
"""
import os
import re
import time


def remove_tags(markup):
    """
    returns markup with all tags removed
    """
    pattern = re.compile(r'<.*?>')
    return re.sub(pattern, '', markup)


def get_lines_from_block(text):
    """
    finds the first matching multi-line block of text
    returns tuple of (num_lines, block)
    """
    ml_block = []
    line = remove_tags(text[0])
    cur_indent = len(line) - len(line.lstrip())

    for i in range(len(text)):
        next_line = remove_tags(text[i])
        next_indent = len(next_line) - len(next_line.lstrip())

        if cur_indent == next_indent: # multiline block
            deline = next_line.strip()
            if deline:
                ml_block.append(deline)

        else: # end of block, return (num_lines, block)
            if ml_block:
                return (i, ' '.join(ml_block))
            break

    # no block found
    return (0, '')


def parse(directory='.', genre='All'):
    """
    Writes a compilation of all headings, transitions, actions,
    parentheticals, and dialogue as separate files.
    """
    categories = {
        'headings': [],
        'actions': [],
        'characters': [],
        'dialogue': [],
        'parentheticals': []
    }

    # iterate through all the files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isdir(filepath):
            start = time.time()
            print('Parsing', filename, '...')
            parsed_genre = parse(filepath, genre=filename)
            print(f'Finished in {time.time() - start} s')
            for category in parsed_genre:
                categories[category] += parsed_genre[category]

        if filename.endswith('.html'):
            filename = os.path.join(directory, filename)
            with open(filename, encoding='utf-8') as f:
                screenplay = f.readlines()

            char = False
            i = 0

            while i < len(screenplay):
                line = remove_tags(screenplay[i])
                deline = line.strip()

                # Empty
                if len(deline) == 0:
                    pass
                else:
                    # Heading
                    first = deline.split()[0].upper()
                    if first.startswith('INT') or first.startswith('EXT'):
                        char = False
                        categories['headings'].append(deline)

                    elif line.isupper():
                        # Transition
                        if deline in ['CUT TO:', 'FADE IN:', 'FADE OUT:', 
                                      'DISSOLVE TO:', 'SMASH CUT:', 'END CREDITS:', 
                                      'CUT TO BLACK:', 'CONTINUED:', '(CONTINUED)']:
                            pass

                        # Character
                        else:
                            categories['characters'].append(deline)
                            char = True

                    elif char:
                        # Parenthetical
                        if deline[0] == '(':
                            if deline[-1] == ')':
                                categories['parentheticals'].append(deline[1:len(deline)-1])

                        # Dialogue
                        else:
                            char = False
                            num_lines, ml_dia = get_lines_from_block(screenplay[i:i+80])
                            categories['dialogue'].append(ml_dia)
                            i += num_lines

                    # Action
                    else: 
                        num_lines, ml_act = get_lines_from_block(screenplay[i:i+40])
                        categories['actions'].append(ml_act)
                        i += num_lines 

                i += 1

    # write to files
    for key in categories:
        filename = f'./parsed_categories/{key.upper()}_{genre}'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(categories[key]))

    return categories


if __name__ == '__main__':
    start = time.time()
    parse('Genres')
    print(f'Finished parsing all screenplays in {time.time() - start} s.')
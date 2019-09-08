"""
# Sentinel.py

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


def clean(line):
    """
    returns line with undesirable characters removed
    """
    line = remove_tags(line)
    line = re.sub(re.compile(r'^\.{4,}'), '', line)
    line = re.sub(re.compile(r'^-{4,}'), '', line)
    line = re.sub(re.compile(r'^\d.?'), '', line)
    return line

def get_lines_from_block(text):
    """
    finds the first matching multi-line block of text
    returns tuple of (num_lines, block)
    """
    ml_block = []
    line = clean(text[0])
    cur_indent = len(line) - len(line.lstrip())

    for i in range(len(text)):
        next_line = clean(text[i])
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


def parse(*sources, destination='.', write=True):
    """
    Writes a compilation of all headings, transitions, actions,
    parentheticals, and dialogue as separate files.
    """
    categories = {
        'headings': [],
        'actions': [],
        'dialogue': [],
        'parentheticals': []
    }

    for filename in sources:
        start = time.time()
        # print('Parsing', filename, '...')
        with open(filename, encoding='utf-8') as f:
            screenplay = f.readlines()
        char = False
        i = 0

        while i < len(screenplay):
            line = clean(screenplay[i])
            deline = line.strip()

            # Empty
            if len(deline) == 0:
                pass
            else:
                # Heading
                first = deline.split()[0]
                if first.startswith('INT') or first.startswith('EXT'):
                    char = False
                    heading = re.sub(r'^\W*(INT|EXT).?\W*', '', deline)
                    categories['headings'].append(heading)

                # Parenthetical
                elif deline[0] == '(':
                    if deline[-1] == ')':
                        paren = deline[1:len(deline)-1].strip()
                        if paren:
                            categories['parentheticals'].append(paren)

                elif deline.isupper():

                    # Transition
                    if deline.strip(':') in ['CUT TO', 'FADE IN', 'FADE OUT', 
                                  'DISSOLVE TO', 'SMASH CUT', 'END CREDITS', 
                                  'CUT TO BLACK', 'CONTINUED', '(CONTINUED)']:
                        pass

                    # Character
                    else:
                        char = True

                # Dialogue
                elif char:
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
        # print(f'Finished in {time.time() - start} s')

    if write:
        for key in categories:
            filename = os.path.join(destination, key.upper())
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(categories[key]))
    return categories



def parse_directory(source_dir='.', destination='parsed_categories', genre='All'):
    """
    Parses specified directory
    """
    categories = {
        'headings': [],
        'actions': [],
        'dialogue': [],
        'parentheticals': []
    }

    # iterate through all the files in the directory
    for filename in os.listdir(source_dir):
        filepath = os.path.join(source_dir, filename)
        # recursively parse genre directories
        if os.path.isdir(filepath):
            start = time.time()
            print('Parsing', filename, '...')
            parsed_genre = parse_directory(filepath, genre=filename)
            print(f'Finished in {time.time() - start} s')

            for category in parsed_genre:
                categories[category] += parsed_genre[category]

        # parse individual screenplays
        elif filename.endswith('.html'):
            filename = os.path.join(source_dir, filename)
            parsed_file = parse(filename, write=False)
            for category in parsed_file:
                categories[category] += parsed_file[category]

    # create directory if it doesn't exist
    try:
        os.mkdir(destination)
    except FileExistsError:
        pass

    # write to files
    if genre != 'All':
        for key in categories:
            filename = os.path.join(destination, key.upper())
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(categories[key]))
        return categories


if __name__ == '__main__':
    start = time.time()
    parse_directory('Genres')
    print(f'Finished parsing all screenplays in {time.time() - start} s.')
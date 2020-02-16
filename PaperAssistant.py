import os
import re
from collections import defaultdict


class PaperAssistant:
    def __init__(self, tex_folder=None, bib_path='anthology.bib'):
        self.tex_folder = tex_folder
        self.bib_path = bib_path

    def get_bib(self, title):
        '''
        Find a bibtex in a .bib by title and copy to clipboard automatically (only string match supported now)
        requires pip install pyperclip
        '''
        import pyperclip
        title = ' '.join([i for i in title.split() if i != ' ']).lower()
        lastLine = ''
        with open(self.bib_path, encoding='utf8') as bibtex_file:
            for line in bibtex_file:
                if title in line.lower():
                    print(lastLine, line)
                    name = lastLine[lastLine.find('{') + 1:].strip()[:-1]
                    pyperclip.copy(name)  # send to clipboard
                    # read the clipboard
                    print(pyperclip.paste(), '[copied!!!]')
                    break
                lastLine = line
        return name

    def remove_tex_comments(self):
        '''
        Be careful!!! All the comments (line starting with %) in the tex files will be deleted.
        '''
        for dirpath, dirnames, filenames in os.walk(self.tex_folder):
            for filename in filenames:
                if filename.endswith('tex'):
                    path = os.path.join(dirpath, filename)
                    print(path)
                    with open(path) as f:
                        res = [
                            line for line in f if not line.strip().startswith('%')]
                    with open(path, 'w') as o:
                        for line in res:
                            o.write(line)

    def count_ref(self):
        '''
        Count how many times you cite papers in your tex files, so that you can remove those rare ones if desired.
        '''
        ref_ct = defaultdict(int)
        for dirpath, dirnames, filenames in os.walk(self.tex_folder):
            for filename in filenames:
                if filename.endswith('tex'):
                    path = os.path.join(dirpath, filename)
                    print(path)
                    with open(path, encoding='utf8') as f:
                        for line in f:
                            if line.startswith('%'):
                                continue
                            ref_l = re.findall('cite{.*?}', line)
                            for refs in ref_l:
                                for ref in refs[5:-1].split(','):
                                    ref_ct[ref.strip()] += 1

        sorted_ref_ct = sorted(list(ref_ct.items()), key=lambda x: x[1])
        print(sorted_ref_ct)
        return sorted_ref_ct


if __name__ == "__main__":
    tex_folder = 'XXX'
    bib_path = 'anthology.bib' 
    pa = PaperAssistant(tex_folder=tex_folder, bib_path=bib_path)

    title = 'ring content models for multi-document summ'
    pa.get_bib(title)
    pa.count_ref()
    # cannot be undone!
    pa.remove_tex_comments()

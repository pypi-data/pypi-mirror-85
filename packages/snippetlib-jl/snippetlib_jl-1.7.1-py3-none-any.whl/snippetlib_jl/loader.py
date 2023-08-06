import os

from pathlib import PurePath,Path

from jupyter_core.paths import jupyter_path
import sys 

import tornado
import os 


class SnippetsLoader:
    '''
    This is a modified class from the developed snippets loader here
    https://github.com/QuantStack/jupyterlab-snippets
    '''
    def __init__(self):
        dirr = os.path.dirname(os.path.abspath(__file__))
        self.snippet_paths = [os.path.join(dirr,"menu","KD-Snippets")]
        print("SNIPPET PATHS",self.snippet_paths)
        
    def collect_snippets(self):
        snippets = []
        base = [('How to create new snippets.py',),('How to upload your snippets.py',),('Base imports.py',)]
        for root_path in self.snippet_paths:
            for dirpath, dirnames, filenames in os.walk(root_path, followlinks=True):
                for f in filenames:
                    fullpath = PurePath(dirpath).relative_to(root_path).joinpath(f)

                    if fullpath.parts not in snippets:
                        if fullpath.parts in base or fullpath.parts in ['__pycache__']:
                            pass
                        else:
                            snippets.append(fullpath.parts)
        # snippets.sort()
        snippets.extend(base)
        snippets = self.clean_snippets_list(snippets)
        return snippets

    def clean_snippets_list(self,snippets):
        index_list = []
        copy = snippets[:]

        for snippet in snippets: 

            if snippet[0].endswith('.ipynb_checkpoints') or snippet[0].endswith('.ipynb') or snippet[0].endswith('__pycache__'):
                index_list.append(snippets.index(snippet))

        for index in index_list:
            snippets.remove(copy[index])
            
        return snippets

    def get_current_directory(self):
        return os.path.dirname(os.path.abspath(__file__))

    def get_snippet_content(self, snippet):
        try:
            for root_path in self.snippet_paths:
                path = os.path.join(root_path, *snippet)

                # Prevent access to the entire file system when the path contains '..'
                accessible = os.path.abspath(path).startswith(root_path)
                if not accessible:
                    print(f'jupyterlab-snippets: {path} not accessible from {root_path}')

                if accessible and os.path.isfile(path):
                    with open(path) as f:
                        return f.read()
        except:
            raise tornado.web.HTTPError(status_code=500)

        print(f'jupyterlab-snippets: {snippet} not found in {self.snippet_paths}')
        raise tornado.web.HTTPError(status_code=404)
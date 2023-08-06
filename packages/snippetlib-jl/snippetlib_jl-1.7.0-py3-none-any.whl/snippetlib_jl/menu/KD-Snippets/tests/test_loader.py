import unittest 

from snippetlib_jl.loader import SnippetsLoader as sl

class TestLoader(unittest.TestCase):
    def test_list(self):
        '''Ensure that a list is not empty'''
        s = sl()
        
        content_exist = lambda content : content is not None
        try: 
            snippets_paths = s.collect_snippets()
            one_snippet_content = s.get_snippet_content(snippets_paths[0])

        except IndexError: 
            snippets_paths = one_snippet_content = None

        self.assertIsNotNone(snippets_paths)
        self.assertIsNotNone(one_snippet_content)

            

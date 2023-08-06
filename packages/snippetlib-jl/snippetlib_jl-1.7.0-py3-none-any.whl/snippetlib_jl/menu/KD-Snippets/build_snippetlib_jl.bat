pip install snippetlib-jl
jupyter serverextension enable --py snippetlib_jl
jlpm
jlpm build
jupyter labextension link .
jlpm build
jupyter lab build

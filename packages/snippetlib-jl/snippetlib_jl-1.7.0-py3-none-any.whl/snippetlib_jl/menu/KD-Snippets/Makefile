all: wheel

install: wheel

	pip uninstall -y snippetlib_jl || true
	jupyter labextension uninstall snippetlib_jl
	pip install dist/snippetlib_jl-*.whl
	jlpm 
	jlpm build 
	jupyter labextension link .
	jlpm build 
	jupyter lab build 

install_configure: wheel

	# pip install snippetlib_jl
	pip install dist/snippetlib_jl-*.whl
	jupyter serverextension enable --py snippetlib_jl
	jlpm
	jlpm build
	jupyter labextension link .
	jlpm build
	jupyter lab build
	
install_develop: wheel 

	pip uninstall -y snippetlib_jl || true
	pip install dist/snippetlib_jl-*.whl
	

wheel:
	rm -rf build dist
	python setup.py bdist_wheel


install_pipeline: wheel
	pip uninstall -y snippetlib_jl || true
	pip install dist/snippetlib_jl-*.whl



.PHONY: all wheel install



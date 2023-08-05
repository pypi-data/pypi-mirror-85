#SOURCE_NAME?=$(shell < oda.yaml yq -r '.metadata.source_short_name')
SOURCE_NAME?=$(shell python3 -c 'import yaml; print(yaml.safe_load(open("oda.yaml")).get("metadata",{}).get("source_short_name","unnamed"))')


mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
#current_version := $(shell cd $(current_dir); git describe --tags)

c="bash -c '. $(current_dir)/make-functions.sh && $@'"

pull: 
	bash -c '. $(current_dir)/make-functions.sh && $@'

build: pull
	bash -c '. $(current_dir)/make-functions.sh && $@'

push: build
	bash -c '. $(current_dir)/make-functions.sh && $@'

clean:
	bash -c '. $(current_dir)/make-functions.sh && $@'
	
rm:
	bash -c '. $(current_dir)/make-functions.sh && $@'

run:
	bash -c '. $(current_dir)/make-functions.sh && $@'

run-one: 
	bash -c '. $(current_dir)/make-functions.sh && $@'


run-cwl:
	ls 
	cwltool $(WORKFLOW).cwl 

run-reana:
	reana-client   -lDEBUG   create  -f reana.yaml --name $(WORKFLOW)
	reana-client   -lDEBUG   start --workflow $(WORKFLOW)

build-singularity:
	bash -c '. $(current_dir)/make-functions.sh && $@'

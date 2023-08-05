#!/bin/bash

if [ ${DEBUG:-no} == "yes" ]; then
    set -x
fi

exec 2> >(awk '{print "\033[90m", strftime("%Y-%m-%dT%H:%M:%S"), "\033[31m", $0, "\033[0m"}')
exec > >(awk '{print "\033[90m", strftime("%Y-%m-%dT%H:%M:%S"), "\033[0m", $0}')

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo -e "\033[32mfound ci-template-cc location in $DIR\033[0m"

pip install --upgrade pyyaml --user || pip install --upgrade pyyaml \
    || { echo -e "\033[31missue updating python module of pyyaml from $DIR!\033[0m"; exit 1; }

oda-cc version -c $DIR || {
    pip install --upgrade ${DIR} --user || pip install --upgrade ${DIR} \
        || { echo -e "\033[31missue updating python module for ci-tempalte-cc from $DIR!\033[0m"; exit 1; }
}

if oda-cc get uri_base unset; then
    echo "found operable oda-cc from ci-template-cc"
else
    echo "NOT found operable oda-cc from ci-template-cc"
    exit 1
fi

SOURCE_NAME=$( oda-cc get metadata.source_short_name unnamed )
CC_BASE_IMAGE=$( oda-cc get cc_base_image integralsw/osa-python:11.1-3-g87cee807-20200410-144247-refcat-43.0-heasoft-6.27.2-python-3.8.2 )
ROOT_NB=$( oda-cc get root_notebook verify.ipynb )

PORT=8998

DOCKER_REGISTRY=admin.reproducible.online



#mkfile_path = $(abspath $(lastword $(MAKEFILE_LIST)))
#current_dir = $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
#current_version := $(shell cd $(current_dir); git describe --tags)

PIP="python -m pip"

echo "selected pip: $PIP"

REQ_NB2W=$(< requirements.txt grep nb2workflow | tee req_nb2w.txt)

if [ "$REQ_NB2W"x == ""x ]; then
    nb2workflow-version > req_nb2w.txt
    REQ_NB2W=$(cat req_nb2w.txt)
fi

$PIP freeze | grep nb2w | grep $(cat req_nb2w.txt) || $PIP install -r req_nb2w.txt

NB2WORKFLOW_VERSION=$(nb2workflow-version)
    
IMAGE="$DOCKER_REGISTRY/cc-$SOURCE_NAME:$( git describe --always --tags)-$NB2WORKFLOW_VERSION"

SINGULARITY_IMAGE=${IMAGE//\//}

echo "req_nb2w: $REQ_NB2W"
echo "image: $IMAGE"

function pull() {
    echo $NB2WORKFLOW_VERSION
    docker pull $IMAGE || true
    touch job.cwl
}

function build() {
    touch pip.conf
    docker pull $IMAGE || ( nb2worker ./ --build --tag-image $IMAGE --job --from ${CC_BASE_IMAGE:?} --docker-run-prefix="mkdir -pv /home/oda; export HOME_OVERRRIDE=/home/oda; source /init.sh; " --docker-command='id; export HOME_OVERRRIDE=/tmp; mkdir -pv $HOME_OVERRRIDE; source /init.sh; source /etc/bashrc; nbrun /repo/'$SOURCE_NAME'.ipynb $@'; ls -ltr *cwl; ) 
    touch job.cwl
}


function push() {
    docker push $IMAGE
}

function clean() {
    for nb in *ipynb; do 
            jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace $nb; 
        done
}

function rm() {
    docker rm -f $SOURCE_NAME || true
}


function ensure_minio() {
    if [ -z $MINIO_UPLOAD_KEY ]; then
        echo -e "\033[31mWARNING, MINIO_UPLOAD_KEY not set\033[0m"
        if [ ${LOCAL_ONLY:-no} == "yes" ]; then
            echo -e "\033[33mWARNING, LOCAL_ONLY=\"${LOCAL_ONLY}\", so MINIO_UPLOAD_KEY not set is allowed\033[0m"
        else
            echo -e "\033[31mERROR, LOCAL_ONLY=\"${LOCAL_ONLY}\" not \"yes\", but MINIO_UPLOAD_KEY not set - exiting\033[0m"
            exit 1
        fi
    fi
}

function run() {
  # this will listen with a notebook
  
    echo -e "\e[34mMounting\e[0m $PWD will be mounted in to use the code, and jupyter workdir "

    if [ ${MOUNT_SSH_FLAG:=no} == "yes" ]; then
        extra="-v /${HOME:?HOME variable is not set?}/.ssh:/home/oda/.ssh:ro"
        echo -e "\033[32mYES mounting ssh keys\033[0m: will rely on ssh when possible"
    else
        echo -e "\033[31mNOT mounting ssh keys\033[0m: will rely on https, please be sure sources are synchronous"
    fi


    docker rm -f $SOURCE_NAME || true
    docker run --entrypoint cat $IMAGE  /etc/passwd > passwd
    < passwd sed 's/1000/'$(id -u)'/' > passwd.new

    [ -s passwd.new ] || exit 1

    mkdir -pv /tmp/tmpcode-$SOURCE_NAME; \
        docker run --rm -it \
                --user $(id -u) \
		-e ODA_SPARQL_ROOT \
                -p $PORT:$PORT \
                -v $PWD/passwd.new:/etc/passwd \
                -v $PWD:/repo \
                -v $PWD:/home/jovyan \
                -v $PWD:/home/integral \
                -e JENA_PASSWORD \
                -e MINIO_UPLOAD_KEY \
                --name $SOURCE_NAME \
                --entrypoint  bash $IMAGE \
                $extra \
                -c "export ODA_SPARQL_ROOT=http://fuseki.internal.odahub.io/dataanalysis
                    export HOME_OVERRRIDE=/home/jovyan
                    export HOME=/home/jovyan
                    source /init.sh
                    echo $MINIO_UPLOAD_KEY > /tmp/home-run/.minio
                    chmod 400 /tmp/home-run/.minio
                    cd /repo
                    jupyter notebook --ip=0.0.0.0 --no-browser --port=$PORT"
}

# TODO: this logic should be within oda eval 
function run-one() {
        cname=cc-ci-run-$SOURCE_NAME-${RANDOM}

        ensure_minio

        docker run --entrypoint cat $IMAGE  /etc/passwd > passwd
        < passwd sed 's/1000/'$(id -u)'/' > passwd.new

        if [ ${MOUNT_SSH_FLAG:=no} == "yes" ]; then
            extra="-v /${HOME:?HOME variable is not set?}/.ssh:/home/oda/.ssh:ro"
            echo -e "\033[32mYES mounting ssh keys\033[0m: will rely on ssh when possible"
        else
            echo -e "\033[31mNOT mounting ssh keys\033[0m: will rely on https, please be sure sources are synchronous"
        fi

        echo -e "\033[33mnotebooks to run set by NB2RUN (defaults to root notebook $ROOT_NB) ${NB2RUN:=$ROOT_NB}\033[0m"
        export NB2RUN

        docker run \
            --name $cname \
            -e CI_JOB_TOKEN \
            -e MINIO_UPLOAD_KEY \
            -e JENA_PASSWORD \
            -e NBARGS_PYDICT \
            $extra \
                --entrypoint  bash $IMAGE \
                -c '''
                      mkdir -pv /tmp/output
                      export
                      export | grep CI_J
                      export | grep TOKE


                      mkdir -pv /tmp/home-run
                      chmod 700 /tmp/home-run
                      export HOME_OVERRRIDE=/tmp/home-run
                      
                      export ODA_SPARQL_ROOT=http://fuseki.internal.odahub.io/dataanalysis
                      
                      id -u
                      ls -lotra /tmp
                      source /init.sh

                      echo $MINIO_UPLOAD_KEY > /tmp/home-run/.minio
                      chmod 400 /tmp/home-run/.minio

                      if [ "'$MOUNT_SSH_FLAG'" == "yes" ]; then
                          if git clone git@gitlab.astro.unige.ch:integral/cc-workflows/cc-isgri-oda-nustar-reference.git /tmp/test-clone; then
                              echo -e "\033[32mSUCCESS\033[0mfully cloned private repo from gitlab";
                          else
                              echo -e "\033[31mFAILED033[0m to cloned private repo from gitlab";
                              echo "make sure that your home contains ssh keys"
                              exit 1
                          fi
                      else
                          echo "skipping ssh check: ssh will not be used"
                      fi

                      git clone /repo /tmp/home-run/repo
                      cd /tmp/home-run/repo

                      echo "${NBARGS_PYDICT:-{\}}" > nbargs.py
                      cat nbargs.py

                      export PYTHONUNBUFFERED=1

                      nb="'$NB2RUN'"
                      set -ex
                      python -c "import oda, yaml, ast, json;\
                                 md, d = oda.evaluate(
                                         \"kb\", 
                                         yaml.safe_load(open(\"oda.yaml\"))[\"uri_base\"], 
                                         nbname=\""${nb//.ipynb/}"\", 
                                         **ast.literal_eval(open(\"nbargs.py\").read()) or {}, 
                                         _write_files=True,
                                         _return_metadata=True,
                                     );\
                                 json.dump(d, open(\"cwl.output.json\", \"w\"));\
                                 json.dump(md, open(\"metadata.json\", \"w\"))
                                 " 2>&1  | cut -c1-400 | tee ${nb//.ipynb/_output.log}  
                      ls -l cwl.output.json
                      cp -fv cwl.output.json "${nb//.ipynb/_output.json}"
                      set +ex

                      ls -ltor

                      for jf in *json; do
                         filesize=$(stat -c%s "$jf")
                    
                         if (( filesize > 50001000 )); then
                             rm -fv $jf
                         fi
                      done

                      for outnb in *ipynb; do
                         nbreduce $outnb 3
                      done

                      cp *_output.* *.json /tmp/output
                      ls -ltor /tmp/output

                ''' || { echo -e "\033[31m workflow failed!\033[0m"; exit 1; }

        docker cp $cname:/tmp/output .
        docker rm -f $cname

        ls -ltr output

        cat output/metadata.json

        f=$NB2RUN

        fb=${f//.ipynb}


        set -ex
        nbinspect ${fb}.ipynb  > pars_default.json

        #nbinspect ${f}_output.ipynb  > pars.json
        echo "${NBARGS_PYDICT:-{\}}" > nbargs.py
        python -c 'import ast, json;\
                   json.dump(
                    { **json.load(open("pars_default.json")), 
                      **{ k: {"value": v} for
                          k, v in ast.literal_eval(open("nbargs.py").read()).items()} }, 
                    open("pars.json", "w")
                   )'

        echo -e "\033[33mpars.json:\033[0m"
        cat pars.json

        if [ "$fb" == ${ROOT_NB//.ipynb} ]; then
            nb_suffix=""
        else
            nb_suffix="-$fb"
        fi
        
        pars_suffix=$(oda-cc format '{pars[subcases_pattern][value]}_{pars[reference_instrument][value]}_{pars[nscw][value]}scw_sf{pars[systematic_fraction][value]}_{pars[osa_version][value]}')
        these_outputs=outputs$nb_suffix/$pars_suffix

        mkdir -pv $these_outputs
        mv -fv output/* $these_outputs
        cp -fv pars.json $these_outputs

        # this hierarically stacks them. But how is it used? unclear. please clarify what do you expect
 #       cp -rfv outputs $pars_suffix
}

function build-singularity() {
#       singularity -vvv create $(SINGULARITY_IMAGE) || true
        #docker save $(IMAGE_NAME) | singularity -vvv import $(SINGULARITY_IMAGE)

    docker run -v /var/run/docker.sock:/var/run/docker.sock -v /dev/shm/singularity/:/output --privileged -t --rm quay.io/singularity/docker2singularity $IMAGE
    mkdir -pv /data/singularity/$SOURCE_NAME
    mv -fv /dev/shm/singularity/* /data/singularity/$SOURCE_NAME/${SINGULARITY_IMAGE}
}

#run-cwl:
#    ls 
#    cwltool job.cwl --subcases_pattern="_1" --source_name="Her X-1" --osa_version='OSA11.0' --nscw=10 --ng_sig_limit=2. --systematic_fraction=0.01



# Common CI/CD routines re-used in [CC Workflows](https://gitlab.astro.unige.ch/integral/cc-workflows)

|  | |
| ------ | ------ |
| **See Also** | https://redmine.astro.unige.ch/projects/isgri-calibration/wiki/Common_ISGRI_Cross-Calibration_Workflows |

The workflows are mostly of INTEGRAL docker containers, which are [publicly available](https://hub.docker.com/orgs/integralsw). 

## Makefile:

Everybody likes to type "make". Also the make's target completing tracking is great and is a progenitor of similar techniques in other workflow mangment systems. But Makefile systax is another level of quoting hell, so all processes are actually described in [make-functions.sh](make-functions.sh)
In general, for every "make XXX" there is an "XXX" bash function in [make-functions.sh](make-functions.sh).

## make-functions.sh

### *build* 

build the container image, if needed. 

### *run-one*

runs all notebooks in a loop, using [oda evaluation](https://github.com/cdcihub/oda-kb).

needs access to [ODA KB](https://github.com/volodymyrss/oda-kb), uses the default ODA_SPARQL_ROOT=http://fuseki.internal.odahub.io/dataanalysis

benefits from access to ODA DataLake (minio) - not criticial hence TBD.

Workflow input parameters can be set as:

```bash
$ NBARGS_PYDICT='{"nscw":2}' make run-one
```

note taht NBARGS_PYDICT should be a valid python dictionary.

Use **nbinspect** to list notebook parameters.

### *run*

runs jupyter server, allowing to manually run and inspect the notebook. the notebook is mounted from the current directory hence can be later commited.

## Workflow Repository configuraion: oda.yaml

useful modifications for each workflow repository is contained in oda.yaml.

## image

integralsw/osa-python is the *base* docker image

## nb2workflow

[nb2workflow](https://github.com/volodymyrss/nb2workflow) adapts notebooks as workflows, either [CWL](https://www.commonwl.org/) jobs or [OpenAPI](https://swagger.io/specification/) services.

extract of some of the functions useful here:

- **nbrun** *[nbname]* runs notebook in a one-shot way. This can be done for test locally, and it is also done inside CWL container job (e.g. on REANA)

- **nbinspect** *[nbname]* shows notebook parameters

- **nb2service** runs a discoverable service that can execute the notebook on demand.
 
- **nb2worker** builds a container, either one-shot (for CWL) or service

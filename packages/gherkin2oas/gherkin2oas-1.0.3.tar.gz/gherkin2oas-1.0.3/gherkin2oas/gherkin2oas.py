from .utils import *
import json
import os
import traceback
from openapi_spec_validator import validate_spec
import subprocess
import os

def gherkin2oas(resources_folder=None, oas_title=None, oas_description=None, oas_security=None, oas_version=None, oas_host=None, oas_basepath=None, oas_schemes=None, oas_produces=None):
    for fname in os.listdir(resources_folder):
        if fname.endswith('.resource'):
            break
    else:
        raise RuntimeError("no .resource file found in {}".format(resources_folder))
    try:
        if not os.path.isdir(resources_folder + '/output_files'):
            os.makedirs(resources_folder + '/output_files')
        if not os.path.isdir(resources_folder + '/output_files/swagger-oas2'):
            os.makedirs(resources_folder + '/output_files/swagger-oas2')
        if not os.path.isdir(resources_folder + '/output_files/oas3'):
            os.makedirs(resources_folder + '/output_files/oas3')
    except:
        print(traceback.format_exc())
    resources = preprocessor.main(resources_folder)
    resource_names = nlp.plural_extend(resources)
    nlp_model = nlp.resource_analysis(resources,resource_names)
    model = nlp_model['model']
    resource_graph = nlp_model['resource_graph']
    state_graph = nlp_model['state_graph']
    oas_schema = formatter.generate_swagger(model, oas_security)
    oas_schema['swagger'] = '2.0'
    oas_schema['info'] = {  "title":            oas_title,
                            "description":      oas_description,
                            "version":          oas_version
    }
    oas_schema['host'] = oas_host
    oas_schema['schemes'] = oas_schemes 
    oas_schema['basePath'] = oas_basepath
    oas_schema['produces'] = oas_produces

    with open(resources_folder + '/output_files/swagger-oas2/swagger.json', 'w') as outfile:
        json.dump(oas_schema, outfile, indent=4)

    if os.name == 'nt':
        p = subprocess.Popen(["swagger2openapi.cmd", resources_folder + '/output_files/swagger-oas2/swagger.json', "-o", resources_folder + '/output_files/oas3/swagger.json'])
    else:
        p = subprocess.Popen(["swagger2openapi", resources_folder + '/output_files/swagger-oas2/swagger.json', "-o", resources_folder + '/output_files/oas3/swagger.json'])
    p.communicate()
    with open(resources_folder + '/output_files/oas3/swagger.json', 'r', encoding='utf-8') as inputfile:
        # spec = json.load(inputfile)
        # for oas_field in spec:
        #     i
        validate_spec(json.load(inputfile))
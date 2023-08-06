import json
import shutil
from os import scandir, remove
from os.path import join
import re
import yaml
from ddc.utils import stream_exec_cmd

REQUIRED_PH = 'Обязательно.'


def underscore_to_camelcase(s):
    return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)


def get_service_conf(api_workdir, service):
    conf_path = api_workdir + "/" + service + ".yaml"
    with open(conf_path, 'r') as f:
        return yaml.load(f.read())


def __build_docs(service_id, workdir, output_dir):
    print("Build docs...")
    api_workdir = join(workdir, "api")
    proto_path = join(api_workdir, "proto")

    versions = []
    for entry in scandir(proto_path):
        versions.append(entry.name)

    for version in versions:
        version_dir = join(proto_path, version)
        __build_swagger(service_id, version_dir, output_dir)
        exit(0)
        doc_content = get_gen_doc_content(join(version_dir, "doc_json.json"),
                                          service_id)
        swagger_file = service_id + ".swagger.json"
        output_file = join(output_dir, swagger_file)
        with (open(output_file, 'r'))as f:
            sw_str = f.read()
            sw_str = sw_str.replace('"' + version, '"')
            sw_str = sw_str.replace('#/definitions/' + version, '#/definitions/')
            swagger = json.loads(sw_str)
        swagger['info']['version'] = None
        swagger['info'].pop('version')

        # swagger['host'] = service + '.apis.devision.io'
        swagger['schemes'] = ["http"]

        swagger['schemes'] = None
        swagger['consumes'] = None
        swagger['produces'] = None
        swagger['tags'] = []
        for srv in doc_content['services']:
            swagger['tags'].append({
                "name": srv['name'],
                "description": srv['description'],
            })
        for defK, defV in swagger['definitions'].items():
            print(defK)

            required = []

            new_pros = {}
            for fK, fV in defV.get('properties', {}).items():
                title = fV.get('title')
                description = fV.get('description')

                if not title and not description:
                    raise ValueError("Нет комментария поля: " + str(fK))

                if not title and description:
                    parts = description.split("\n")
                    if parts:
                        title = parts[0]

                if REQUIRED_PH in title:
                    required.append(fK)
                    title = title.replace(REQUIRED_PH, '').strip()

                if not description:
                    fV['description'] = title
                if 'type' in fV and fV['type'] == 'array' \
                        and fV['items'].get('format') == 'int64':
                    fV['items']['type'] = 'number'

                camel_case_fk = underscore_to_camelcase(fK)
                new_pros[camel_case_fk] = fV
            defV['properties'] = new_pros
            defV['required'] = required
        with (open(output_file, 'w'))as f:
            f.write(json.dumps(swagger))
        print("file = %s" % str(output_file))
        # target = join(workdir, "docs", "content", "api",
        #               version + "_" + swagger_file)
        # shutil.move(file, target)


def get_gen_doc_content(doc_json, service):
    service__proto_ = service + ".proto"
    try:
        with (open(doc_json, 'r'))as f:
            con_ = json.loads(f.read())
            for f in con_['files']:
                if f['name'] == service__proto_:
                    return f
    finally:
        remove(doc_json)
    raise ValueError("В результатах генериации документации не найден файл: " + service__proto_)


def __build_swagger(service, version_dir, output_dir):
    stream_exec_cmd("""
        docker run --rm \
            -v {version_dir}:{version_dir} \
            -v {output_dir}:/tmp/grpc_docs \
            -w {version_dir} \
            znly/protoc:0.3.0 \
            -I. --swagger_out=logtostderr=true:. \
            --doc_out=/tmp/grpc_docs \
            --doc_opt=json,doc_json.json \
            {service}.proto
        """.format(
        version_dir=version_dir,
        output_dir=output_dir,
        service=service,
    ))


# docker run -v `pwd`:/defs namely/protoc-all:1.32_2 -d ./api/proto/v2 --lint -l go --with-validator --with-gateway -o api/out/swagger

def start_grpc_docs(cwd: str, output_dir: str, service_id: str):
    __build_docs(service_id, cwd, output_dir)
    # all_output = []
    # exit_code = -1
    # image_tag = None
    # try:
    #     if not docker_image_tag:
    #         exit_code, image_tag = __build_docker_image(all_output, cwd)
    #     else:
    #         image_tag = docker_image_tag
    #
    #     docker_args = [
    #         "-v {output_dir}:/tmp/ddc_build_mount".format(output_dir=output_dir),
    #     ]
    #
    #     all_output.append("Copy assets")
    #     exit_code, mix_output = stream_exec_cmd(
    #         "docker run --rm {docker_args} {image_tag} cp -R /usr/app_assets /tmp/ddc_build_mount".format(
    #             image_tag=image_tag, docker_args=" ".join(docker_args),
    #         )
    #     )
    #     all_output.append(mix_output)
    # except StopIteration:
    #     pass
    # finally:
    #     if not docker_image_tag and image_tag:
    #         stream_exec_cmd("docker image rm " + image_tag)
    #
    # return exit_code, "\n".join(all_output)


if __name__ == '__main__':
    start_grpc_docs("/Users/arturgspb/PycharmProjects/api-accountmanagement", "/Users/arturgspb/PycharmProjects/ddc/qwe", "accountmanagement")

# coding=utf-8
import requests
import sys
import json
import argparse

docker_server = "your-docker-server"


class dockerRegistry(object):
    def __init__(self):
        ver_check = self.__current()
        if ver_check["code"] == 200:
            self.ver = ver_check["version"]
        else:
            sys.exit(ver_check)

    def version(self):
        api_version_req = "/v2/"
        api_version = api_version_req.split("/")[1]
        api_check_url = docker_server + api_version_req
        response = requests.get(api_check_url, timeout=30)
        api_version_info = {}
        api_version_info["code"] = response.status_code
        api_version_info["version"] = api_version
        return api_version_info

    def __current(self):
        ver = self.version()
        code = ver["code"]
        info = {}
        if code == 200:
            info["code"] = code
            info["version"] = ver["version"]
        else:
            info["code"] = code
            info["errors"] = "Bad version"
            info["detail"] = "https://docs.docker.com/registry/spec/api/"
        return info

    def delimg(self, image, tag):
        headers = {
            "Accept": "application/vnd.docker.distribution.manifest.v2+json"
        }
        api_digest_req = "{host}/{ver}/{image}/manifests/{tag}".format(
            host=docker_server, ver=self.ver, image=image, tag=tag)
        res_diget = requests.get(api_digest_req, headers=headers)
        if res_diget.status_code == 200:
            digest = res_diget.headers["Docker-Content-Digest"]
            api_delete_req = "{host}/{ver}/{image}/manifests/{digest}".format(
                host=docker_server, ver=self.ver, image=image, digest=digest)
            res_del = requests.delete(api_delete_req, headers=headers)
            code = res_del.status_code
            status = res_del.headers["Content-Length"]
            if code == 202 and status == "0":
                return "[Image] {image} - Deleted".format(image=image)
            else:
                return "digest={}".format(digest)
        else:
            return "[Image] {image} - Not Found".format(image=image)

    def listimg(self):
        api_repos_req = "{host}/{ver}/_catalog".format(
            host=docker_server, ver=self.ver)
        req = requests.get(api_repos_req)
        reps = json.loads(req.text)["repositories"]
        return reps

    def listtag(self, image):
        api_tag_req = "{host}/{ver}/{image}/tags/list".format(
            host=docker_server, ver=self.ver, image=image)
        req = requests.get(api_tag_req)
        tags = json.loads(req.text)
        if tags.get("tags"):
            return tags
        else:
            return "[Image] {image} - Not Found".format(image=image)


def opt():
    parser = argparse.ArgumentParser("Docker API", argument_default="-h")
    parser.add_argument("--version", dest="ver",
                        action="store_true", default=False, help="API version")
    subparsers = parser.add_subparsers(help='commands')

    list_parser = subparsers.add_parser("list", help="List images")
    list_parser.add_argument("--all", dest="images", action="store_true", default=False, help="List all images")
    list_parser.add_argument("--image", dest="image", help="List tags for image")

    delete_parser = subparsers.add_parser("delete", help="Delete a image")
    delete_parser.add_argument("--image", dest="image", required=True)
    delete_parser.add_argument("--tag", dest="tag", required=True)
    return parser


def main():
    DR = dockerRegistry()
    arg = opt()
    paras = arg.parse_args()
    method = sys.argv
    ver = paras.ver
    if ver:
        ver = DR.version()
        print(ver)
    elif len(method) > 1 and method[1] == "list":
        images = paras.images
        image = paras.image
        if images:
            images = DR.listimg()
            print(images)
        elif image:
            tag = DR.listtag(image)
            print(tag)
        else:
            arg.print_help()
    elif len(method) > 1 and method[1] == "delete":
        image = paras.image
        tag = paras.tag
        dels = DR.delimg(image, tag)
        print(dels)
    else:
        arg.print_help()


if __name__ == "__main__":
    main()

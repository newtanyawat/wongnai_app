from flask import Blueprint
from ..service import controller

routes = Blueprint('/api/files', __name__)

routes.add_url_rule(
    'upload',
    'Upload',
    controller.upload,
    methods=["GET"]
)

routes.add_url_rule(
    'service_upload',
    'Service_upload',
    controller.service_upload,
    methods=["POST"]
)

routes.add_url_rule(
    'download/<uuid_name>',
    'Download',
    controller.download,
    methods=["GET"]
)

routes.add_url_rule(
    'service_download/<uuid_name>',
    'Service_download',
    controller.service_download,
    methods=["POST"]
)

routes.add_url_rule(
    'delete/<uuid_name>',
    'Delete',
    controller.delete,
    methods=["GET"]
)

routes.add_url_rule(
    'confirm_delete/<uuid_name>',
    'Confirm_delete',
    controller.confirm_delete,
    methods=["POST"]
)

routes.add_url_rule(
    'service_delete/<uuid_name>',
    'Service_delete_delete',
    controller.service_delete,
    methods=["POST"]
)

routes.add_url_rule(
    'list',
    'List',
    controller.list_files,
    methods=["GET"]
)
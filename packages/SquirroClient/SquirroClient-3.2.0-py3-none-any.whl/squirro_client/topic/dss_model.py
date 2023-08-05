import json
import logging

log = logging.getLogger(__name__)


class ExecutionError(Exception):
    """Error in executing a machine learning job"""

    pass


class DSSModels(object):

    #
    #  DSS Model
    #
    def get_dss_models(self, project_id):
        """Return all DSS Models for a project.

        :param project_id: Id of the Squirro project.
        """
        url = "%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dss_model" % {
            "ep": self.topic_api_url,
            "tenant": self.tenant,
            "project_id": project_id,
        }
        headers = {"Content-Type": "application/json"}
        res = self._perform_request("get", url, headers=headers)
        return self._process_response(res)["models"]

    def get_dss_model(self, project_id, model_id):
        """Return A single DSS Model.

        :param project_id: Id of the Squirro project.
        :param model_id: id of the DSS model
        """
        url = "%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dss_model/%(model_id)s" % {
            "ep": self.topic_api_url,
            "tenant": self.tenant,
            "project_id": project_id,
            "model_id": model_id,
        }

        headers = {"Content-Type": "application/json"}
        res = self._perform_request("get", url, headers=headers)
        return self._process_response(res)

    def new_dss_model(
        self,
        project_id,
        name,
        template_id,
        ground_truth_id,
        template_params=None,
        ground_truth_version=None,
        is_incomplete=False,
    ):
        """Create a new DSS Model.

        :param project_id: Id of the Squirro project.
        :param name: Name of the DSS Model.
        :param template_id: template do be used.
        :param template_params: parameters to initialize the template.
        :param ground_truth_id: id of the grountruth.
        :param ground_truth_version: version of the grountruth if any.
        :param is_incomplete: mark a model as incomplete.
        """

        url = "%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dss_model" % {
            "ep": self.topic_api_url,
            "tenant": self.tenant,
            "project_id": project_id,
        }
        headers = {"Content-Type": "application/json"}
        # TODO workaround to also allow incomplete models
        model_params = {
            "name": name,
            "template_id": template_id,
            "gt_id": ground_truth_id,
            "template_params": template_params,
            "ground_truth_version": ground_truth_version,
            "token": self.refresh_token,
            "is_incomplete": is_incomplete,
        }

        res = self._perform_request(
            "post", url, data=json.dumps(model_params), headers=headers
        )
        return self._process_response(res, [201])

    def modify_dss_model(
        self,
        project_id,
        model_id,
        name,
        template_id=None,
        template_params=None,
        ground_truth_id=None,
        ground_truth_version=None,
        is_incomplete=None,
    ):
        """Update DSS Model

        :param project_id: Id of the Squirro project.
        :param model_id: Id of the Machine Learning workflow.
        :param name: Name of the DSS Model.
        :param template_id: template do be used.
        :param template_params: parameters to initialize the template.
        :param ground_truth_id: id of the groundtruth.
        :param ground_truth_version: version of the groundtruth if any
        :param is_incomplete: mark a model as incomplete.
        """
        url = "%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dss_model/%(model_id)s" % {
            "ep": self.topic_api_url,
            "tenant": self.tenant,
            "project_id": project_id,
            "model_id": model_id,
        }
        headers = {"Content-Type": "application/json"}
        # TODO workaround to also allow incomplete models
        model_params = {
            "name": name,
            "template_id": template_id,
            "gt_id": ground_truth_id,
            "template_params": template_params,
            "ground_truth_version": ground_truth_version,
            "token": self.refresh_token,
            "is_incomplete": is_incomplete,
        }
        res = self._perform_request(
            "put", url, data=json.dumps(model_params), headers=headers
        )
        return self._process_response(res, [204])

    def delete_dss_model(self, project_id, model_id):
        """Delete DSS Model

        :param project_id: Id of the Squirro project.
        :param model_id: Id of the  DSS Model.
        """
        url = "%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dss_model/%(model_id)s" % {
            "ep": self.topic_api_url,
            "tenant": self.tenant,
            "project_id": project_id,
            "model_id": model_id,
        }

        headers = {"Content-Type": "application/json"}
        res = self._perform_request("delete", url, headers=headers)
        return self._process_response(res, [204])

import json
import logging

log = logging.getLogger(__name__)


class ExecutionError(Exception):
    """Error in executing a machine learning job"""

    pass


class DSSGroundTruthMixin(object):

    #
    #  DSS Groundtruth
    #
    def get_groundtruths(self, project_id):
        """Return all ground truth for a project in a list.

        :param project_id: Id of the Squirro project.
        """

        base_url = "{}/v0/{}/projects/{}/groundtruths"
        url = base_url.format(self.topic_api_url, self.tenant, project_id)

        headers = {"Content-Type": "application/json"}
        res = self._perform_request("get", url, headers=headers)
        return self._process_response(res)

    def get_groundtruth(self, project_id, groundtruth_id):
        """Get a single Ground Truth.

        :param project_id: Id of the Squirro project.
        :param groundtruth_id: Id of the GroundTruth
        """
        base_url = "{}/v0/{}/projects/{}/groundtruths/{}"
        headers = {"Content-Type": "application/json"}

        url = base_url.format(
            self.topic_api_url, self.tenant, project_id, groundtruth_id
        )
        res = self._perform_request("get", url, headers=headers)
        return self._process_response(res)

    def new_groundtruth(self, project_id, name, config):
        """Create a new Ground Truth.

        :param project_id: Id of the Squirro project.
        :param name: Name of the Ground Truth.
        :param config: Ground Truth Config.

        """

        base_url = "{}/v0/{}/projects/{}/groundtruths"
        headers = {"Content-Type": "application/json"}

        url = base_url.format(self.topic_api_url, self.tenant, project_id)

        groundtruth_params = {"name": name, "config": config}

        res = self._perform_request(
            "post", url, data=json.dumps(groundtruth_params), headers=headers
        )
        return self._process_response(res, [201])

    def modify_groundtruth(self, project_id, groundtruth_id, name=None, config=None):
        """Modify an existing Ground Truth.

        :param project_id: Id of the Squirro project.
        :param groundtruth_id: Id of the Ground Truth.
        :param name: Name of the Ground Truth.
        :param config: Dictionary of Ground Truth config.
        """
        url = "{}/v0/{}/projects/{}/groundtruths/{}"
        headers = {"Content-Type": "application/json"}

        groundtruth_update = {}

        if name is not None:
            groundtruth_update["name"] = name
        if config is not None:
            groundtruth_update["config"] = config

        url = url.format(self.topic_api_url, self.tenant, project_id, groundtruth_id)
        res = self._perform_request(
            "put", url, data=json.dumps(groundtruth_update), headers=headers
        )
        return self._process_response(res, [204])

    def delete_groundtruth(self, project_id, groundtruth_id):
        """Delete Ground Truth

        :param project_id: Id of the Squirro project.
        :param groundtruth_id: Id of the Ground Truth.
        """
        url = "{}/v0/{}/projects/{}/groundtruths/{}"
        headers = {"Content-Type": "application/json"}

        url = url.format(self.topic_api_url, self.tenant, project_id, groundtruth_id)
        res = self._perform_request("delete", url, headers=headers)
        return self._process_response(res, [204])

    #
    #  DSS Ground Truth Label
    #
    def get_groundtruth_labels(
        self,
        project_id,
        groundtruth_id,
        temporal_version=None,
        label=None,
        extract_query=None,
        item_id=None,
    ):
        """Return the labeled extract of a ground truth for a project in a list.

        :param project_id: Id of the Squirro project.
        :param groundtruth_id: Id of the GroundTruth
        :param temporal_version: temporal version of the Ground Truth
        :param label: label to filter Ground Truth by
        :param: item_id: item_id to filter Ground Truth by
        """
        base_url = "{}/v0/{}/projects/{}/groundtruths/{}/labels"
        headers = {"Content-Type": "application/json"}
        data = {
            "temporal_version": temporal_version,
            "label": label,
            "extract_query": extract_query,
            "item_id": item_id,
        }
        print(data)
        url = base_url.format(
            self.topic_api_url, self.tenant, project_id, groundtruth_id
        )
        res = self._perform_request("get", url, headers=headers, params=data)
        return self._process_response(res)

    def get_groundtruth_label(self, project_id, groundtruth_id, label_id):
        """Get a single labeled extract from a Ground Truth.

        :param project_id: Id of the Squirro project.
        :param groundtruth_id: Id of the GroundTruth
        :param label_id: Id of the labeled extract
        """
        base_url = "{}/v0/{}/projects/{}/groundtruths/{}/label/{}/"
        headers = {"Content-Type": "application/json"}

        url = base_url.format(
            self.topic_api_url, self.tenant, project_id, groundtruth_id, label_id
        )
        res = self._perform_request("get", url, headers=headers)
        return self._process_response(res)

    def new_groundtruth_label(self, project_id, groundtruth_id, label):
        """Create a new labeled extract.

        :param project_id: Id of the Squirro project.
        :param groundtruth_id: Id of the Ground Truth
        :param label: information of the labeled extract.

        """

        base_url = "{}/v0/{}/projects/{}/groundtruths/{}/labels"
        headers = {"Content-Type": "application/json"}

        url = base_url.format(
            self.topic_api_url, self.tenant, project_id, groundtruth_id
        )

        label_params = {"label": label}

        # Inject token
        # ml_workflow['squirro_token'] = self.refresh_token

        res = self._perform_request(
            "post", url, data=json.dumps(label_params), headers=headers
        )
        return self._process_response(res, [201])

    def modify_groundtruth_label(
        self, project_id, groundtruth_id, label_id, validity, label=None
    ):
        """Modify an existing labeled extract.

        :param project_id: Id of the Squirro project
        :param groundtruth_id: Id of the Ground Truth
        :param label_id: Id of the labeled extract
        :param validity: validity of the labeled extract
        :param label: label of the labeled extract
        """
        base_url = "{}/v0/{}/projects/{}/groundtruths/{}/labels"
        headers = {"Content-Type": "application/json"}

        label_update = {"validity": validity, "label": label}

        url = "/".join([base_url, label_id])
        url = url.format(self.topic_api_url, self.tenant, project_id, groundtruth_id)
        res = self._perform_request(
            "put", url, data=json.dumps(label_update), headers=headers
        )
        return self._process_response(res, [201])

    def delete_groundtruth_label(self, project_id, groundtruth_id, label_id):
        """Delete labeled extract

        :param project_id: Id of the Squirro project.
        :param groundtruth_id: Id of the Ground Truth.
        :param label_id: Id of the labeled extract
        """
        base_url = "{}/v0/{}/projects/{}/groundtruths/{}/labels"
        headers = {"Content-Type": "application/json"}

        url = "/".join([base_url, label_id])
        url = url.format(self.topic_api_url, self.tenant, project_id, groundtruth_id)
        res = self._perform_request("delete", url, headers=headers)
        return self._process_response(res, [204])

    #
    #  DSS Ground Truth Rule
    #
    def get_groundtruth_rules(self, project_id, groundtruth_id):
        """Get all rules for the Ground Truth.

        :param project_id: Id of the Squirro project
        :param groundtruth_id: Id of the GroundTruth
        """
        base_url = "{}/v0/{}/projects/{}/groundtruths/{}/rules"
        headers = {"Content-Type": "application/json"}

        url = base_url.format(
            self.topic_api_url, self.tenant, project_id, groundtruth_id
        )
        res = self._perform_request("get", url, headers=headers)
        return self._process_response(res)

    def get_groundtruth_rule(self, project_id, groundtruth_id, rule_id):
        """Get a single rule of the Ground Truth.

        :param project_id: Id of the Squirro project.
        :param groundtruth_id: Id of the GroundTruth
        :param rule_id: Id of the rule
        """
        base_url = "{}/v0/{}/projects/{}/groundtruths/{}/rules/{}"
        headers = {"Content-Type": "application/json"}

        url = base_url.format(
            self.topic_api_url, self.tenant, project_id, groundtruth_id, rule_id
        )
        res = self._perform_request("get", url, headers=headers)
        return self._process_response(res)

    def new_groundtruth_rule(self, project_id, groundtruth_id, rule):
        """Create a new rule in Ground Truth.

        :param project_id: Id of the Squirro project.
        :param groundtruth_id: Id of the Ground Truth
        :param rule: information of the rule.

        """

        base_url = "{}/v0/{}/projects/{}/groundtruths/{}/rules"
        headers = {"Content-Type": "application/json"}

        url = base_url.format(
            self.topic_api_url, self.tenant, project_id, groundtruth_id
        )

        rule_params = {"rule": rule}

        res = self._perform_request(
            "post", url, data=json.dumps(rule_params), headers=headers
        )
        return self._process_response(res, [201])

    def modify_groundtruth_rule(self, project_id, groundtruth_id, rule_id, rule):
        """Modify an existing rule.

        :param project_id: Id of the Squirro project.
        :param groundtruth_id: Id of the Ground Truth.
        :param rule_id: Id of the rule
        :param rule: information of the rule.
        """
        base_url = "{}/v0/{}/projects/{}/groundtruths/{}/rules"
        headers = {"Content-Type": "application/json"}

        rule_update = {"rule": rule}

        url = "/".join([base_url, rule_id])
        url = url.format(self.topic_api_url, self.tenant, project_id, groundtruth_id)
        res = self._perform_request(
            "put", url, data=json.dumps(rule_update), headers=headers
        )
        return self._process_response(res, [204])

    def delete_groundtruth_rule(self, project_id, groundtruth_id, rule_id):
        """Delete rule

        :param project_id: Id of the Squirro project.
        :param groundtruth_id: Id of the Ground Truth.
        :param rule_id: Id of the rule
        """
        base_url = "{}/v0/{}/projects/{}/groundtruths/{}/rules"
        headers = {"Content-Type": "application/json"}

        url = "/".join([base_url, rule_id])
        url = url.format(self.topic_api_url, self.tenant, project_id, groundtruth_id)
        res = self._perform_request("delete", url, headers=headers)
        return self._process_response(res, [204])

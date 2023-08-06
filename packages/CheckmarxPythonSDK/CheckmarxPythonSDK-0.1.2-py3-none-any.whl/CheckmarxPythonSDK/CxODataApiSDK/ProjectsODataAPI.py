import requests

from ..config import config
from . import authHeaders
from ..compat import (OK, UNAUTHORIZED)


class ProjectsODataAPI(object):

    def __init__(self):
        self.retry = 0

    def top_n_projects_by_risk_score(self, number_of_projects):
        """
        Requested result: list the 5 Projects whose most recent scans yielded the highest Risk Score
        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$expand=LastScan&$orderby=LastScan/RiskScore%20desc&$top=5

        Args:
            number_of_projects (int):

        Returns:
            `list` of `dict`
            sample
            [
             {
             'Id': 5, 'Name': 'jvl_local', 'IsPublic': True, 'Description': '',
             'CreatedDate': '2020-11-01T15:14:27.907Z', 'OwnerId': 2,
             'OwningTeamId': '00000000-1111-1111-b111-989c9070eb11',
              'EngineConfigurationId': 1, 'IssueTrackingSettings': None,
              'SourcePath': '', 'SourceProviderCredentials': '',
              'ExcludedFiles': '', 'ExcludedFolders': '', 'OriginClientTypeId': 0, 'PresetId': 36,
              'LastScanId': 1000005, 'TotalProjectScanCount': 1, 'SchedulingExpression': None
              }
            ]
        """
        n_projects = None

        url = config.get("base_url") + ("/Cxwebinterface/odata/v1/Projects?$expand=LastScan&$orderby=LastScan"
                                        "/RiskScore%20desc&$top={n}").format(n=number_of_projects)

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            auth=authHeaders.basic_auth,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item_list = r.json().get('value')
            n_projects = [
                {
                    "Id": item.get("Id"),
                    "Name": item.get("Name"),
                    "IsPublic": item.get("IsPublic"),
                    "Description": item.get("Description"),
                    "CreatedDate": item.get("CreatedDate"),
                    "OwnerId": item.get("OwnerId"),
                    "OwningTeamId": item.get("OwningTeamId"),
                    "EngineConfigurationId": item.get("EngineConfigurationId"),
                    "IssueTrackingSettings": item.get("IssueTrackingSettings"),
                    "SourcePath": item.get("SourcePath"),
                    "SourceProviderCredentials": item.get("SourceProviderCredentials"),
                    "ExcludedFiles": item.get("ExcludedFiles"),
                    "ExcludedFolders": item.get("ExcludedFolders"),
                    "OriginClientTypeId": item.get("OriginClientTypeId"),
                    "PresetId": item.get("PresetId"),
                    "LastScanId": item.get("LastScanId"),
                    "TotalProjectScanCount": item.get("TotalProjectScanCount"),
                    "SchedulingExpression": item.get("SchedulingExpression"),
                } for item in item_list
            ]
        elif r.status_code == UNAUTHORIZED and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.top_n_projects_by_risk_score(number_of_projects)
        else:
            raise ValueError(r.text)

        self.retry = 0

        return n_projects

    def top_n_projects_by_last_scan_duration(self, number_of_projects):
        """
        Requested result: list the 5 Projects whose most recent scan had the longest duration
        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$expand=LastScan&$orderby=LastScan/ScanDuration%20desc&$top=5

        Args:
            number_of_projects (int):

        Returns:
             `list` of `dict`
        """
        n_projects = None

        url = config.get("base_url") + ("/Cxwebinterface/odata/v1/Projects?$expand=LastScan&$orderby=LastScan"
                                        "/ScanDuration%20desc&$top={n}").format(n=number_of_projects)

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            auth=authHeaders.basic_auth,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item_list = r.json().get('value')
            n_projects = [
                {
                    "Id": item.get("Id"),
                    "Name": item.get("Name"),
                    "IsPublic": item.get("IsPublic"),
                    "Description": item.get("Description"),
                    "CreatedDate": item.get("CreatedDate"),
                    "OwnerId": item.get("OwnerId"),
                    "OwningTeamId": item.get("OwningTeamId"),
                    "EngineConfigurationId": item.get("EngineConfigurationId"),
                    "IssueTrackingSettings": item.get("IssueTrackingSettings"),
                    "SourcePath": item.get("SourcePath"),
                    "SourceProviderCredentials": item.get("SourceProviderCredentials"),
                    "ExcludedFiles": item.get("ExcludedFiles"),
                    "ExcludedFolders": item.get("ExcludedFolders"),
                    "OriginClientTypeId": item.get("OriginClientTypeId"),
                    "PresetId": item.get("PresetId"),
                    "LastScanId": item.get("LastScanId"),
                    "TotalProjectScanCount": item.get("TotalProjectScanCount"),
                    "SchedulingExpression": item.get("SchedulingExpression"),
                } for item in item_list
            ]
        elif r.status_code == UNAUTHORIZED and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.top_n_projects_by_last_scan_duration(number_of_projects)
        else:
            raise ValueError(r.text)

        self.retry = 0

        return n_projects

    def all_projects_with_their_last_scan_and_the_high_vulnerabilities(self):
        """
        Requested result: list all projects, and for each project list the security issues (vulnerabilities) with
        a High severity degree found in the project's most recent scan.
        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$expand=LastScan
        ($expand=Results($filter=Severity%20eq%20CxDataRepository.Severity%27High%27))

        Returns:
            `list` of `dict`
        """
        n_projects = None

        url = config.get("base_url") + ("/Cxwebinterface/odata/v1/Projects?$expand=LastScan($expand=Results($filter="
                                        "Severity%20eq%20CxDataRepository.Severity%27High%27))")

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            auth=authHeaders.basic_auth,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item_list = r.json().get('value')
            n_projects = [
                {
                    "Id": item.get("Id"),
                    "Name": item.get("Name"),
                    "IsPublic": item.get("IsPublic"),
                    "Description": item.get("Description"),
                    "CreatedDate": item.get("CreatedDate"),
                    "OwnerId": item.get("OwnerId"),
                    "OwningTeamId": item.get("OwningTeamId"),
                    "EngineConfigurationId": item.get("EngineConfigurationId"),
                    "IssueTrackingSettings": item.get("IssueTrackingSettings"),
                    "SourcePath": item.get("SourcePath"),
                    "SourceProviderCredentials": item.get("SourceProviderCredentials"),
                    "ExcludedFiles": item.get("ExcludedFiles"),
                    "ExcludedFolders": item.get("ExcludedFolders"),
                    "OriginClientTypeId": item.get("OriginClientTypeId"),
                    "PresetId": item.get("PresetId"),
                    "LastScanId": item.get("LastScanId"),
                    "TotalProjectScanCount": item.get("TotalProjectScanCount"),
                    "SchedulingExpression": item.get("SchedulingExpression"),
                    "LastScan": item.get("LastScan")
                } for item in item_list
            ]
        elif r.status_code == UNAUTHORIZED and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.all_projects_with_their_last_scan_and_the_high_vulnerabilities()
        else:
            raise ValueError(r.text)

        self.retry = 0

        return n_projects

    def only_projects_that_have_high_vulnerabilities_in_the_last_scan(self):
        """
        Requested result:list only projects that had vulnerabilities with a High severity degree found
        in their last scan
        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$expand=LastScan($expand=Results)&
        $filter=LastScan/Results/any(r:%20r/Severity%20eq%20CxDataRepository.Severity%27High%27)

        Returns:

        """
        pass

    def for_all_projects_in_a_team_return_the_number_of_issues_vulnerabilities_within_a_predefined_time_range(self):
        """
        Requested result:list the number of recurrent/resolved/new issues (vulnerabilities) detected by scans made in
        all projects that were carried out in a team within a predefined time range. The sample query below refers to
        a time range between the 23/07/2015 and 23/08/2015.

        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?
        $filter=OwningTeamId%20eq%20%2700000000-1111-1111-b111-989c9070eb11%27&
        $expand=Scans($expand=ResultSummary;$select=Id,ScanRequestedOn,ResultSummary;
        $filter=ScanRequestedOn%20gt%202015-07-23%20and%20ScanRequestedOn%20lt%202015-08-23)
        Returns:

        """
        pass

    def retrieve_a_count_of_the_projects_in_the_system(self):
        """
        Query used for retrieving the data: http://localhost/Cxwebinterface/odata/v1/Projects/$count
        Returns:

        """

    def retrieve_all_projects_with_a_custom_field_that_has_a_specific_value(self):
        """
        Requested result: retrieve all projects that contain a custom filed (for example, ProjManager, indicating the
        project manager's name) with a specific value (for example, Joe).

        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$filter=CustomFields/any
        (f: f/FieldName eq 'ProjManager' and f/FieldValue eq 'Joe')

        Returns:

        """

    def retrieve_all_projects_with_a_custom_field_as_well_as_the_custom_field_information(self):
        """
        Requested result: retrieve all projects that contain a custom field (for example, ProjManager, indicating the
        project manager's name), as well as the custom field's information.

        Query used for retrieving the data:
        http://localhost/cxwebinterface/odata/v1/Projects?$expand=CustomFields&$filter=CustomFields/any
        (f: f/FieldName eq 'Field1')

        Returns:

        """

    def retrieve_a_list_of_presets_associated_with_each_project(self):
        """
        Requested result: retrieves a list of presets associated with each project

        Query used for retrieving the data: http://localhost/Cxwebinterface/odata/v1/Projects?$expand=Preset

        Returns:

        """

    def retrieve_all_projects_that_are_set_up_with_a_non_standard_configuration(self):
        """
        Requested result: retrieve all projects that are set up with a non-standard configuration,
        such as “Multi-Lanaguage Scan (v8.4.2 and up)".

        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$filter=EngineConfigurationId
        or http://localhost/Cxwebinterface/odata/v1/Projects?$filter=EngineConfigurationId%20gt%201

        Returns:

        """

    def get_all_projects_id_name(self):
        """

        Returns:
            `list` of int
        """
        project_id_name_list = []

        url = config.get("base_url") + "/Cxwebinterface/odata/v1/Projects?$select=Id,Name"

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            auth=authHeaders.basic_auth,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item_list = r.json().get('value')
            project_id_name_list = [
                {
                    "ProjectId": item.get("Id"),
                    "ProjectName": item.get("Name")
                } for item in item_list
            ]
        elif r.status_code == UNAUTHORIZED and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_all_projects_id_name()
        else:
            raise ValueError(r.text)

        self.retry = 0

        return project_id_name_list

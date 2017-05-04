class CsvIngestionJob():
    @property
    def id(self):
        pass

    @property
    def csv_uri(self):
        pass

    @property
    def headers(self):
        pass


class CreateCsvIngestionJobRequest(object):
    def __init__(self, tenant_id, project_id, csv_uri, job_id):
        self._tenant_id = tenant_id
        self._project_id = project_id
        self._csv_uri = csv_uri
        self._job_id = job_id

    @property
    def job_id(self):
        return self._job_id

    @property
    def tenant_id(self):
        return self._tenant_id

    @property
    def project_id(self):
        return self._project_id

    @property
    def csv_uri(self):
        return self._csv_uri

    def to_dict(self):
        return dict(
            tenant_id=self.tenant_id,
            project_id=self.project_id,
            csv_uri=self.csv_uri,
            job_id=self.job_id
        )

    @classmethod
    def from_dict(cls, raw_dict):
        return cls(
            raw_dict.get('tenant_id'),
            raw_dict.get('project_id'),
            raw_dict.get('csv_uri'),
            raw_dict.get('job_id')
        )

    def __str__(self):
        return ("CreateCsvIngestionJobRequest( tenant_id={tenant_id}, project_id={project_id}, "
                "csv_uri={csv_uri}, job_id={job_id})").format(
            **self.to_dict())

    def __repr__(self):
        return self.__str__()


def new_job(new_ingestion_request):
    return CsvIngestionJob()

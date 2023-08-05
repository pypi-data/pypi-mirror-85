"""Mongo data models."""

from mongoengine.fields import (Document, StringField, DateTimeField,
                                ListField, IntField, EmbeddedDocument,
                                EmbeddedDocumentListField, BooleanField,
                                DictField, FloatField, EmbeddedDocumentField)


class RepoEvents(Document):
    """The repository events collection model.

    Attributes:
        event_type (StringField): The GitHub event type https://developer.github.com/v3/activity/event_types
        organization (StringField): The organization name of the GitHub repo.
        repository (StringField): The name of the GitHub repo.
        timestamp (DateTimeField): The datetime timestamp of the event.
    """

    meta = {'allow_inheritance': True}

    # Static list of valid event types
    valid_event_types = ("ReleaseEvent", "CommitEvent", "PullEvent")

    # Crawler fields
    event_type = StringField(required=True, choices=valid_event_types)
    organization = StringField(required=True)
    repository = StringField(required=True)
    timestamp = DateTimeField(required=True)

class LinterScanEvent(EmbeddedDocument):
    """A sub-document for static analysis events.

    Attributes:
        linter_name (StringField): The name of the linter that ran against the file.
        file_path (StringField): The full path of the file in the repo.
        errors_total (IntField): Total number of errors.
        warnings_total (IntField): Total number of warnings.
        linter_output (StringField): Full output from the linter.
    """
    linter_name = StringField()
    file_path = StringField()
    errors_total = IntField()
    warnings_total = IntField()
    linter_output = StringField()

    def __init__(self, **kwargs):
        """Pass any init parameters to the Document class."""
        EmbeddedDocument.__init__(self, **kwargs)


class ReleaseEvent(RepoEvents):
    """The GitHub release events model."""
    def __init__(self, **kwargs):
        RepoEvents.__init__(self, **kwargs)
        self.event_type = "ReleaseEvent"


class PullEvent(RepoEvents):
    """The GitHub pull requests events model."""

    sha = StringField(required=True)
    ref = StringField(required=True, null=True)

    merged = BooleanField(required=True)
    commits = IntField(required=True)
    additions = IntField(required=True)
    deletions = IntField(required=True)
    changed_files = IntField(required=True)

    def __init__(self, **kwargs):
        RepoEvents.__init__(self, **kwargs)
        self.event_type = "PullEvent"

class MaturityKPI(EmbeddedDocument):
    """The maturity KPI total and sub-totals."""

    total = FloatField(default=0.0)
    assets = FloatField(default=0.0)
    tooling = FloatField(default=0.0)
    automation = FloatField(default=0.0)
    security = FloatField(default=0.0)

    def __init__(self, load_dict=None, **kwargs):
        EmbeddedDocument.__init__(self, **kwargs)
        self.load(load_dict)

    def load(self, load_dict):
        if load_dict:
            self.total = load_dict["total"]
            self.assets = load_dict["assets"]
            self.tooling = load_dict["tooling"]
            self.automation = load_dict["automation"]
            self.security = load_dict["security"]


class QualityKPI(EmbeddedDocument):
    """The quality KPI total and sub-totals."""

    total = FloatField(default=0.0)
    pipeline = FloatField(default=0.0)
    testing = FloatField(default=0.0)
    static_analyis = FloatField(default=0.0)
    deploy = FloatField(default=0.0)

    def __init__(self, load_dict=None, **kwargs):
        EmbeddedDocument.__init__(self, **kwargs)
        self.load(load_dict)

    def load(self, load_dict):
        if load_dict:
            self.total = load_dict["total"]
            self.pipeline = load_dict["pipeline"]
            self.testing = load_dict["testing"]
            self.static_analysis = load_dict["static_analysis"]
            self.deploy = load_dict["deploy"]


class RiskKPI(EmbeddedDocument):
    """The risk KPI total and sub-totals."""

    total = FloatField(default=0.0)
    secrets = FloatField(default=0.0)
    auth = FloatField(default=0.0)
    keys = FloatField(default=0.0)
    compliance = FloatField(default=0.0)
    code_warnings = FloatField(default=0.0)
    code_errors = FloatField(default=0.0)
    devops_warnings = FloatField(default=0.0)
    devops_errors = FloatField(default=0.0)


    def __init__(self, load_dict=None, **kwargs):
        EmbeddedDocument.__init__(self, **kwargs)
        self.load(load_dict)

    def load(self, load_dict):
        if load_dict:
            self.total = load_dict["total"]
            self.secrets = load_dict["secrets"]
            self.auth = load_dict["auth"]
            self.keys = load_dict["keys"]
            self.compliance = load_dict["compliance"]

class InfrastructureKPI(EmbeddedDocument):
    """The infrastructure KPI total and sub-totals."""

    total = FloatField(default=0.0)
    tags = FloatField(default=0.0)
    networking = FloatField(default=0.0)
    compute_resources = FloatField(default=0.0)
    environments = FloatField(default=0.0)

    def __init__(self, load_dict=None, **kwargs):
        EmbeddedDocument.__init__(self, **kwargs)
        self.load(load_dict)

    def load(self, load_dict):
        if load_dict:
            self.total = load_dict["total"]
            self.tags = load_dict["tags"]
            self.networking = load_dict["networking"]
            self.compute_resources = load_dict["compute_resources"]
            self.environments = load_dict["environments"]

class VelocityKPI(EmbeddedDocument):
    """The velocity KPI total and sub-totals."""

    pr_size = FloatField(default=0.0)
    pr_duration = FloatField(default=0.0)
    pr_commit_count = FloatField(default=0.0)
    commit_freq = FloatField(default=0.0)
    actors = ListField()
    comment_percent = FloatField()
    space_percent = FloatField()


class InvestmentKPI(EmbeddedDocument):
    """The investment KPI total and sub-totals."""

    total = FloatField(default=0.0)
    features = FloatField(default=0.0)
    defects = FloatField(default=0.0)
    devops = FloatField(default=0.0)
    debt = FloatField(default=0.0)

    def __init__(self, load_dict=None, **kwargs):
        EmbeddedDocument.__init__(self, **kwargs)
        self.load(load_dict)

    def load(self, load_dict):
        if load_dict:
            self.total = load_dict["total"]
            self.features = load_dict["features"]
            self.defects = load_dict["defects"]
            self.devops = load_dict["devops"]
            self.debt = load_dict["debt"]

class CommitEvent(RepoEvents):
    """The GitHub commit events model.

    Attributes:
        sha (StringField): The SHA of the most recent commit on ref after the push.
        ref (StringField): The full git ref that was pushed. Example: refs/heads/master.
        content_flags (ListField, optional): Flags that matched the file content rules.
        filename_flags (ListField, optional): Flags that matched the filename rules.
        LinterScanEvents (Document): A sub-document for static analysis events.
    """

    # Commit fields
    sha = StringField(required=True)
    additions = IntField(default=0)
    deletions = IntField(default=0)
    total = IntField(default=0)
    commit_files = ListField()

    # Category and Tokens
    category =  DictField()
    file_count = DictField()
    #tokens = DictField()
    #files = ListField()

    # Linter fields
    linter_events = EmbeddedDocumentListField(LinterScanEvent)

    # Analysis fields
    investment_kpi = EmbeddedDocumentField(InvestmentKPI)
    maturity_kpi = EmbeddedDocumentField(MaturityKPI)
    quality_kpi = EmbeddedDocumentField(QualityKPI)
    risk_kpi = EmbeddedDocumentField(RiskKPI)
    velocity_kpi = EmbeddedDocumentField(VelocityKPI)
    infra_kpi = EmbeddedDocumentField(InfrastructureKPI)


class PipelineRun(Document):
    name = StringField(max_length=120, required=True)
    number = IntField()
    repo = StringField(max_length=200)
    branch = StringField(max_length=50)
    sha = StringField(max_length=50)
    commit_id = StringField(max_length=50)

    build_files = ListField(StringField(max_length=128))
    file_count = IntField()

    buildnumber = IntField(required=True)
    building = BooleanField(required=True)
    duration_millis = IntField()
    result = StringField(max_length=50)
    timestamp = DateTimeField()
    url = StringField(max_length=256)

    fail_stage = StringField(max_length=50)
    fail_logs = StringField(max_length=10000)

class Group(Document):
    name = StringField(max_length=120, primary_key=True, required=True)
    children = ListField(StringField(max_length=120))

class Set(Document):
    name = StringField(max_length=120, primary_key=True, required=True)
    children = ListField(StringField(max_length=120))

class JiraIssue(Document):
    issue_id            = StringField()
    issue_key           = StringField(primary_key=True, required=True)
    issuetype_name      = StringField()
    parent_issue_key    = StringField()
    parent_issue_id     = StringField()
    project_id          = StringField()
    project_key         = StringField()
    project_name        = StringField()
    resolution_name     = StringField()
    resolution_date     = DateTimeField()
    created             = DateTimeField()
    priority_name       = StringField()
    priority_id         = StringField()
    status_name         = StringField()
    assignee_key        = StringField()
    story_points        = FloatField()
    labels              = ListField(StringField())
    updated             = DateTimeField()
    work_begin_date     = DateTimeField()
    work_completed_date = DateTimeField()

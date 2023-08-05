# topograph-library

## Mongoengine Models

### Usage

```bash
pip install topo-library
```

```python
from datetime import datetime
from topolibrary.model import PushEvent, LinterScanEvent

repo_event = PushEvent()
repo_event.repo_name = "TestRepo"
repo_event.timestamp = datetime.utcnow()
repo_data.sha = "sha3429940u9480928342934"
repo_data.ref = "stelligent/asdfasdfasdf"

scan_event = LinterScanEvent()
scan_event.linter_name = "cfn_nage"
scan_event.file_path = "TestRepo/cfn.yaml"
scan_event.errors_total = 6
scan_event.warnings_total = 10
scan_event.linter_output = "Output from linter"

repo_event.linter_warnings_total = 20
repo_event.linter_errors_total = 30
repo_event.linter_events.append(scan_event)

PushEvent.save(repo_event)
```

### Available Documents
* RepoEvents
* PushEvent
* ReleaseEvent
* PullRequestEvent
* LinterScanEvent (Embedded Document)

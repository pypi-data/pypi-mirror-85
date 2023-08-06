"""Test configuration for the Matchlight SDK."""
import time
import uuid

import pytest

import matchlight


@pytest.fixture
def access_key():
    """Provides a fake access key in the form of a UUID4."""
    return uuid.uuid4().hex


@pytest.fixture
def secret_key():
    """Provides a fake secret key in the form of a UUID4."""
    return uuid.uuid4().hex


@pytest.fixture
def connection(access_key, secret_key):
    """A connection object initialized with a fake access and secret key."""
    return matchlight.Matchlight(access_key=access_key, secret_key=secret_key)


@pytest.fixture(scope='function')
def id():
    """Provides a fake id in the form of a UUID4."""
    return str(uuid.uuid4())


@pytest.fixture(scope='function')
def number_of_records():
    """A record count fixture."""
    return 10


@pytest.fixture(scope='function')
def number_of_unseen_alerts():
    """An unseen alerts count fixture."""
    return 10


@pytest.fixture(scope='function')
def document(request):
    """A document mapping fixture."""
    return {
        'id': uuid.uuid4().hex,
        'name': 'Document record',
        'description': '',
        'ctime': time.time(),
        'mtime': time.time(),
        'metadata': {},
    }


@pytest.fixture(scope='function')
def document_record(document):
    """A document record fixture."""
    return matchlight.Record(**document)


@pytest.fixture(scope='function')
def project_name():
    """A project name fixture."""
    return 'Test Project'


@pytest.fixture(scope='function', params=[
    'bulk_pii',
    'document',
    'pii',
    'source_code',
])
def project_type(request):
    """A parametrized project type fixture."""
    return request.param


@pytest.fixture(scope='function')
def upload_token():
    """An upload token (dash-separated UUID4) fixture."""
    return str(uuid.uuid4())


@pytest.fixture(scope='function')
def project_payload(project_name, project_type, upload_token,
                    number_of_records, number_of_unseen_alerts):
    """A project payload artifact, parametrized by project type."""
    return {
        'project_name': project_name,
        'project_type': project_type,
        'project_upload_token': upload_token,
        'last_date_modified': time.time(),
        'number_of_records': number_of_records,
        'number_of_unseen_alerts': number_of_unseen_alerts,
    }


@pytest.fixture
def project(project_payload):
    """A project instance fixture, parametrized by project type."""
    return matchlight.Project.from_mapping(project_payload)


@pytest.fixture(scope='function')
def alert_payload(id, upload_token):
    """An alert payload artifact."""
    return {
        'id': id,
        'alert_number': 10,
        'type': 'pii',
        'url': 'https://terbiumlabs.com/matchlight.html',
        'url_metadata': {
            'description': 'Matchlight provides intelligence on your most imp',
            'tor_only': 'false'
        },
        'ctime': time.time(),
        'mtime': time.time(),
        'seen': 'true',
        'archived': 'true',
        'upload_token': upload_token,
        'details': {
            'pii': {
                'fields': ['phone']
            }
        },
        'asset_name': 'Example Record',
        'project_name': 'Sample Project',
    }


@pytest.fixture(scope='function')
def alert_details_pii_payload():
    """An alert details payload artifact for a pii alert."""
    return {
        'details': {
            'pii': [
                {
                    'email': 'o****@gmail.com',
                    'first': 'a****',
                    'last': 'b****',
                    'record_id': 'd3c59d38c4054f62876a2a7a3dca41ca'
                }
            ]
        },
        'notes': '',
        'type': 'pii'
    }


@pytest.fixture
def alert(alert_payload):
    """An alert instance fixture."""
    return matchlight.Alert.from_mapping(alert_payload)


@pytest.fixture(scope='function')
def pii_search_email_only_results():
    """PII search results for only the email field."""
    return [
        {
            'fields': ['email'],
            'ts': '2018-07-25T20:00:44',
            'source': 'Exactis Breach June 2018'
        },
        {
            'fields': ['email'],
            'ts': '2017-01-25T02:35:04',
            'source': 'https://pastebin.com/raw.php?i=1DgbtSZc'
        },
        {
            'fields': ['email'],
            'ts': 1556221970,
            'source': 'Zoosk Breach Nov 2016'
        },
        {
            'fields': ['email'],
            'ts': '1558333205',
            'source': 'https://www.reddit.com/r/AskReddit/comments/3oqj4a'
        },
    ]


@pytest.fixture(scope='function')
def search_email_only_results():
    """PII search results for only the email field."""
    return [
        {
            'cwid': 'fff33cbe7ed54f5ebfccd09c3d24999c',
            'score': 800,
            'ts': 1453298293,
            'urls': [
                [
                    1453298293,
                    (
                        'http://blockchainbdgpzk.onion/tx/4f4097992b89156'
                        '690817556fc3f540535bdfadde06661c9cae21d500943f970'
                    )
                ]
            ]
        },
        {
            'cwid': 'ffedf0a2b775cfd50383603ff827d702',
            'score': 400,
            'ts': 1438870917,
            'urls': [
                [
                    1438870917,
                    (
                        'http://nqigfqrxnkwcqmiq.onion/'
                        'wiki/index.php#Whistleblowing'
                    )
                ]
            ]
        },
    ]

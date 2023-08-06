"""Unit tests the record methods of the Matchlight SDK."""
from __future__ import unicode_literals

import io
import json
import random
import string
import time
import uuid

import pytest
import responses

import matchlight


DOCUMENT_RECORD_PATH = 'tests/fixtures/UTF-8-test.txt'
PII_RECORDS_RAW_PATH = 'tests/fixtures/pii_records_raw.json'


# fake = faker.Factory.create()


# See <https://github.com/pytest-dev/pytest-factoryboy/issues/29>
# class PiiRecord(object):
#
#     def __init__(self, email, first_name, middle_name, last_name,
#                  ssn, address, city, state, zipcode, phone):
#         self.email = email
#         self.first_name = first_name
#         self.middle_name = middle_name
#         self.last_name = last_name
#         self.ssn = ssn
#         self.address = address
#         self.city = city
#         self.state = state
#         self.zipcode = zipcode
#         self.phone = phone
#
#
# @pytest_factoryboy.register
# class PiiRecordFactory(factory.Factory):
#
#     class Meta:
#         model = PiiRecord
#
#     email = factory.LazyAttribute(lambda _: fake.email())
#     first_name = factory.LazyAttribute(lambda _: fake.first_name())
#     middle_name = factory.LazyAttribute(lambda _: fake.first_name())
#     last_name = factory.LazyAttribute(lambda _: fake.last_name())
#     ssn = factory.LazyAttribute(lambda _: fake.ssn())
#     address = factory.LazyAttribute(lambda _: fake.address())
#     city = factory.LazyAttribute(lambda _: fake.city())
#     state = factory.LazyAttribute(lambda _: fake.state())
#     zipcode = factory.LazyAttribute(lambda _: fake.zipcode())
#     phone = factory.LazyAttribute(lambda _: fake.phone_number())


@pytest.fixture(scope='function', params=[PII_RECORDS_RAW_PATH])
def pii_records_raw(request):
    """Sample PII records."""
    with io.open(request.param) as fp:
        return json.loads(fp.read())


def test_record_details(document):
    """Verifies that record details are returned correctly."""
    record = matchlight.Record(**document)
    assert record.details == document


def test_record_user_provided_id(document):
    """Verifies record user provided identifiers."""
    document['metadata']['user_record_id'] = 42
    record = matchlight.Record(**document)
    assert record.user_provided_id == document['metadata']['user_record_id']


def test_record_add_pii_missing_first_name_error(connection, project):
    """Test that add_pii throws an error for missing first_name argument."""
    missing_first_name_record_data = {
        'email': 'heather03@hotmail.com',
        'middle_name': '',
        'last_name': 'whatever',
        'ssn': '000-00-0000',
        'address': '25068 Treena Cliff',
        'city': 'Almediashire',
        'state': 'Georgia',
        'zipcode': 82360,
        'phone': '04962816540'
    }

    with pytest.raises(matchlight.error.SDKError) as err_info:
        connection.records.add_pii(
            project=project,
            description='',
            **missing_first_name_record_data
        )

    assert str(err_info.value) == (
        'Fingerprinter Failed: the first_name argument is required along with '
        'the last_name argument.'
    )


def test_record_add_pii_missing_last_name_error(connection, project):
    """Test that add_pii throws an error for missing last_name argument."""
    missing_last_name_record_data = {
        'email': 'heather03@hotmail.com',
        'first_name': 'Elby',
        'middle_name': '',
        'ssn': '000-00-0000',
        'address': '25068 Treena Cliff',
        'city': 'Almediashire',
        'state': 'Georgia',
        'zipcode': 82360,
        'phone': '04962816540'
    }

    with pytest.raises(matchlight.error.SDKError) as err_info:
        connection.records.add_pii(
            project=project,
            description='',
            **missing_last_name_record_data
        )

    assert str(err_info.value) == (
        'Fingerprinter Failed: the last_name argument is required along with '
        'the first_name argument.'
    )


@responses.activate
@pytest.mark.parametrize('min_score', [
    None,
    800,
])
def test_record_add_document_prototype(
        min_score, connection, project, document):
    """Verifies adding document records to a project."""
    with io.open(DOCUMENT_RECORD_PATH, 'rb') as f:
        content = f.readline()[0:840]

    responses.add(
        method=responses.POST,
        url='{}/records/upload/document/{}'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            project.upload_token
        ),
        json={
            'id': uuid.uuid4().hex,
            'name': 'name',
            'description': '',
            'ctime': time.time(),
            'mtime': time.time(),
            'metadata': '{}',
        },
        status=200
    )

    record = connection.records.add_document(
        project=project,
        name=document['name'],
        description=document['description'],
        content=content,
        user_record_id='12345',
        min_score=min_score)
    assert len(responses.calls) == 1

    record = connection.records.add_document(
        project=project,
        name=document['name'],
        description=document['description'],
        content=content,
        user_record_id=12345,
        min_score=min_score,
        offline=True)
    assert isinstance(record, dict)
    assert len(responses.calls) == 1

    # Test that a nice error is returned for too long input
    with pytest.raises(matchlight.error.SDKError) as err_info:
        connection.records.add_document(
            project=project,
            name=document['name'],
            description=document['description'],
            content=''.join(random.choice(
                string.ascii_uppercase + string.digits
            ) for _ in range(860)),
        )

    assert str(err_info.value) == (
        'Fingerprinter Failed: the maximum length of a Document record'
        ' is 840 characters.'
    )


@responses.activate
@pytest.mark.parametrize('min_score', [
    None,
    800,
])
def test_record_add_document(min_score, connection, project, document):
    """Verifies adding document records to a project."""
    with io.open(DOCUMENT_RECORD_PATH, 'rb') as f:
        content = f.readline()[0:840]

    responses.add(
        method=responses.POST,
        url='{}/records/upload/document/{}'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            project.upload_token
        ),
        json={
            'id': uuid.uuid4().hex,
            'name': 'name',
            'description': '',
            'ctime': time.time(),
            'mtime': time.time(),
            'metadata': '{}',
        },
        status=200
    )

    record = connection.records.add_document(
        project=project,
        name=document['name'],
        description=document['description'],
        content=content,
        user_record_id='12345',
        min_score=min_score)
    assert len(responses.calls) == 1

    record = connection.records.add_document(
        project=project,
        name=document['name'],
        description=document['description'],
        content=content,
        user_record_id=12345,
        min_score=min_score,
        offline=True)
    assert isinstance(record, dict)
    assert len(responses.calls) == 1


@responses.activate
def test_record_add_pii(connection, project, pii_records_raw):
    """Verifies adding PII records to a project."""
    record_data = [
        {
            'id': uuid.uuid4().hex,
            'name': matchlight.utils.blind_email(record['email']),
            'description': '',
            'ctime': time.time(),
            'mtime': time.time(),
        }
        for record in pii_records_raw
    ]

    for payload in record_data:
        responses.add(
            method=responses.POST,
            url='{}/records/upload/pii/{}'.format(
                matchlight.MATCHLIGHT_API_URL_V2,
                project.upload_token
            ),
            json={
                'id': payload['id'],
                'name': payload['name'],
                'description': payload['description'],
                'ctime': payload['ctime'],
                'mtime': payload['mtime'],
                'metadata': '{}',
            },
            status=200
        )

    for counter, pii_record in enumerate(pii_records_raw):
        record = connection.records.add_pii(
            project=project,
            description='',
            **pii_record)
        assert record.id == record_data[counter]['id']
        assert len(responses.calls) == counter + 1

    for counter, pii_record in enumerate(pii_records_raw):
        record = connection.records.add_pii(
            project=project,
            description='',
            offline=True,
            **pii_record)
        assert isinstance(record, dict)
        assert len(responses.calls) == 6

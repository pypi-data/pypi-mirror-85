"""Unit tests the alert methods of the Matchlight SDK."""
import datetime
import json

import responses

import matchlight


@responses.activate
def test_pii_search(connection, pii_search_email_only_results):
    """Verifies alert listing and filtering."""
    responses.add(
        method=responses.POST,
        url='{}/pii_search'.format(matchlight.MATCHLIGHT_API_URL_V2),
        json={'results': pii_search_email_only_results},
        status=200
    )

    assert list(
        connection.pii_search(email='familybird@terbiumlabs.com')
    ) == [
        {
            'fields': ['email'],
            'ts': datetime.datetime.strptime(
                '2018-07-25T20:00:44',
                '%Y-%m-%dT%H:%M:%S'
            ),
            'source': 'Exactis Breach June 2018'
        },
        {
            'fields': ['email'],
            'ts': datetime.datetime.strptime(
                '2017-01-25T02:35:04',
                '%Y-%m-%dT%H:%M:%S'
            ),
            'source': 'https://pastebin.com/raw.php?i=1DgbtSZc'
        },
        {
            'fields': ['email'],
            'ts': datetime.datetime.fromtimestamp(1556221970.0),
            'source': 'Zoosk Breach Nov 2016'
        },
        {
            'fields': ['email'],
            'ts': datetime.datetime.fromtimestamp(1558333205.0),
            'source': 'https://www.reddit.com/r/AskReddit/comments/3oqj4a'
        }
    ]

    assert json.loads(responses.calls[0].request.body) == {
        'email_fingerprints': [['ff71225ace46c2b0'], ['293de73a18a5e063']],
        'limit': 50,
    }


@responses.activate
def test_pii_search_limit(connection, pii_search_email_only_results):
    """Verifies alert listing and filtering."""
    responses.add(
        method=responses.POST,
        url='{}/pii_search'.format(matchlight.MATCHLIGHT_API_URL_V2),
        json={'results': pii_search_email_only_results[:2]},
        status=200
    )

    assert list(
        connection.pii_search(email='familybird@terbiumlabs.com', limit=2)
    ) == [
        {
            'fields': ['email'],
            'ts': datetime.datetime.strptime(
                '2018-07-25T20:00:44',
                '%Y-%m-%dT%H:%M:%S'
            ),
            'source': 'Exactis Breach June 2018'
        },
        {
            'fields': ['email'],
            'ts': datetime.datetime.strptime(
                '2017-01-25T02:35:04',
                '%Y-%m-%dT%H:%M:%S'
            ),
            'source': 'https://pastebin.com/raw.php?i=1DgbtSZc'
        }
    ]

    assert json.loads(responses.calls[0].request.body) == {
        'email_fingerprints': [['ff71225ace46c2b0'], ['293de73a18a5e063']],
        'limit': 2,
    }


@responses.activate
def test_search_email(connection, search_email_only_results):
    """Verifies generic search when using email."""
    responses.add(
        method=responses.POST,
        url='{}/detailed_search'.format(matchlight.MATCHLIGHT_API_URL_V2),
        json={'results': search_email_only_results},
        status=200
    )

    assert list(
        connection.search(email='familybird@terbiumlabs.com')
    ) == [
        {
            'score': 800,
            'ts': datetime.datetime.fromtimestamp(1453298293.0),
            'url': (
                'http://blockchainbdgpzk.onion/tx/4f4097992b89156'
                '690817556fc3f540535bdfadde06661c9cae21d500943f970'
            )
        }, {
            'score': 800,
            'ts': datetime.datetime.fromtimestamp(1438870917.0),
            'url': (
                'http://nqigfqrxnkwcqmiq.onion/'
                'wiki/index.php#Whistleblowing'
            )
        }
    ]

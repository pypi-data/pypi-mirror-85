"""Agent for Automated Test Equipment.

This example agent automates testing in conjuntion with the Cloud Service.

"""
import logging
from functools import wraps
import pprint
from six.moves.urllib import parse as urlparse
import requests
from requests.exceptions import ConnectionError  # raised by responses
import responses
import sys
import time
import json
import six
from six.moves import configparser

if six.PY2:
  ConfigParser = configparser.SafeConfigParser
else:
  ConfigParser = configparser.ConfigParser


log = logging.getLogger(__name__)
logging.getLogger("responses").setLevel(logging.WARNING)


def _step(function):
    """See -s flag. Decorator to enable a pause in operations."""
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        msg = '{} to continue PRESS ENTER.'.format(function.__name__.upper())
        six.moves.input(msg) if self.step else None
        return function(self, *args, **kwargs)
    return wrapper


def _make_url(base, parts):
    """Helper function to append path parts to cloud url.

    The list of path parts are joined to create the url path.

    Args:
        base (string): base url, e.g. http://localhost:8080
        parts (list): string parts of the url path, e.g. ['api', 'v1']

    Returns:
        string: full path url, e.g. "http://localhost:8080/api/v1"

    """
    pieces = list(urlparse.urlparse(base))
    path = '/'.join(parts)
    pieces[2] = '/'.join([pieces[2], path])
    return urlparse.urlunparse(pieces)


def make_json(items):
    """Helper function to create a Pythonic JSON object from a list.

    Converts string integer with integer.
    Converts string to boolean for strings ('true', 'True', 'false', 'False')
    
    Args:
        items (list): list of key, value tuples

    Returns:
        dict: dictionary with values of type string, int, and bool

    """
    true_values = ('true', 'True')
    false_values = ('false', 'False')
    items = [(k, int(v)) if v.isdigit() else (k, v) for k, v in items]
    items = [(k, True) if v in true_values else (k, v) for k, v in items]
    items = [(k, False) if v in false_values  else (k, v) for k, v in items]
    
    return dict(items)
    

def _verbose_http(response):
    """See -v flag.  Helper function to log HTTP interaction.

    Args:
        response (:obj:`requests.Response`): response from HTTP server

    """
    # Details of REQUEST to server.
    log.debug(50*'-')
    log.debug(50*'>')
    log.debug('> HTTP {} {}'.format(response.request.method,
                                    response.request.url))
    for h in response.request.headers:
        log.debug('> HTTP {}: {}'.format(h, response.request.headers[h]))
    log.debug('> HTTP Body: {}'.format(response.request.body))

    # Details of RESPONSE from server.
    log.debug(50*'<')
    log.debug('< HTTP URL: {}'.format(response.url))
    log.debug('< HTTP Status: {}'.format(response.status_code))
    for h in response.headers:
        log.debug('< HTTP {}: {}'.format(h, response.headers[h]))
    try:
        body = response.json()
    except ValueError as e:
        body = response.text
    finally:
        log.debug('< HTTP Body: {}'.format(body))

    for h in response.history:
        log.debug('< HTTP Response.history {} {}'.format(
            h.status_code, h.headers['Location']))
    log.debug(50*'-')


class Agent(object):
    """Example implementation of an Agent for Cloud Service.

    Args:
        user (str): username credential for HTTP Basic Auth for ATE Server.
        passkey (str): passkey credential for HTTP Basic Auth for ATE Server.
        cloud (str): fullpath URL of Cloud Service excluding API version.
        step (bool): interrupted program execution with user prompts if True.
        fname (str): filename for config ini defining the mock API stubs.

    Attributes:
        aaa (tuple(str)): user and passkey tuple to inject HTTP Basic Auth
            into :obj:`requests.Session`.
        step (bool): True if ``step`` and will cause command line pause between
            key parts of the overall program.  Useful to watch what happens
            on the command line terminal.  `CAUTION: requires keyboard input.`
        mock_parser (:obj:`ConfigParser.SafeConfigParser`): off-the-shelf
            parser that loads mock API configuration file.
        url_cloud (str): base URL of Cloud Service including API version.
        url_devices_collection (str): RESTful endpoint of Cloud Service to
            register an Agent.
        url_devices_item (str): RESTful endpoint of Cloud Service to request
            details of a specific device including the test plan.
        url_cases_collection (str): RESTful endpoint of Cloud Service to
            request resource for a test case.

    """
    path_parts = ['api', 'v1']
    """list(str): Hardcoded segmets of the Cloud Service URL path."""

    def __init__(self, user, passkey, cloud, step=False, fname=str()):
        self.aaa = (user, passkey)
        self.step = step

        # Mock API for DUT and ATE.
        self.mock_parser = ConfigParser()
        try:
            self.mock_parser.read(fname)
        except TypeError as e:  # when fname == None
            log.warning(e)

        # Cloud Service URL's.
        self.url_cloud = _make_url(cloud, self.path_parts)
        self.url_devices_collection = _make_url(self.url_cloud, ['devices'])
        self.url_devices_item = _make_url(self.url_cloud, ['devices', user])
        self.url_cases_collection = _make_url(self.url_cloud, ['cases'])

    def __str__(self):
        str_agent = pprint.pformat(vars(self))        
        # flatten config file sections and items
        str_mock = [' '.join([section, json.dumps(
            make_json(self.mock_parser.items(section)))]) for
            section in self.mock_parser.sections()]
        str_mock = pprint.pformat(str_mock)
        return  '\n'.join(['\nAgent', str_agent, 'Mock API', str_mock])
        
    @_step
    def register(self):
        """Request the Cloud Service to create resource for this device.

        Cloud Service will bind UUID (unique hardware address) to passkey.
        Cloud Service may limit the number of UUID that bind to a passkey.
        Passkey is unique to a user account on the Cloud Service;
        Don't share your passkey!

        Example:
            In your script that operates ab Agent, behavior can be different
            between a new registration and using this method to verify
            the device is already registered::

                status = agent.register()
                if status == 200:
                    # behavior if already registered.
                elif status == 201:
                    # behavior because successful new registration.

        Returns:
            int: HTTP status code if less than 400.

            The Cloud Service may return HTTP Status:
            ``200 OK`` if UUID is already bound to passkey, or
            ``201 CREATED`` if successful bind UUID to unbound passkey.

        Raises:
            requests.exceptions.RequestException:
                Raised if HTTP Status is 4XX or 5XX.
                The Cloud Service may return HTTP Status:
                ``401 UNAUTHORIZED`` if PASSKEY is unknown, or
                ``403 FORBIDDEN`` if PASSKEY is already bound.

        """
        log.info('STEP 0: REGISTER AGENT TO CLOUD')
        try:
            r = requests.post(self.url_devices_collection, auth=self.aaa)
            r.raise_for_status()  # HTTP Status 4xx or 5xx
        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.InvalidURL) as e:
            # HTTPError = r.raise_for_status HTTP Status Code 4xx or 5xx.
            # ConnectionError = network problem, URL is not reachable.
            # InvalidURL = malformed URL to begin with.
            raise requests.exceptions.RequestException(e)
        else:
            _verbose_http(r)
            message = {200: 'STEP 0: OK AGENT ALREADY REGISTERED.',
                       201: 'STEP 0: OK SUCCESSFULLY CREATE NEW AGENT.',
                       401: 'STEP 0: FAIL UNAUTHORIZED PASSKEY IS UNKNOWN.',
                       403: 'STEP 0: FAIL FORBIDDEN PASSKEY ALREADY IN USE'}
            log.info(message[r.status_code])

        return r.status_code

    @_step
    def run(self):
        """Main loop to execute all testcases from Cloud assigned to this UUID.

        """
        # Session is used to persist cookie from Cloud Service across requests.
        with requests.Session() as session:
            # First, get cases to execute and session tracker.
            tests = self._download(session)

            # Then, execute each case.
            try:
                for k, v in tests.items():
                    self._create_test_resource(k, v, session)
                    self._prgauto(k, v, session)
                    log.info('END OF CASE {}'.format(k))
            except AttributeError as e:
                log.warning('NO CASES AVAILABLE.')
                log.warning(e)
            else:
                log.info('GOODBYE, ALL CASES IN PLAN HAVE BEEN RUN.')

    @_step
    def _download(self, session):
        """Fetch the cases to execute and a new session tracker.

        Returns:
            tests (:obj:`dict`): test cases from Cloud Service.
                Empty dict if missing deployment or no cases available.
                Example dict looks like::

                {
                    u'case-1': u'2018-08-03T12:00:17.790590',
                    u'mycase': u'2018-08-03T12:00:17.790590'
                }

        """
        log.info('STEP 1: GET TEST CASES FROM CLOUD.')
        try:
            r = session.get(self.url_devices_item, auth=self.aaa)
            r.raise_for_status()
            tests = r.json()
        except requests.exceptions.HTTPError as e:
            # raise_for_status()
            # when GET fail HTTP Basic Auth if not registered
            log.warning(e)
            tests = dict()
        except ValueError as e:
            # r.json() when JSON not in HTTP body or when emtpy HTTP body.
            log.warning(e)
            tests = dict()
            _verbose_http(r)
        else:
            _verbose_http(r)
            log.info('STEP 1: GOT CASES: {}'.format(', '.join(tests.keys())))

        return tests

    @_step
    def _create_test_resource(self, name, created, session):
        """Request to create dedicated testing resource on Cloud Service.

        Be sure to include the session tracker cookie in the request to
        the Cloud Service.  This ensures results are correctly recorded.

        The Cloud Service expects the POST to include json data for the
        individual test case.  Do not use an envelope for the json data.
        Example data looks like::

            {
                `name`: created
            }

        Args:
            name (str): name of test case.
            created (str): timestamp identifier of test.
            session (:obj:`requests.Session`): because need cookies.

        Returns:
            requests.Response: HTTP response from Cloud.

        """
        log.info('STEP 2: REQUEST TO CREATE TEST RESOURCE {}'.format(name))
        try:
            r = session.post(self.url_cases_collection,
                             json={name: created},
                             auth=self.aaa)
            r.raise_for_status()  # HTTP Status 4xx or 5xx
        except requests.exceptions.RequestException as e:
            # HTTPError from r.raise_for_status() HTTP 401 Unauthorized.
            # InvalidURL is malformed URL.
            log.warning('STEP 2....WRONG')
            log.warning(r.json())
            log.warning(e)
            sys.exit(r.json())
        else:
            _verbose_http(r)
            log.info('STEP 2: OK, CREATED TEST RESOURCE {}'.format(name))
            return r

    @_step
    def _prgauto(self, name, created, session):
        """Automatically work through interaction with Cloud Service.

        Requests module will automatically Redirect-Get following response
        status code 303 if both conditions are satisfied:
            1) HTTP header Location is defined
            2) Requests allow_redirect optional argument is True. Default True.

        Requests module internally tracks Post-Redirect-Get using attribute
        called 'history', so use this to monitor PRG occurances.

        """
        # You must do this first step manually.  JSON must be empty dict.
        log.info('STEP 3: REQUEST TO START CASE {}'.format(name))
        url = _make_url(self.url_cases_collection, [name])
        try:
            response_from_cloud = session.put(url, json=dict(), auth=self.aaa)
        except requests.exceptions.RequestException as e:
            log.warning(e)
        else:
            _verbose_http(response_from_cloud)
            log.info('STEP 3: OK, STARTED CASE {}'.format(name))

        try:
            urlnext = response_from_cloud.links['next']['url']
        except KeyError as e:
            log.critical('GOODBYE, MISSING LINK HEADER')
            urlnext = None

        # Continue to automatically process the rest of the steps.
        log.info('STEP 3: WORK THROUGH EACH STEP....')
        while urlnext is not None:
            six.moves.input('Press ENTER to continue.') if self.step else None

            # Respect the Cloud Service instruction for time delay.
            try:
                seconds = int(response_from_cloud.headers.get('retry-after'))
                log.info(' '.join(['sleeping for ', seconds, 'seconds']))
                for second in range(seconds):
                    log.info('sleeping for a second.')
                    time.sleep(1)
            except KeyError:  # HTTP Header Retry-After does not exist.
                log.debug('no time for sleep.')
            except ValueError:  # HTTP Header Retry-After not an integer.
                log.debug('HTTP Header Retry-After is not integer.')
            except TypeError:  # HTTP Header Retry-After 
                log.debug('no time for sleep.')
            else:
                log.info('waking up.')

            # Proxy communications to DUT or ATE
            # !!! Do NOT use session to avoid damaging cookie from cloud.
            # !!! use requests.request to avoid damaging cookie from cloud.
            with responses.RequestsMock() as mock_response_from_device:

                # oops, something bad happened.
                if not response_from_cloud.ok:  # LESS THAN HTTP 4XX
                    log.warning('Oops, HTTP 4xx or 5xx error from cloud.')
                    # TODO something graceful
                    
                # determine if Agent should POST or GET to device.
                # r.history exists if Requests automatically redirects.
                method = 'POST' if response_from_cloud.history else 'GET'

                # add URL to Mock API, or make Real passthru.
                section = ' '.join([method, urlnext])
                try:
                    items = self.mock_parser.items(section)
                except configparser.NoSectionError:
                    mock_response_from_device.add_passthru(urlnext)
                else:
                    log.info(' '.join(['Creating Mock API Response', urlnext]))
                    mock_response_status = 201 if method == 'POST' else 200
                    mock_response_json = make_json(items)
                    mock_response_from_device.add(
                        method, urlnext, json=mock_response_json,
                        status=mock_response_status)

            
                # execute the proxy communication to device.
                # regardless if Mock or Real passthru
                try:
                    response_from_device = requests.request(
                        method, urlnext, json=response_from_cloud.json())
                except ValueError as e:  # via requests.response.json
                    log.debug(e)
                except ConnectionError as e:  # via responses package.
                    log.debug(e)
                else:
                    _verbose_http(response_from_device)


            # Extract data from device response.
            try:
                j = response_from_device.json()
            except ValueError as e:  # response does not contain valid json.
                log.warning(e)
                j = None

            # Update Cloud Service with data from DUT or ATE.
            # !!! use session in order to return cookie to server.
            try:
                response_from_cloud = session.put(
                    response_from_cloud.links['self']['url'],
                    json=j, auth=self.aaa)
            except ConnectionError:
                pass
            else:
                _verbose_http(response_from_cloud)

            # Process next link, KeyError is end of protocol.
            try:
                urlnext = response_from_cloud.links['next']['url']
                # urlself = r.links['self']['url']
            except KeyError as e:
                urlnext = None


if __name__ == '__main__':
    pass

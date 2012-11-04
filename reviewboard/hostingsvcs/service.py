import base64
import logging
import mimetools
import urllib2
from pkg_resources import iter_entry_points

from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _


class HostingService(object):
    """An interface to a hosting service for repositories and bug trackers.

    HostingService subclasses are used to more easily configure repositories
    and to make use of third party APIs to perform special operations not
    otherwise usable by generic repositories.

    A HostingService can specify forms for repository and bug tracker
    configuration.

    It can also provide a list of repository "plans" (such as public
    repositories, private repositories, or other types available to the hosting
    service), along with configuration specific to the plan. These plans will
    be available when configuring the repository.
    """
    name = None
    plans = None
    supports_bug_trackers = False
    supports_repositories = False
    supports_ssh_key_association = False

    # These values are defaults that can be overridden in repository_plans
    # above.
    needs_authorization = False
    supported_scmtools = []
    form = None
    fields = []
    repository_fields = {}
    bug_tracker_field = None

    def __init__(self, account):
        assert account
        self.account = account

    def is_authorized(self):
        """Returns whether or not the account is currently authorized.

        An account may no longer be authorized if the hosting service
        switches to a new API that doesn't match the current authorization
        records. This function will determine whether the account is still
        considered authorized.
        """
        return False

    def associate_ssh_key(self, repository, key):
        """Associates an SSH key with a given repository

        The `key` (an instance of :py:mod:`paramiko.PKey`) will be added to
        the hosting service's list of deploy keys (if possible). If there
        is a problem uploading the key to the hosting service, a
        :py:exc:`SSHKeyAssociationError` will be raised.
        """
        raise NotImplementedError

    def authorize(self, username, password, local_site_name=None,
                  *args, **kwargs):
        raise NotImplementedError

    def get_file(self, repository, path, revision, *args, **kwargs):
        if not self.supports_repositories:
            raise NotImplementedError

        return repository.get_scmtool().get_file(path, revision)

    def get_file_exists(self, repository, path, revision, *args, **kwargs):
        if not self.supports_repositories:
            raise NotImplementedError

        return repository.get_scmtool().file_exists(path, revision)

    @classmethod
    def get_repository_fields(cls, username, plan, tool_name, field_vars):
        if not cls.supports_repositories:
            raise NotImplementedError

        # Grab the list of fields for population below. We have to do this
        # differently depending on whether or not this hosting service has
        # different repository plans.
        fields = cls._get_field(plan, 'repository_fields')

        new_vars = field_vars.copy()
        new_vars['hosting_account_username'] = username

        results = {}

        for field, value in fields[tool_name].iteritems():
            try:
                results[field] = value % new_vars
            except KeyError, e:
                logging.error('Failed to generate %s field for hosting '
                              'service %s using %s and %r: Missing key %s'
                              % (field, unicode(cls.name), value, new_vars, e),
                              exc_info=1)
                raise KeyError(
                    _('Internal error when generating %(field)s field '
                      '(Missing key "%(key)s"). Please report this.') % {
                          'field': field,
                          'key': e,
                      })

        return results

    @classmethod
    def get_bug_tracker_requires_username(cls, plan=None):
        if not cls.supports_bug_trackers:
            raise NotImplementedError

        return ('%(hosting_account_username)s' in
                cls._get_field(plan, 'bug_tracker_field', ''))

    @classmethod
    def get_bug_tracker_field(cls, plan, field_vars):
        if not cls.supports_bug_trackers:
            raise NotImplementedError

        bug_tracker_field = cls._get_field(plan, 'bug_tracker_field')

        if not bug_tracker_field:
            return ''

        try:
            return bug_tracker_field % field_vars
        except KeyError, e:
            logging.error('Failed to generate %s field for hosting '
                          'service %s using %r: Missing key %s'
                          % (bug_tracker_field, unicode(cls.name),
                             field_vars, e),
                          exc_info=1)
            raise KeyError(
                _('Internal error when generating %(field)s field '
                  '(Missing key "%(key)s"). Please report this.') % {
                      'field': bug_tracker_field,
                      'key': e,
                  })

    @classmethod
    def _get_field(cls, plan, name, default=None):
        if cls.plans:
            assert plan

            for plan_name, info in cls.plans:
                if plan_name == plan and name in info:
                    return info[name]

        return getattr(cls, name, default)

    #
    # HTTP utility methods
    #

    def _json_get(self, *args, **kwargs):
        data, headers = self._http_get(*args, **kwargs)
        return simplejson.loads(data), headers

    def _json_post(self, *args, **kwargs):
        data, headers = self._http_post(*args, **kwargs)
        return simplejson.loads(data), headers

    def _http_get(self, url, *args, **kwargs):
        r = self._build_request(url, *args, **kwargs)
        u = urllib2.urlopen(r)
        return u.read(), u.headers

    def _http_post(self, url, body=None, fields={}, files={},
                   content_type=None, headers={}, *args, **kwargs):
        headers = headers.copy()

        if body is None:
            if fields is not None:
                body, content_type = self._build_form_data(fields, files)
            else:
                body = ''

        if content_type:
            headers['Content-Type'] = content_type

        headers['Content-Length'] = str(len(body))

        r = self._build_request(url, body, headers, **kwargs)
        u = urllib2.urlopen(r)
        return u.read(), u.headers

    def _build_request(self, url, body=None, headers={}, username=None,
                       password=None):
        r = urllib2.Request(url, body, headers)

        if username is not None and password is not None:
            r.add_header(urllib2.HTTPBasicAuthHandler.auth_header,
                         'Basic %s' % base64.b64encode(username + ':' +
                                                       password))

        return r

    def _build_form_data(self, fields, files):
        """Encodes data for use in an HTTP POST."""
        BOUNDARY = mimetools.choose_boundary()
        content = ""

        for key in fields:
            content += "--" + BOUNDARY + "\r\n"
            content += "Content-Disposition: form-data; name=\"%s\"\r\n" % key
            content += "\r\n"
            content += str(fields[key]) + "\r\n"

        for key in files:
            filename = files[key]['filename']
            value = files[key]['content']
            content += "--" + BOUNDARY + "\r\n"
            content += "Content-Disposition: form-data; name=\"%s\"; " % key
            content += "filename=\"%s\"\r\n" % filename
            content += "\r\n"
            content += value + "\r\n"

        content += "--" + BOUNDARY + "--\r\n"
        content += "\r\n"

        content_type = "multipart/form-data; boundary=%s" % BOUNDARY

        return content_type, content


def get_hosting_services():
    """Gets the list of hosting services.

    This will return an iterator for iterating over each hosting service.
    """
    for entry in iter_entry_points('reviewboard.hosting_services'):
        try:
            cls = entry.load()
        except Exception, e:
            logging.error('Unable to load repository hosting service %s: %s' %
                          (entry, e))
            continue

        yield (entry.name, cls)


def get_hosting_service(name):
    """Retrieves the hosting service with the given name.

    If the hosting service is not found, None will be returned.
    """
    entries = list(iter_entry_points('reviewboard.hosting_services', name))

    if entries:
        entry = entries[0]

        try:
            return entry.load()
        except Exception, e:
            logging.error('Unable to load repository hosting service %s: %s' %
                          (entry, e))

    return None

import json
import logging
import httpx

from ..exceptions import ClientException, ApiException
from ..const import API_URL

LOG = logging.getLogger(__package__)

class NgenicBase(object):
    """Superclass for all models"""

    def __init__(self, token, json):
        """Initialize our base object.

        :param token:
            (required) OAuth2 bearer token
        :param json:
            (required) Json representation of the concrete model
        """

        # this will be added to the HTTP Authorization header for each request
        self._token = token

        # this header will be added to each HTTP request
        self._auth_headers = {"Authorization": "Bearer %s" % self._token}

        # backing json of the model
        self._json = json

    def json(self):
        """Get a json representaiton of the model

        :return:

        """
        return self._json

    def uuid(self):
        """Get uuid attribute"""
        return self["uuid"]

    def __setitem__(self, attribute, data):
        self._json[attribute] = data

    def __getitem__(self, attribute):
        if attribute not in self._json:
            raise AttributeError(attribute)
        return self._json[attribute]

    def update(self):
        raise ClientException("Cannot update a '%s'" % self.__class__.__name__)

    def _parse(self, response):
        rsp_json = None

        if response is None:
            return None

        if response.status_code == 204:
            return None

        try:
            rsp_json = response.json()
        except ValueError:
            raise ApiException("Ngenic API return an invalid json body (status=%d)" % response.status_code)

        return rsp_json

    def _new_instance(self, instance_class, json, **kwargs):
        """Create a new model instance

        :param class instance_class:
            (required) class of instance to initialize with json
        :param dict json:
            (required) data to initialize the instance with
        :param kwargs:
            Additional data required by the instance type
        :return:
            new `instance_class` or `list(instance_class)`
        """
        if json is not None and (not isinstance(json, dict) and not isinstance(json, list)):
            raise ClientException("Invalid data to create new instance with (expected json)")
        if not json:
            return None

        if isinstance(json, list):
            return list(instance_class(self._token, x, **kwargs) for x in json)
        else:
            return instance_class(self._token, json, **kwargs)

    def _parse_new_instance(self, url, instance_class, **kwargs):
        """Get JSON from an URL and create a new instance of it

        :param str url:
            (required) url to get instance data from
        :param class instance_class:
            (required) class of instance to initialize with parsed data
        :param kwargs:
            may contain additional args to the instance class
        :return:
            new `instance_class`
        :rtype:
            `instance_class`
        """
        ret_json = self._parse(self._get(url))
        return self._new_instance(instance_class, ret_json, **kwargs)

    async def _async_parse_new_instance(self, url, instance_class, **kwargs):
        """Get JSON from an URL and create a new instance of it

        :param str url:
            (required) url to get instance data from
        :param class instance_class:
            (required) class of instance to initialize with parsed data
        :param kwargs:
            may contain additional args to the instance class
        :return:
            new `instance_class`
        :rtype:
            `instance_class`
        """
        ret_json = self._parse(await self._async_get(url))
        return self._new_instance(instance_class, ret_json, **kwargs)

    def _request(self, method, *args, **kwargs):
        """Make a HTTP request.
        This is the generic method for all requests, it will handle errors etc in a common way.

        :param str method:
            (required) HTTP method (i.e get, post, delete)
        :param args:
            Additional args to requests lib
        :param kwargs:
            Additional kwargs to requests lib
        :return:
            request
        """
        r = None
        try:
            request_method = getattr(httpx, method)
            r = request_method(*args, **kwargs)

            # raise for e.g. 401
            r.raise_for_status()

            return r
        except httpx.HTTPError as exc:
            raise ClientException(self._get_error("A request exception occurred", r, parent_ex=exc))
        except Exception as exc:
            raise ClientException(self._get_error("An exception occurred", r, parent_ex=exc))

    async def _async_request(self, method, *args, **kwargs):
        """Make a HTTP request (async).
        This is the generic method for all requests, it will handle errors etc in a common way.

        :param str method:
            (required) HTTP method (i.e get, post, delete)
        :param args:
            Additional args to requests lib
        :param kwargs:
            Additional kwargs to requests lib
        :return:
            request
        """
        r = None
        try:
            async with httpx.AsyncClient() as client:
                request_method = getattr(client, method)
                r = await request_method(*args, **kwargs)

                # raise for e.g. 401
                r.raise_for_status()

                return r
        except httpx.HTTPError as exc:
            raise ClientException(self._get_error("A request exception occurred", r, parent_ex=exc))
        except Exception as exc:
            raise ClientException(self._get_error("An exception occurred", r, parent_ex=exc))

    def _get_error(self, msg, req, parent_ex=None):
        if req is not None and req.status_code == 429:
            # Too many requests
            server_msg = "Too many requests have been made, retry again after %s" % req.headers["X-RateLimit-Reset"]
        else:
            try:
                server_msg = req.json()["message"]
            except:
                if req is not None:
                    server_msg = str(req.status_code)
                elif parent_ex is not None:
                    server_msg = str(parent_ex)
                else:
                    server_msg = "Unknown error"
                pass

        return "%s: %s" % (msg, server_msg)

    def _prehandle_write(self, data, is_json, **kwargs):
        headers = self._auth_headers.copy()

        if is_json:
            data = json.dumps(data) if data is not None else data
            headers["Content-Type"] = "application/json"

        if "headers" in kwargs:
            # let caller override headers
            headers.update(kwargs.get("headers"))

        return (data, headers)

    def _delete(self, url, **kwargs):
        LOG.debug("DELETE %s with %s", url, kwargs)
        return self._request("delete",
                             "%s/%s" % (API_URL, url),
                             headers=self._auth_headers)
                            
    def _async_delete(self, url, **kwargs):
        LOG.debug("DELETE %s with %s", url, kwargs)
        return self._async_request("delete",
                             "%s/%s" % (API_URL, url),
                             headers=self._auth_headers)

    def _get(self, url, **kwargs):
        LOG.debug("GET %s with %s", url, kwargs)
        return self._request("get",
                             "%s/%s" % (API_URL, url),
                             headers=self._auth_headers,
                             **kwargs)

    async def _async_get(self, url, **kwargs):
        LOG.debug("GET %s with %s", url, kwargs)
        return await self._async_request("get",
                             "%s/%s" % (API_URL, url),
                             headers=self._auth_headers,
                             **kwargs)

    def _post(self, url, data=None, is_json=True, **kwargs):
        data, headers = self._prehandle_write(data, is_json, kwargs)

        LOG.debug("POST %s with %s, %s", url, data, kwargs)
        return self._request("post",
                             "%s/%s" % (API_URL, url),
                             data=data,
                             headers=headers)

    def _async_post(self, url, data=None, is_json=True, **kwargs):
        data, headers = self._prehandle_write(data, is_json, kwargs)

        LOG.debug("POST %s with %s, %s", url, data, kwargs)
        return self._async_request("post",
                             "%s/%s" % (API_URL, url),
                             data=data,
                             headers=headers)

    def _put(self, url, data=None, is_json=True, **kwargs):
        data, headers = self._prehandle_write(data, is_json, **kwargs)
        
        LOG.debug("PUT %s with %s, %s", url, data, kwargs)
        return self._request("put",
                             "%s/%s" % (API_URL, url),
                             data=data,
                             headers=headers)

    def _async_put(self, url, data=None, is_json=True, **kwargs):
        data, headers = self._prehandle_write(data, is_json, **kwargs)
        
        LOG.debug("PUT %s with %s, %s", url, data, kwargs)
        return self._async_request("put",
                             "%s/%s" % (API_URL, url),
                             data=data,
                             headers=headers)

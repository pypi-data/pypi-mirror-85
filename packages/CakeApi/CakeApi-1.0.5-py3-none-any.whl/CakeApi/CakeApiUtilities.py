from requests.sessions import session
from requests.models import Response
import urllib3
from unittest.case import TestCase


class CreateApiCollection:

    def __init__(self, baseUrl: str = None, proxyHost: str = None, proxyPort: str = None, proxyUsername: str = None,
                 proxyPassword: str = None, verifySSL: bool = False, certificatePath: str = None,
                 auth: bool = False,
                 authUserName: str = None, authPassword: str = None, disableInsecureRequestWarning: bool = False):
        if disableInsecureRequestWarning is True:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.__currentResponse: Response
        self.__session = session()
        if baseUrl is not None:
            self.__baseUrl: str = baseUrl
        else:
            self.__baseUrl: str = ""
        if verifySSL is True:
            if certificatePath is None:
                raise Exception("Since you have set ssl as true, please provide certificate path.")
            self.__session.verify = certificatePath
        else:
            self.__session.verify = False
        if auth is True:
            if authUserName is None or authPassword is None:
                raise Exception(
                    "Since you have set auth as true you need to provide username and password for authentication.")
            else:
                self.__session.auth = (authUserName, authPassword)
        if proxyHost is not None and proxyPort is not None:
            if proxyUsername is not None and proxyPassword is not None:
                self.__session.proxies = {
                    'http': 'http://' + proxyUsername + ':' + proxyPassword + '@' + proxyHost + ':' + proxyPort,
                    'https': 'https://' + proxyUsername + ':' + proxyPassword + '@' + proxyHost + ':' + proxyPort
                }
            else:
                if proxyUsername is None and proxyPassword is not None:
                    raise Exception("Proxy password is provided but username is none, make sure username is provided")
                if proxyPassword is None and proxyUsername is not None:
                    raise Exception("Proxy username is provided but password is none, make sure password is provided")
                self.__session.proxies = {
                    'http': 'http://' + proxyHost + ':' + proxyPort,
                    'https': 'https://' + proxyHost + ':' + proxyPort
                }
        else:
            if proxyHost is not None and proxyPort is None:
                raise Exception('Proxy host is provided but port is none, please make sure port is provided')
            if proxyHost is None and proxyPort is not None:
                raise Exception('Proxy port is provided but host is none, please make sure host is provided')
        self.__collectionVariables: dict = {}

    def getTestUtils(self):
        """
        This function returns test utilities
        :return:
        """
        return TestCase()

    def hitTheGetRequest(self, url: str, params=None, headers=None, cookies=None,
                         auth=None, timeout=None, allow_redirects=True,
                         hooks=None, stream=None, cert=None):
        """Constructs a :method:`GET Request <Request>`, prepares it and sends it.
                            Returns :class: stores response and returns `self` object.

                            :param url: URL for the new :class:`Request` object.
                            :param params: (optional) Dictionary or bytes to be sent in the query
                                string for the :class:`Request`.
                            :param headers: (optional) Dictionary of HTTP Headers to send with the
                                :class:`Request`.
                            :param cookies: (optional) Dict or CookieJar object to send with the
                                :class:`Request`.
                            :param auth: (optional) Auth tuple or callable to enable
                                Basic/Digest/Custom HTTP Auth.
                            :param timeout: (optional) How long to wait for the server to send
                                data before giving up, as a float, or a :ref:`(connect timeout,
                                read timeout) <timeouts>` tuple.
                            :type timeout: float or tuple
                            :param allow_redirects: (optional) Set to True by default.
                            :type allow_redirects: bool
                            :param proxies: (optional) Dictionary mapping protocol or protocol and
                                hostname to the URL of the proxy.
                            :param stream: (optional) whether to immediately download the response
                                content. Defaults to ``False``.
                            :param verify: (optional) Either a boolean, in which case it controls whether we verify
                                the server's TLS certificate, or a string, in which case it must be a path
                                to a CA bundle to use. Defaults to ``True``.
                            :param cert: (optional) if String, path to ssl client cert file (.pem).
                                If Tuple, ('cert', 'key') pair.
                            """
        self.__currentResponse = self.__session.get(url=self.__baseUrl + url,
                                                    headers=headers,
                                                    params=params or {},
                                                    auth=auth,
                                                    cookies=cookies,
                                                    hooks=hooks,
                                                    timeout=timeout,
                                                    allow_redirects=allow_redirects,
                                                    stream=stream, cert=cert)
        return self

    def hitThePostRequest(self, url: str, params=None, data=None, json=None, headers=None, cookies=None,
                          auth=None, timeout=None, allow_redirects=True,
                          hooks=None, stream=None, cert=None):
        """Constructs a :method:`POST Request <Request>`, prepares it and sends it.
                            Returns :class: stores response and returns `self` object.

                            :param url: URL for the new :class:`Request` object.
                            :param params: (optional) Dictionary or bytes to be sent in the query
                                string for the :class:`Request`.
                            :param data: (optional) Dictionary, list of tuples, bytes, or file-like
                                object to send in the body of the :class:`Request`.
                            :param json: (optional) json to send in the body of the
                                :class:`Request`.
                            :param headers: (optional) Dictionary of HTTP Headers to send with the
                                :class:`Request`.
                            :param cookies: (optional) Dict or CookieJar object to send with the
                                :class:`Request`.
                            :param auth: (optional) Auth tuple or callable to enable
                                Basic/Digest/Custom HTTP Auth.
                            :param timeout: (optional) How long to wait for the server to send
                                data before giving up, as a float, or a :ref:`(connect timeout,
                                read timeout) <timeouts>` tuple.
                            :type timeout: float or tuple
                            :param allow_redirects: (optional) Set to True by default.
                            :type allow_redirects: bool
                            :param proxies: (optional) Dictionary mapping protocol or protocol and
                                hostname to the URL of the proxy.
                            :param stream: (optional) whether to immediately download the response
                                content. Defaults to ``False``.
                            :param verify: (optional) Either a boolean, in which case it controls whether we verify
                                the server's TLS certificate, or a string, in which case it must be a path
                                to a CA bundle to use. Defaults to ``True``.
                            :param cert: (optional) if String, path to ssl client cert file (.pem).
                                If Tuple, ('cert', 'key') pair.
                            """
        self.__currentResponse = self.__session.post(url=self.__baseUrl + url,
                                                     data=data,
                                                     json=json,
                                                     headers=headers,
                                                     params=params or {},
                                                     auth=auth,
                                                     cookies=cookies,
                                                     hooks=hooks,
                                                     timeout=timeout,
                                                     allow_redirects=allow_redirects,
                                                     stream=stream, cert=cert)
        return self

    def hitThePutRequest(self, url: str, params=None, data=None, json=None, headers=None, cookies=None,
                         auth=None, timeout=None, allow_redirects=True,
                         hooks=None, stream=None, cert=None):
        """Constructs a :method:`PUT Request <Request>`, prepares it and sends it.
                            Returns :class: stores response and returns `self` object.

                            :param url: URL for the new :class:`Request` object.
                            :param params: (optional) Dictionary or bytes to be sent in the query
                                string for the :class:`Request`.
                            :param data: (optional) Dictionary, list of tuples, bytes, or file-like
                                object to send in the body of the :class:`Request`.
                            :param json: (optional) json to send in the body of the
                                :class:`Request`.
                            :param headers: (optional) Dictionary of HTTP Headers to send with the
                                :class:`Request`.
                            :param cookies: (optional) Dict or CookieJar object to send with the
                                :class:`Request`.
                            :param auth: (optional) Auth tuple or callable to enable
                                Basic/Digest/Custom HTTP Auth.
                            :param timeout: (optional) How long to wait for the server to send
                                data before giving up, as a float, or a :ref:`(connect timeout,
                                read timeout) <timeouts>` tuple.
                            :type timeout: float or tuple
                            :param allow_redirects: (optional) Set to True by default.
                            :type allow_redirects: bool
                            :param proxies: (optional) Dictionary mapping protocol or protocol and
                                hostname to the URL of the proxy.
                            :param stream: (optional) whether to immediately download the response
                                content. Defaults to ``False``.
                            :param verify: (optional) Either a boolean, in which case it controls whether we verify
                                the server's TLS certificate, or a string, in which case it must be a path
                                to a CA bundle to use. Defaults to ``True``.
                            :param cert: (optional) if String, path to ssl client cert file (.pem).
                                If Tuple, ('cert', 'key') pair.
                            """
        self.__currentResponse = self.__session.put(url=self.__baseUrl + url,
                                                    data=data,
                                                    json=json,
                                                    headers=headers,
                                                    params=params or {},
                                                    auth=auth,
                                                    cookies=cookies,
                                                    hooks=hooks,
                                                    timeout=timeout,
                                                    allow_redirects=allow_redirects,
                                                    stream=stream, cert=cert)
        return self

    def hitThePatchRequest(self, url: str, params=None, data=None, json=None, headers=None, cookies=None,
                           auth=None, timeout=None, allow_redirects=True,
                           hooks=None, stream=None, cert=None):
        """Constructs a :method:`PATCH Request <Request>`, prepares it and sends it.
                            Returns :class: stores response and returns `self` object.

                            :param url: URL for the new :class:`Request` object.
                            :param params: (optional) Dictionary or bytes to be sent in the query
                                string for the :class:`Request`.
                            :param data: (optional) Dictionary, list of tuples, bytes, or file-like
                                object to send in the body of the :class:`Request`.
                            :param json: (optional) json to send in the body of the
                                :class:`Request`.
                            :param headers: (optional) Dictionary of HTTP Headers to send with the
                                :class:`Request`.
                            :param cookies: (optional) Dict or CookieJar object to send with the
                                :class:`Request`.
                            :param auth: (optional) Auth tuple or callable to enable
                                Basic/Digest/Custom HTTP Auth.
                            :param timeout: (optional) How long to wait for the server to send
                                data before giving up, as a float, or a :ref:`(connect timeout,
                                read timeout) <timeouts>` tuple.
                            :type timeout: float or tuple
                            :param allow_redirects: (optional) Set to True by default.
                            :type allow_redirects: bool
                            :param proxies: (optional) Dictionary mapping protocol or protocol and
                                hostname to the URL of the proxy.
                            :param stream: (optional) whether to immediately download the response
                                content. Defaults to ``False``.
                            :param verify: (optional) Either a boolean, in which case it controls whether we verify
                                the server's TLS certificate, or a string, in which case it must be a path
                                to a CA bundle to use. Defaults to ``True``.
                            :param cert: (optional) if String, path to ssl client cert file (.pem).
                                If Tuple, ('cert', 'key') pair.
                            """
        self.__currentResponse = self.__session.patch(url=self.__baseUrl + url,
                                                      data=data,
                                                      json=json,
                                                      headers=headers,
                                                      params=params or {},
                                                      auth=auth,
                                                      cookies=cookies,
                                                      hooks=hooks,
                                                      timeout=timeout,
                                                      allow_redirects=allow_redirects,
                                                      stream=stream, cert=cert)
        return self

    def hitTheDeleteRequest(self, url: str, params=None, data=None, json=None, headers=None, cookies=None,
                            auth=None, timeout=None, allow_redirects=True,
                            hooks=None, stream=None, cert=None):
        """Constructs a :method:`DELETE Request <Request>`, prepares it and sends it.
                            Returns :class: stores response and returns `self` object.

                            :param url: URL for the new :class:`Request` object.
                            :param params: (optional) Dictionary or bytes to be sent in the query
                                string for the :class:`Request`.
                            :param data: (optional) Dictionary, list of tuples, bytes, or file-like
                                object to send in the body of the :class:`Request`.
                            :param json: (optional) json to send in the body of the
                                :class:`Request`.
                            :param headers: (optional) Dictionary of HTTP Headers to send with the
                                :class:`Request`.
                            :param cookies: (optional) Dict or CookieJar object to send with the
                                :class:`Request`.
                            :param auth: (optional) Auth tuple or callable to enable
                                Basic/Digest/Custom HTTP Auth.
                            :param timeout: (optional) How long to wait for the server to send
                                data before giving up, as a float, or a :ref:`(connect timeout,
                                read timeout) <timeouts>` tuple.
                            :type timeout: float or tuple
                            :param allow_redirects: (optional) Set to True by default.
                            :type allow_redirects: bool
                            :param proxies: (optional) Dictionary mapping protocol or protocol and
                                hostname to the URL of the proxy.
                            :param stream: (optional) whether to immediately download the response
                                content. Defaults to ``False``.
                            :param verify: (optional) Either a boolean, in which case it controls whether we verify
                                the server's TLS certificate, or a string, in which case it must be a path
                                to a CA bundle to use. Defaults to ``True``.
                            :param cert: (optional) if String, path to ssl client cert file (.pem).
                                If Tuple, ('cert', 'key') pair.
                            """
        self.__currentResponse = self.__session.delete(url=self.__baseUrl + url,
                                                       data=data,
                                                       json=json,
                                                       headers=headers,
                                                       params=params or {},
                                                       auth=auth,
                                                       cookies=cookies,
                                                       hooks=hooks,
                                                       timeout=timeout,
                                                       allow_redirects=allow_redirects,
                                                       stream=stream, cert=cert)
        return self

    def hitTheOptionsRequest(self, url: str, params=None, data=None, json=None, headers=None, cookies=None,
                             auth=None, timeout=None, allow_redirects=True,
                             hooks=None, stream=None, cert=None):
        """Constructs a :method:`OPTIONS Request <Request>`, prepares it and sends it.
                            Returns :class: stores response and returns `self` object.

                            :param url: URL for the new :class:`Request` object.
                            :param params: (optional) Dictionary or bytes to be sent in the query
                                string for the :class:`Request`.
                            :param data: (optional) Dictionary, list of tuples, bytes, or file-like
                                object to send in the body of the :class:`Request`.
                            :param json: (optional) json to send in the body of the
                                :class:`Request`.
                            :param headers: (optional) Dictionary of HTTP Headers to send with the
                                :class:`Request`.
                            :param cookies: (optional) Dict or CookieJar object to send with the
                                :class:`Request`.
                            :param auth: (optional) Auth tuple or callable to enable
                                Basic/Digest/Custom HTTP Auth.
                            :param timeout: (optional) How long to wait for the server to send
                                data before giving up, as a float, or a :ref:`(connect timeout,
                                read timeout) <timeouts>` tuple.
                            :type timeout: float or tuple
                            :param allow_redirects: (optional) Set to True by default.
                            :type allow_redirects: bool
                            :param proxies: (optional) Dictionary mapping protocol or protocol and
                                hostname to the URL of the proxy.
                            :param stream: (optional) whether to immediately download the response
                                content. Defaults to ``False``.
                            :param verify: (optional) Either a boolean, in which case it controls whether we verify
                                the server's TLS certificate, or a string, in which case it must be a path
                                to a CA bundle to use. Defaults to ``True``.
                            :param cert: (optional) if String, path to ssl client cert file (.pem).
                                If Tuple, ('cert', 'key') pair.
                            """
        self.__currentResponse = self.__session.options(url=self.__baseUrl + url,
                                                        data=data,
                                                        json=json,
                                                        headers=headers,
                                                        params=params or {},
                                                        auth=auth,
                                                        cookies=cookies,
                                                        hooks=hooks,
                                                        timeout=timeout,
                                                        allow_redirects=allow_redirects,
                                                        stream=stream, cert=cert)
        return self

    def hitTheHeadRequest(self, url: str, params=None, data=None, json=None, headers=None, cookies=None,
                          auth=None, timeout=None, allow_redirects=True,
                          hooks=None, stream=None, cert=None):
        """Constructs a :method:`HEAD Request <Request>`, prepares it and sends it.
                            Returns :class: stores response and returns `self` object.

                            :param url: URL for the new :class:`Request` object.
                            :param params: (optional) Dictionary or bytes to be sent in the query
                                string for the :class:`Request`.
                            :param data: (optional) Dictionary, list of tuples, bytes, or file-like
                                object to send in the body of the :class:`Request`.
                            :param json: (optional) json to send in the body of the
                                :class:`Request`.
                            :param headers: (optional) Dictionary of HTTP Headers to send with the
                                :class:`Request`.
                            :param cookies: (optional) Dict or CookieJar object to send with the
                                :class:`Request`.
                            :param auth: (optional) Auth tuple or callable to enable
                                Basic/Digest/Custom HTTP Auth.
                            :param timeout: (optional) How long to wait for the server to send
                                data before giving up, as a float, or a :ref:`(connect timeout,
                                read timeout) <timeouts>` tuple.
                            :type timeout: float or tuple
                            :param allow_redirects: (optional) Set to True by default.
                            :type allow_redirects: bool
                            :param proxies: (optional) Dictionary mapping protocol or protocol and
                                hostname to the URL of the proxy.
                            :param stream: (optional) whether to immediately download the response
                                content. Defaults to ``False``.
                            :param verify: (optional) Either a boolean, in which case it controls whether we verify
                                the server's TLS certificate, or a string, in which case it must be a path
                                to a CA bundle to use. Defaults to ``True``.
                            :param cert: (optional) if String, path to ssl client cert file (.pem).
                                If Tuple, ('cert', 'key') pair.
                            """
        self.__currentResponse = self.__session.head(url=self.__baseUrl + url,
                                                     data=data,
                                                     json=json,
                                                     headers=headers,
                                                     params=params or {},
                                                     auth=auth,
                                                     cookies=cookies,
                                                     hooks=hooks,
                                                     timeout=timeout,
                                                     allow_redirects=allow_redirects,
                                                     stream=stream, cert=cert)
        return self

    def getCollectionVariableValue(self, variableName: str):
        return self.__collectionVariables[variableName]

    def setCollectionVariable(self, variableName: str, variableValue: str):
        self.__collectionVariables[variableName] = variableValue

    def SetValueFromResponseToTheCollectionVariale(self, variableName: str, responseDictPath: str):
        self.__collectionVariables[variableName] = self.__getDictValue(self.__currentResponse.json(),
                                                                       self.__cleanDictPath(responseDictPath))
        return self

    def getResponse(self):
        return self.__currentResponse

    def getStatusCode(self):
        return str(self.__currentResponse.status_code)

    def validateStatusCode(self, expectedStatusCode: str):
        """
        To validate the status code of the current response
        :param expectedStatusCode: str
        """
        self.getTestUtils().assertEqual(self.getStatusCode(), expectedStatusCode.strip(), msg="Status code mismatch")
        return self

    def validateStatusCodeIs200(self):
        """
        To verify whether the status code of the current response is 200
        """
        self.getTestUtils().assertEqual(self.getStatusCode(), '200', msg="Status code mismatch")
        return self

    def validateStatusCodeIs201(self):
        """
        To verify whether the status code of the current response is 201
        """
        self.getTestUtils().assertEqual(self.getStatusCode(), '201', msg="Status code mismatch")
        return self

    def validateStausCodeIsEither200Or201(self):
        """
        To verify whether the status code of the current response is 200 or 201
        """
        self.getTestUtils().assertIn(self.getStatusCode(), ['200', '201'],
                                     msg="Status code is not 200 or 201, actual status code - {}".format(
                                         self.getStatusCode()))
        return self

    def validateTheResponseValue(self, expectedValue, responseDictPath: str):
        """
        To validate whether the response has the expected value present in the provided dictionary path
        :param expectedValue: Any
        :param responseDictPath: str
        responseDictPath - Example ['data'][0]['firstName']
        """
        self.getTestUtils().assertEqual(
            self.__getDictValue(self.__currentResponse.json(), self.__cleanDictPath(responseDictPath)), expectedValue,
            msg="Response value mismatch")
        return self

    def validateIfListInTheResponseContainsItem(self, expectedValue, responseDictPath: str):
        """
        To validate whether the list in the response contains the provided item.
        :param expectedValue: Any
        :param responseDictPath: str
        responseDictPath - Example ['data'][0]['firstName']
        """
        responseList = list(self.__getDictValue(self.__currentResponse.json(), self.__cleanDictPath(responseDictPath)))
        i = 0
        isItemFound = False
        while i < len(responseList):
            if str(expectedValue) == str(responseList[i]):
                isItemFound = True
                break
            else:
                i += 1
                continue
        if isItemFound == False:
            self.getTestUtils().fail(
                "Expected item is not present in the response list\nExpected item - {}\nResponse list - {}".format(
                    expectedValue, responseList))
        return self

    def validateReponseBodyContainsText(self, expectedText):
        """
        To validate whether the response body contains the given text
        :param expectedText:
        """
        if expectedText not in self.__currentResponse.text:
            self.getTestUtils().fail(
                "Expected text is not present in the response body\nExpected text - {}\nResponse body - {}".format(
                    expectedText, self.__currentResponse.text))
        return self

    def closeSession(self):
        """
        To close the current session
        :return:
        """
        self.__session.close()

    def createNewSession(self):
        """
        Using this functions you can create a new session and terminate the existing session.
        """
        self.closeSession()
        self.__session = session()
        return self

    def __cleanDictPath(self, path):
        path = path.replace('[', '').replace("'", '').replace('"', "").split(']')
        if "" in path:
            path.remove("")
        cleanedPath = []
        for indice in path:
            if indice.isdigit() is True:
                cleanedPath.append(int(indice))
            else:
                cleanedPath.append(indice)
        return cleanedPath

    def __getDictValue(self, dictVariable, path):
        if len(path) == 0:
            return dictVariable
        else:
            return self.__getDictValue(dictVariable[path[0]], path[1:])

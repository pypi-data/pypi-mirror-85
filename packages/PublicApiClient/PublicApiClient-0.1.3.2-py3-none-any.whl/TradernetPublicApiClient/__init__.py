"""
Tradernet API PublicApiClient lib for Python 3
@link https://tradernet.ru/tradernet-api/public-api-client
"""

import time, hmac, hashlib, requests, json, urllib3

__version__ = '0.1.3.3'
__all__ = ['PublicApiClient']


class PublicApiClient:
    """
    Names of private variables start from: __
    """

    # API ver 1
    V1: int = 1
    # API ver 2
    V2: int = 2

    # by default https://tradernet.ru/api
    __apiUrl = str()

    # @link https://tradernet.ru/tradernet-api/auth-api
    __apiKey = str()
    __apiSecret = str()

    __version = int()
    __devMode: bool = False

    def __init__(self, apiKey=None, apiSecret=None, version=V1):
        """
        :param apiKey:
        :param apiSecret:
        :param version:
        """
        self.__apiUrl = 'https://tradernet.ru/api'
        self.__version = version
        self.__apiKey = apiKey
        self.__apiSecret = apiSecret

    def setApiUrl(self, _apiUrl):
        """
        Load URL different by default URL
        :param _apiUrl:
        :return:
        """
        self.__apiUrl = _apiUrl

    def isDevMode(self):
        """
        Develop mode
        :return:
        """
        self.__devMode = True

    def preSign(self, d):
        """
        preSign -- for api key's signature
        :param d:
        :return: string
        """

        s = ''
        for i in sorted(d):
            if type(d[i]) == dict:
                s += i + '=' + self.preSign(d[i]) + '&'
            else:
                s += i + '=' + str(d[i]) + '&'
        return s[:-1]

    def httpencode(self, d):
        """
        httpencode - Analog for PHP http_build_query function
        :param d:
        :return: string
        """
        s = ''
        for i in sorted(d):
            if type(d[i]) == dict:
                for into in d[i]:
                    if type(d[i][into]) == dict:
                        for subInto in d[i][into]:
                            if type(d[i][into][subInto]) == dict:
                                s += self.httpencode(d[i][into][subInto])
                            else:
                                s += i + '[' + into + ']' + '[' + subInto + ']=' + str(d[i][into][subInto]) + '&'
                    else:
                        s += i + '[' + into + ']=' + str(d[i][into]) + '&'
            else:
                s += i + '=' + str(d[i]) + '&'

        return s[:-1]

    def sendRequest(self, method, aParams=None, format='JSON'):
        """
        Send request
        :param method:
        :param aParams:
        :param format:
        :return: Responce
        """

        aReq = dict()
        aReq['cmd'] = method
        if aParams:
            aReq['params'] = aParams
        if (self.__version != self.V1) and (self.__apiKey):
            aReq['apiKey'] = self.__apiKey
        aReq['nonce'] = int(time.time() * 10000)

        preSig = self.preSign(aReq)
        Presig_Enc = self.httpencode(aReq)

        isVerify = True

        #  is local connect, ssl ignoring
        if self.__devMode == True:
            urllib3.disable_warnings()
            isVerify = False

        # Create signature for API V1 or V2
        if self.__version == self.V1:
            aReq['sig'] = hmac.new(key=self.__apiSecret.encode()).hexdigest()
            res = requests.post(self.__apiUrl, data={'q': json.dumps(aReq)}, verify=isVerify)
        else:
            apiheaders = {
                'X-NtApi-Sig': hmac.new(key=self.__apiSecret.encode(), msg=preSig.encode('utf-8'),
                                        digestmod=hashlib.sha256).hexdigest(),
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            self.__apiUrl += '/v2/cmd/' + method
            res = requests.post(self.__apiUrl, params=Presig_Enc, headers=apiheaders, data=Presig_Enc, verify=isVerify)

        return (res)

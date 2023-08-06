import requests
import re
import hashlib
import itertools
import string


class MyIP:
    def __call__(self, *args, **kwargs):
        url = "https://www.myip.com/"
        res = requests.get(url)
        r = re.findall('<span id="ip">(.*)</span>', res.text)
        if r:
            return r[0]


class Dict(dict):
    def __getattr__(self, item):
        pass


class DIC:
    def __init__(self, dictionary):
        self.dic = dictionary

    def __call__(self, *args, **kwargs):
        request_dict = self.dic
        get_var = Dict(request_dict)
        for key, value in get_var.items():
            setattr(get_var, key.lower(), value)
        return get_var


class isAlive:
    def __init__(self, url):
        self.url = url

    def __call__(self, *args, **kwargs):
        try:
            res = requests.get(self.url).status_code
        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError("No site connection, Please check the URL")
        except requests.exceptions.MissingSchema:
            raise requests.exceptions.MissingSchema("No site connection, Please check the URL")
        if res == 200:
            return "isAlive"


class Hash: # noqa
    def __init__(self, hash, regex=None, string_len=None, verbose=False): # noqa
        if not isinstance(hash, str):
            raise TypeError("'hash' only accepts a string (str)")
        else:
            self.hash = hash

        if string_len is None:
            self.sting_len_start = 1
            self.sting_len = 32
        else:
            try:
                self.sting_len = int(string_len)
                self.sting_len_start = int(string_len)
            except ValueError:
                raise ValueError("'string_len' only accepts a number (int|str)")
        self.ch = regex
        self.verbose = verbose
        self.regex = None

    def get_regex(self):
        self.ch = str(self.ch)
        if self.ch is None:
            self.ch = "3"
        if len(self.ch) == 1:
            if self.ch == "1":
                self.regex = "0123456789"
            elif self.ch == "2":
                self.regex = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            elif self.ch == "3":
                self.regex = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            elif self.ch == "4":
                self.regex = string.printable.replace(' \t\n\r\x0b\x0c', '')
            else:
                self.regex = self.ch
        else:
            self.regex = self.ch

    def recognize_crypt(self, v=False):
        if len(self.hash) == 32:
            if v:
                print("The hash is md5")
            return hashlib.md5()
        elif len(self.hash) == 40:
            if v:
                print("The hash is sha1")
            return hashlib.sha1()
        elif len(self.hash) == 64:
            if v:
                print("The hash is sha256")
            return hashlib.sha256()
        elif len(self.hash) == 128:
            if v:
                print("The hash is sha512")
            return hashlib.sha512()
        else:
            return "Check the hash again"

    def decrypt(self):
        self.get_regex()
        if self.verbose:
            self.recognize_crypt(True)
        for n in range(self.sting_len_start, self.sting_len+1):
            if self.verbose:
                print(f"String length - {n}")
            for xs in itertools.product(self.regex, repeat=n):
                saved = ''.join(xs)
                m = self.recognize_crypt()
                if m == "Check the hash again":
                    return m
                m.update(saved.encode())
                if self.hash == m.hexdigest():
                    return saved

    def encrypt(self, encryption="md5"):
        print(encryption)
        if encryption == "md5":
            return hashlib.md5(self.hash.encode()).hexdigest()
        elif encryption == "sha1":
            return hashlib.sha1(self.hash.encode()).hexdigest()
        elif encryption == "sha256":
            return hashlib.sha256(self.hash.encode()).hexdigest()
        elif encryption == "sha512":
            return hashlib.sha512(self.hash.encode()).hexdigest()
        else:
            return hashlib.md5(self.hash.encode()).hexdigest()


def isalive(url):
    return isAlive(url)()


def hash(hash, regex=None, string_len=None, verbose=False): # noqa
    return Hash(hash, regex, string_len, verbose)


def myip():
    return MyIP()()


def call_attr(dictionary):
    return DIC(dictionary)()

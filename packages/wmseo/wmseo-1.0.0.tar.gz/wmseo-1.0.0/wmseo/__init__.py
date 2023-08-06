'''
python setup.py sdist
python -m twine upload -u DanielBR08 -p DWhouse130_ --repository-url https://upload.pypi.org/legacy/ dist/*

'''

from google.oauth2 import service_account
from google.cloud import bigquery
import time
from datetime import datetime
import pandas as pd

def create_keyfile_dict_google_big_query_nestle_br():
    variables_keys = {
        "type": "service_account",
        "project_id": "nestle-br",
        "private_key_id": "351fb0b1ae372df2df0d0d5bdcf5647d3788ec5c",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCpXNvV0L9BNz0u\n/2tTY+QGMzVdSHDfpHw86Wy38t2cmhVt3+SQQcPh14GC+hOaus4ZpLqKS5etnrLL\nJ5sNurCWOnFufY2BAd++uUNzg/pOeJfKzHX1wpDZDY7w9wq0oenbHqsl6FiQN4wr\n7mD5Fr0w1ZP0RRrUmqPHg4t3TTLf2captdxBiUhWCn+tJrM8j7yod82UpERxYMbd\nWipOid3ajkaow8AGUXZvJiyKDMoOK9EKJBNI5zFxjKKhOlAJeW6gbOhSl74pA/Ui\n0ffXj/+T9hN7ixjU7v4NN1sHOvJXLgKd4E5SjS/jzi6jAPGgvnZD0FRvKPtPrsk6\na2DU/prFAgMBAAECggEAJoaVC2Jc3zztkg9QHrwOVsq3TOz5oCYOjNyceouolcMH\nNONFXvtWz7zyHRU9+GieEX9DX8oqSrha+5Oa1dit6r6IpxWwZrRCbWQ/T7up6MfN\n37f67VjBEl7fMTlBGi3qwImNbSYZX1UDccrcDE174+vxqBNAMzSqJOxrgUvyUrEc\ndoW63DL6+skob3KPkQdr3NUdNgmKvTA0oj6MR3Lehwk2Cm3Oh3YGLH8q7bp1bDo2\n9xplmkV0Pt0wJ5Cl0w3/036vA7efGaPB7ZCGKYiHwLAHKt7A1OrgBkBbVO++G6jn\nwWRVswO151RaqResfGtq+plWBFgptlwZp09UaIvVgQKBgQDc08VCquEVtADMMg3O\nP1RS7y5/4gxISs3+sOLfHIS8k5nMNhunHEq/K1T7DIcDe8IlB9ky0b1MARl24vIY\nv9pxstNLtTn+lhQtnmQ2m3/0ENNTgDoZdrzwN2v3lWmmspdKt/coN1ZBJR9Hqr8E\nMsyybDTdwZvffKviqVUq8g17eQKBgQDEVp+X1pLrKssSMO52VwZNSFi5I+GsfpSs\nhOGl5dwW32DH3Ymm8GebRAAMYiky6lbvGC44yWY60BuKuc24s2dNIUdq+xR6hVsl\nZBpw5y/TTfmbu78/L0lkSz6NDBtJ75zpCgn/Twy+D8PRYHxakrGwgZrEIQwCOqFd\nEEersD76rQKBgQCDbXKgzAzsmtZCsaOv1dc9COd26zV+LS9O3z4XpeSGS56kgKuS\nmO8Puh140Srl8tlIqtQlP9lXC+x46ndGLaE4PEMvcuvSTsYxpGxmZ8QOoZj0wINT\ntmya15FlqEJaGT6cFMN/5vdqDEsCn2fSet2Db41DUkCQEaZHX5q11ZwamQKBgFy9\nPe0OoZ8LO5iAHGMxf/yJK79nv3Um5TsIGT2vcWIsaR5++kIsVAP2/r7arvMp1Z5i\nIZMZLnyhSCEi2pVfyG+aRI23w1iMHR1wRz0FNoXs0vZInHFP+K6zC/y7tzgZQlih\nMU+zGyW7dJc1qAdwOxZQYbY6ld2HrCi1Q+VI/raRAoGBAMW5g8mJEkge1VtYjVuM\nqT4koPWJIi+8ufg0bQtak0HHu5siBi8gGie/mpayWmVZ+2JZGZxlzu3t/bX4Wagy\nQIHJv9cosvAbkvIYONe1JKoZbHEUoe2MdbjIVoOI6Fboc8xkpYx+o3ZVEfvQwm3/\niy+ANIN9Nn80o62441NoTGuD\n-----END PRIVATE KEY-----\n",
        "client_email": "analyst@nestle-br.iam.gserviceaccount.com",
        "client_id": "114418917477877634367",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/analyst%40nestle-br.iam.gserviceaccount.com"
    }
    return variables_keys

def connect_google_big_query():
    credentials_info = create_keyfile_dict_google_big_query_nestle_br()
    credentials = service_account.Credentials.from_service_account_info(credentials_info)

    client = bigquery.Client(
        credentials=credentials,
        project='nestle-br',
    )
    return client


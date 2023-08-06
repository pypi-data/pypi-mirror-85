# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)
import requests

from client.service import ZADServiceClient, ZADProfileClient
from client.auth import ZADAuthClient

client_id = 'amzn1.application-oa2-client.5f22ade077114ef980883e2045a2fde0'
client_secret = '1ac684981fd46f98752ac47929606cb1587a42ed1045de7f10a2391fd498769d'

access_token = 'Atza|IwEBIPaj4TplQ5xRZ8bhQLfqZh02LY_I1g3gfsAlHNCoQjkKQyFSj20ciylMOYX2kznmRndd2ZaizO7PnuoTCt-S10Cf3b5gB6yNa2ZvnxE-zkXZJ-b4dlLVBKmtlWhkhygqOQUI6yWdE8u1riVmCEOOFvVbL-EMBrpqyk7PNPqNSQxRsNKkjQ9T5WzkjiH2osxc8xLCY5P52ZNbRvDNftGkUqp4npQPkj20whrB7IjGckjpmq-Sqt6smR51S0U7jL_ZDSOv5bJSrpY1IQCL3s21fJ7egMsBcnAGbAlELy0uLf8hgpYpaIJGyfFOclSQ-odc8anNVqDU6wKAGsAuQMlID6R31A6SvYSc28SADjPY_2oz5iMe3JlnMRjNImFIYilArWL_g7hfxI2S7XsgKvBJQwjDIgfmM3QdPPbKf0qUSrhm7LQJKT0gF0DJl5QOuc0oYuY'

def auth():
    auth_client = ZADAuthClient(client_id, client_secret, 'NA')
    url = auth_client.authorization_url('http://localhost/', '{"xixi":"haha"}')
    print(url)

def refresh_access_token():
    refresh_token = "Atzr|IwEBIL6pWY6YvyQiuGLQxNh4OMsE9gy_vxWxAYvln2ioanTjNUVJNPmL33HpiFBbRuyD_Hy2kiVyi8HV-i5KzZ3w2-Ut_B-Y1d8pBotpYZY2zbITEN5gvshbZzB5WxieZIXZo3aHkMj1_UWV1u0SG0SJ7bEKGE78NdWZk1CwqGwWkHvcYwWQ2qdgMN6QI-4ij42GH9kmFNVtdHvmZJOWiLpD1i9NSw9P0hNNiCetEPc6bLW1TjodiyvB9epgyV5vvQ5Yc2r-Tx2eVeXFnY6D_PrONTLTbkxqIjvBQm3LoBZMgOhpGtBEC14JwKYhlyaQvzNU2Qd0xIymAgDwpcPLH_YWb26aOxUE-au-UgLU5bw88MvwMxutD9PkzPkIi6bSEdsddAI7n-FUk9VnWUavGDqO_7wGAaXmOICVJg32WjDw_V1wLjTahoaMxoCCQsaengF2YxI"
    auth_client = ZADAuthClient(client_id, client_secret, 'SANDBOX')
    res = auth_client.token.refresh_token(refresh_token)
    print(res)

def profile():
    client = ZADProfileClient(client_id, access_token, country="NA")
    a = client.profiles.list()
    print(a)

def test():
    client = ZADServiceClient(client_id, access_token, profile_id='3598230827470963', country="US", prepare_mode=False)
    a = client.sp_report.product_ads('20201020')
    print(a)

    # client = ZADServiceClient(client_id, access_token, profile_id='3598230827470963', country="US", prepare_mode=False)
    # a = client.sp_report.campaigns('20201003')
    # a = client.report_get.get_report('amzn1.clicksAPI.v1.p1.5F86B1EC.9f0e5b07-2bb9-4145-a0b4-855bb40f0e8b')
    # a = client.report_download.download_report('https://advertising-api.amazon.com/v1/reports/amzn1.clicksAPI.v1.p1.5F32458E.af87999a-31c6-4ab6-9ff9-e14edd0e810b/download')

    print(a)

profile()
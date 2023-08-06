# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)
import requests

from client.service import ZADServiceClient, ZADProfileClient
from client.auth import ZADAuthClient

client_id = 'amzn1.application-oa2-client.5f22ade077114ef980883e2045a2fde0'
client_secret = '1ac684981fd46f98752ac47929606cb1587a42ed1045de7f10a2391fd498769d'

# LW-US
access_token = 'Atza|IwEBIMDoMhwVHDPtmGbyMeBmfNVcNx7KJMuoBdclBrpruMdfm0II75QUJFPWZAUihMYm2nrbL9DQJaNWLgdepJIAaxeml97NQOkv4A8EbAqRQwoFJAQQEFNNl-NBW-FxEvnsYcCWqVauaVn8xFornF_Fym4xj7AfDjFi5J85txGgE9Xqc5YGB-c8FKuwN0sYLkpC0Xch5LYQoGG0OxY_X8dZunAQ0cDsPd5zKF4Bvu8tnTBgzQG_xh6etRauJuoKZoXjKZbU2yWVICT7X1XSuRFl-UmPu8GVQY3U27oRAzowATFI6LOnfwqabBHJkJ60B8_RwWA8qz1YCPbmMMbJBUXF5zOUrg26jnKcU5ZpJHMPULgTk9SqeqJ3ykHUMUMyv91YiPFVGd-LqtAssQgIqrZ4oJrlkIMdfFOUvARVCYasAzlcRBvqSnPxiYB3-HBw-VkAnPk'

# def auth():
#     auth_client = ZADAuthClient(client_id, client_secret, 'NA')
#     url = auth_client.authorization_url('http://localhost/', '{"xixi":"haha"}')
#     print(url)

def refresh_access_token():
    refresh_token = "Atzr|IwEBIGljpDbsnzcxBsjoiDhWXUJgvF-NW7bVXwjO3fGEHfGuNeuL1VMq3X9ghn86c1T3bDzdG2Xx6rto8Z66WpxD0nz4c8NkPIRlSj2u35IIkbmgnwm_RpLVIzQKGsDcSrNgh0uI5Z9aIxZKm7Yt-BgeQ0RQs56o6dUt6jL7g7HW2paR87Mxt-4JPoZvtqWwoL5DIGW9P5HjMDBoPvpr8yxTNe0EGmfolMHj7pmt8N5JTCHSpXUsNPwkGWRe4lny01rKlsyFYCW7MdYKbVIseKQgEInndrImB3dNBLKzL6FPmUgvACLVdaK1VA81OilI7ULXBKJfTb3MxW-UX3Rj2Ngeb1F1YmzcVhRV0ouT9MiNdlZ53zy90Qb9z0ZfagzjDTRgdC8bwt5X9JUBUVgri1jKOOeFyYSNmtjgd7Y8JGyddnVsB41-IE93OggOO5ZwoGBXIkQ"
    auth_client = ZADAuthClient(client_id, client_secret, 'NA')
    res = auth_client.token.refresh_token(refresh_token)
    print(res)

def profile():
    client = ZADProfileClient(client_id, access_token, country="NA")
    a = client.profiles.list()
    print(a)

def test():
    client = ZADServiceClient(client_id, access_token, profile_id='3843704771630076', country="US", prepare_mode=False)
    a = client.sp_report.queries('20201020')
    print(a)

    # client = ZADServiceClient(client_id, access_token, profile_id='3598230827470963', country="US", prepare_mode=False)
    # a = client.sp_report.campaigns('20201003')
    # a = client.report_get.get_report('amzn1.clicksAPI.v1.p1.5F86B1EC.9f0e5b07-2bb9-4145-a0b4-855bb40f0e8b')
    # a = client.report_download.download_report('https://advertising-api.amazon.com/v1/reports/amzn1.clicksAPI.v1.p1.5F32458E.af87999a-31c6-4ab6-9ff9-e14edd0e810b/download')

    print(a)

test()
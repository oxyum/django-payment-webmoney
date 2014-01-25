Django-Payment-WebMoney
=======================

WebMoney Merchant Interface support for Django.


How to configure WM
-------------------
1. Change your attestation from none to personal or higher
2. Configure payment settings on this page https://merchant.webmoney.ru/conf/purse.asp
3. Choose your purse & click to configure link
4. Edit the following fields: Result URL, Success URL, Fail URL
5. Save & enjoy

Fields urls example for wm-sample:
    Result URL = http://127.0.0.1:8000/webmoney/result/
    Success URL = http://127.0.0.1:8000/success/
    Fail URL = http://127.0.0.1:8000/fail/

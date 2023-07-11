import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import random

# put all headers here
curls = [
    "curl 'https://www.matchesfashion.com/ajax/headerdata' \
  -H 'authority: www.matchesfashion.com' \
  -H 'accept: */*' \
  -H 'accept-language: zh-TW,zh;q=0.9' \
  -H 'cookie: billingCurrency=HKD; country=HKG; indicativeCurrency=; language=en; plpView=productView; loggedIn=false; saleRegion=APAC; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; _gcl_au=1.1.865276343.1688703781; user_signin_state=anonymous; _pin_unauth=dWlkPU9ETXhOamcwTXpZdE5URTROaTAwTVRZNExUZ3lNV1l0WkdZM05EUTRNMlppT0RReQ; _gid=GA1.2.683742302.1688703782; _fbp=fb.1.1688703782084.1501310259; _tt_enable_cookie=1; _ttp=vsgNM-KvxglROOOIn0NEAOXUcTl; pxcts=f5b9c297-1c7d-11ee-9ab8-4c4a5a446169; _pxvid=f5b9b3fc-1c7d-11ee-9ab8-10baed70c686; sailthru_visitor=4b2ca74c-45d1-4958-a17c-5d8df1ea6c88; JSESSIONID=sc~F0A90565EC9BF02F94E9ABE8CA88BFED; defaultSizeTaxonomy=WOMENSHOESEUITSEARCH; sailthru_pageviews=2; _uetsid=f5cdc9b01c7d11eeb9587169d03aa33c; _uetvid=f5cde5401c7d11ee8df769ed9cbf615e; sailthru_content=59be34712042cbb79fd03e6274458b78; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+07+2023+14%3A18%3A20+GMT%2B0800+(%E9%A6%99%E6%B8%AF%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.34.0&isIABGlobal=false&hosts=&consentId=6cd7b740-144e-4f2e-9688-04a02bf4e2ab&interactionCount=0&landingPath=https%3A%2F%2Fwww.matchesfashion.com%2Fintl%2Fproducts%2FGinori-1735-X-Luke-Edward-Hall-Cotswold-scented-candle-320g-1511359&groups=C0002%3A0%2CC0004%3A0%2CC0001%3A1%2CC0003%3A0; _ga=GA1.2.2003679066.1688703782; AWSALBAPP-0=AAAAAAAAAACxnPmDz7MykYyaOi9PRfp1tLJ1eVq2MgQ0xMo/IGIZRZ2z4vasACW7lACEa6Czn3vlWvI4VKT1yvH5i7V0HM49gnkXJRgMOp+AEUYZIZPS9lh4gwlagedccuTQKJwR/24tjqQ=; _px3=20ae76f8baf044dd393bb29fe2bf4191962107a2fe788b31be0c8336fa319599:dKQ2VQ8Dw0IUv7DgU/WaBSf0PJZGON37SJt0LMII4sHmCAEWaP6u86IDbwyFm7FmXH+bJelucN7UxQxZMaykMA==:1000:1ka2DlhdChPDdk9EIXAZAedbSbQKFOO0MMg6GkA4/rrvJmx9pSKlvXTFd7LGQrI7dBQ3QmDpzh1udr3q6tcpDxHsY2xIyvqtnWOVHYdwR/1X4GlzWvz3XaJY6NfSSsJBnXoFmYjYp+UO3yoodoKTKHd24hPeU9LTQc2IbkM+fv5MGKbfGsn1hk9xcXCLoMSEaA/hr60Srcuok3goHirmyA==; _ga_K7BPDXYMDW=GS1.1.1688710695.2.1.1688711101.60.0.0; _pxde=6de12b13f5b69cc812439211c4e17db7071f6b842d5869a82dfd36983d6e68f7:eyJ0aW1lc3RhbXAiOjE2ODg3MTExMDA4ODgsImZfa2IiOjAsImlwY19pZCI6W119; _dd_s=rum=0&expire=1688712258782&logs=1&id=fb74d8b4-0bd7-4eb8-a68e-8990223bad50&created=1688710694487' \
  -H 'referer: https://www.matchesfashion.com/womens/shop/homeware/candles-and-home-fragrance?is=Candles%20and%20Home%20Fragrance' \
  -H 'sec-ch-ua: \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: \"Windows\"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
  --compressed",
    "curl 'https://www.matchesfashion.com/ajax/headerdata?_=1688718346988' \
      -H 'authority: www.matchesfashion.com' \
      -H 'accept: */*' \
      -H 'accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
      -H 'cache-control: no-store' \
      -H 'cookie: plpView=productView; pxcts=e3fb1c13-1c98-11ee-a279-4541426e464e; _pxvid=e3fb0cf3-1c98-11ee-a279-f5991535c648; gender=womens; loggedIn=false; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; JSESSIONID=sc~E4945E6D7C413E98AC7AB69F16CB3D00; _gcl_au=1.1.1954129303.1688715389; user_signin_state=anonymous; _gid=GA1.2.164560864.1688715390; _fbp=fb.1.1688715389836.1789779617; _tt_enable_cookie=1; _ttp=1xqdv3i8hr_Iu7Cef81Mi8R2Oku; _pin_unauth=dWlkPVlUUXhNekUzTTJZdE1EQXhPUzAwWW1GbExXRmtOMlV0WkRjNE1qVmhOV0psTldKag; sailthru_visitor=e00c8455-75b8-45ea-a0a1-fb5182afd40f; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_rf=1; _pxff_fp=1; SESSION_TID=LJSBABPQ26NNG-1LHC261; _gat_UA-4623109-1=1; __tmbid=sg-1688718321-d38961919a8141ac9c163e41df766e90; rskxRunCookie=0; rCookie=y24p8izh7t6dvz16r2jgeljsbadga; OptanonAlertBoxClosed=2023-07-07T08:25:27.725Z; country=HKG; language=en; saleRegion=APAC; billingCurrency=HKD; indicativeCurrency="
    "; _dd_s=rum=0&expire=1688719239519&logs=1&id=eb194266-68dd-4f5c-9fda-345479af8f02&created=1688718305773; fsm_uid=0444ffcc-4f7a-58ea-30d8-b74cc45f3e0a; fsm_sid=f2ea2e82-81eb-5d10-fc4b-489c9768b015; _uetsid=fcc758401c9811eebb1ee96f6f128af1; defaultSizeTaxonomy=WOMENSHOESEUITSEARCH; AWSALBAPP-0=AAAAAAAAAADdhKNVtFmC6QuYSPaXwZ7TSuKZRou5c6Rky8pSZKPxG2Peiw75CYqKMBe30gGlrSZXz/CVQJaW3JLRwZmT5hxjonQSWqXQDWy1lvfy0guyT08y3JjJWQZfYv67N3Ua59qj7Ok=; _uetvid=fcc786201c9811ee8cb66352d446560b; _ga_K7BPDXYMDW=GS1.1.1688715389.1.1.1688718340.41.0.0; _ga=GA1.1.1566256546.1688715390; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+07+2023+16%3A25%3A40+GMT%2B0800+(%E9%A6%99%E6%B8%AF%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.34.0&isIABGlobal=false&hosts=&consentId=3d622456-7a96-4121-bc01-c580ff4f273a&interactionCount=2&landingPath=NotLandingPage&groups=C0002%3A0%2CC0004%3A0%2CC0001%3A1%2CC0003%3A0&AwaitingReconsent=false&geolocation=HK%3BHCW; sailthru_pageviews=2; lastRskxRun=1688718341135; _px3=7ee28b9e23d1735e43ce4b0aa5b2e2d3138a0b2a510918e10b78f902289f373e:wUlrUJtBM1Ge1uSIbucwgj+v/Bb46JUYCKXCX7WhjuD1pcVF3kmGmICCpZ3QGKZBHigFeRyxs1I+hpqR5IDtCA==:1000:yVXBbqovdkylNRE4JjnYGdz3NGedk4RkDk6D+NnHn85GyEe/aFHZMVlgyKPg+NOmW38fALQ4ZpcuU6XdFQCg7wlRtDvQ4sfvEd8n+qWWOHhK3QJWdxAcWTJMTtZKMdqawDrU0kh0qlZjhg3ZyorEiqreV/0hyuXjMR9BIgDRnJ6t8cacMj9a1jjUhR/1t0jlMBaAjHwDqif+yu+JypP6Ew==; _pxde=6913e91b7be430b2d5e48f1c54c1c357b5518ca23a430a97985d036dbe6dc2c6:eyJ0aW1lc3RhbXAiOjE2ODg3MTgzNDQ5MzEsImZfa2IiOjAsImlwY19pZCI6W119' \
  -H 'referer: https://www.matchesfashion.com/intl/womens?is=Candles+and+Home+Fragrance' \
  -H 'sec-ch-ua: \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: \"Windows\"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest' \
  --compressed",
    "curl 'https://www.matchesfashion.com/ajax/headerdata?_=1688718683828' \
  -H 'authority: www.matchesfashion.com' \
  -H 'accept: */*' \
  -H 'accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cache-control: no-store' \
  -H 'cookie: plpView=productView; pxcts=e3fb1c13-1c98-11ee-a279-4541426e464e; _pxvid=e3fb0cf3-1c98-11ee-a279-f5991535c648; gender=womens; loggedIn=false; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; JSESSIONID=sc~E4945E6D7C413E98AC7AB69F16CB3D00; _gcl_au=1.1.1954129303.1688715389; user_signin_state=anonymous; _gid=GA1.2.164560864.1688715390; _fbp=fb.1.1688715389836.1789779617; _tt_enable_cookie=1; _ttp=1xqdv3i8hr_Iu7Cef81Mi8R2Oku; _pin_unauth=dWlkPVlUUXhNekUzTTJZdE1EQXhPUzAwWW1GbExXRmtOMlV0WkRjNE1qVmhOV0psTldKag; sailthru_visitor=e00c8455-75b8-45ea-a0a1-fb5182afd40f; SESSION_TID=LJSBABPQ26NNG-1LHC261; __tmbid=sg-1688718321-d38961919a8141ac9c163e41df766e90; rskxRunCookie=0; rCookie=y24p8izh7t6dvz16r2jgeljsbadga; OptanonAlertBoxClosed=2023-07-07T08:25:27.725Z; country=HKG; language=en; saleRegion=APAC; billingCurrency=HKD; indicativeCurrency="
    "; fsm_uid=0444ffcc-4f7a-58ea-30d8-b74cc45f3e0a; fsm_sid=f2ea2e82-81eb-5d10-fc4b-489c9768b015; defaultSizeTaxonomy=WOMENSHOESEUITSEARCH; signed-up-for-updates=true; _gat_UA-4623109-1=1; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_tm=1; _ga=GA1.1.1566256546.1688715390; _ga_K7BPDXYMDW=GS1.1.1688715389.1.1.1688718657.46.0.0; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+07+2023+16%3A31%3A12+GMT%2B0800+(%E9%A6%99%E6%B8%AF%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.34.0&isIABGlobal=false&hosts=&consentId=3d622456-7a96-4121-bc01-c580ff4f273a&interactionCount=2&landingPath=NotLandingPage&groups=C0002%3A0%2CC0004%3A0%2CC0001%3A1%2CC0003%3A0&AwaitingReconsent=false&geolocation=HK%3BHCW; AWSALBAPP-0=AAAAAAAAAACTYXN81iCLhB+ct+6V3tNvj/PXu5eTeIzltHTQbCqsF8ehUFub0j4iGE7XzSGTaE5DTjARhJXzBefxNuRfpWkYaFkpV6xZdsz6H0xUgwIGXlrKSMED0gVYt6STWsYZMad58Hc=; sailthru_pageviews=7; lastRskxRun=1688718674248; _px3=8b7f808be27671273109f64fe81d6c98b41e2c2b4b1f4ddeb42e66b91dd44072:O3bnLpiKw4TePrZz2KN/9uriF469PEa9qwuh7QdnwREQdbVkceLuvk0bMvSD7vubYBr6X0ZcPlLdqP2PjmfCnw==:1000:a5f+82K57mjMkCGl8asHL2GD775JGVBOQUiRkPtupIvbHFUx5Yoe4q0sxT0iGJRwaqBFkeoa6SfEWTPMULLKUFs1i1Ic9DYJ7w73S/vTxcdE32hJaTnuuCYDeU4o/JkNxEJVhtbiN1T3fEXvyfxHWP2UEt0HzkSDbtXZxamon+sZzUjpYPFI5KimDXjeSTVGLobvLPRxHimW+VrcmiTCQA==; _pxde=9a1dc79bf8f11b644b94182890f973f17e7b1c9fa45aa5d3ba9f83afd75e3d6f:eyJ0aW1lc3RhbXAiOjE2ODg3MTg2NzkyMDIsImZfa2IiOjAsImlwY19pZCI6W119; _dd_s=rum=0&expire=1688719583146&logs=1&id=eb194266-68dd-4f5c-9fda-345479af8f02&created=1688718305773; _uetsid=fcc758401c9811eebb1ee96f6f128af1; _uetvid=fcc786201c9811ee8cb66352d446560b' \
  -H 'referer: https://www.matchesfashion.com/intl/womens/lists/dressing-for-sun' \
  -H 'sec-ch-ua: \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: \"Windows\"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
  -H 'x-datadog-origin: rum' \
  -H 'x-datadog-parent-id: 8709913131846284751' \
  -H 'x-datadog-sampled: 1' \
  -H 'x-datadog-sampling-priority: 1' \
  -H 'x-datadog-trace-id: 7999885720884219672' \
  -H 'x-requested-with: XMLHttpRequest' \
  --compressed",
    "curl 'https://www.matchesfashion.com/ajax/headerdata' \
  -H 'authority: www.matchesfashion.com' \
  -H 'accept: */*' \
  -H 'accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cookie: plpView=productView; pxcts=e3fb1c13-1c98-11ee-a279-4541426e464e; _pxvid=e3fb0cf3-1c98-11ee-a279-f5991535c648; gender=womens; loggedIn=false; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; JSESSIONID=sc~E4945E6D7C413E98AC7AB69F16CB3D00; _gcl_au=1.1.1954129303.1688715389; user_signin_state=anonymous; _gid=GA1.2.164560864.1688715390; _fbp=fb.1.1688715389836.1789779617; _tt_enable_cookie=1; _ttp=1xqdv3i8hr_Iu7Cef81Mi8R2Oku; _pin_unauth=dWlkPVlUUXhNekUzTTJZdE1EQXhPUzAwWW1GbExXRmtOMlV0WkRjNE1qVmhOV0psTldKag; sailthru_visitor=e00c8455-75b8-45ea-a0a1-fb5182afd40f; SESSION_TID=LJSBABPQ26NNG-1LHC261; __tmbid=sg-1688718321-d38961919a8141ac9c163e41df766e90; rskxRunCookie=0; rCookie=y24p8izh7t6dvz16r2jgeljsbadga; OptanonAlertBoxClosed=2023-07-07T08:25:27.725Z; country=HKG; language=en; saleRegion=APAC; billingCurrency=HKD; indicativeCurrency="
    "; fsm_uid=0444ffcc-4f7a-58ea-30d8-b74cc45f3e0a; fsm_sid=f2ea2e82-81eb-5d10-fc4b-489c9768b015; defaultSizeTaxonomy=WOMENSHOESEUITSEARCH; signed-up-for-updates=true; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_tm=1; _gat_UA-4623109-1=1; lastRskxRun=1688718731944; _ga=GA1.1.1566256546.1688715390; _ga_K7BPDXYMDW=GS1.1.1688715389.1.1.1688718738.47.0.0; _uetsid=fcc758401c9811eebb1ee96f6f128af1; _uetvid=fcc786201c9811ee8cb66352d446560b; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+07+2023+16%3A32%3A19+GMT%2B0800+(%E9%A6%99%E6%B8%AF%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.34.0&isIABGlobal=false&hosts=&consentId=3d622456-7a96-4121-bc01-c580ff4f273a&interactionCount=2&landingPath=NotLandingPage&groups=C0002%3A0%2CC0004%3A0%2CC0001%3A1%2CC0003%3A0&AwaitingReconsent=false&geolocation=HK%3BHCW; AWSALBAPP-0=AAAAAAAAAABDioEmhs4PD0/WCtts2RLaps3dVegwcFo1bmLuif2u4FH9A+Fz8sKlkgUeL07FJEQ34GFG7QfaT9kKWdYGpotgFGPZDVQbhKW/8xCFEmbbBLdG40er0ofu20YAnAecpsZKm9w=; _px3=aa0adc9f323b04e161a78b19e2048e16bf06fd2cc75da6ee20d25896fa315b44:JyLvWwdt1z0nbiK/vHFVCpSMva+VEhJn7P6AFuvXe1YcSmkNf/zY4BzsdWq3/cPnlVKQrLsImyFo0LR5/GTq0g==:1000:hlRxJz9yEH+nK+0LypxoPy+mwmXK8lvO1o0+qGwZNTOahX07lNWe6Zem+oPE2carOksKs8ystITu3C//AeulXD9vSRCtziHFVu1USqdj/QXuWhmyj1R5BOPG4G+WhatkTPRkMHLC5TIQMTTxL8o8BXxHU8aj0uw3EQ75vmUGG7DOrIM7B24JsRWRslZ+/TolLK8Y4SYzp2jxWjC5b9jFnA==; sailthru_pageviews=11; _dd_s=rum=0&expire=1688719642714&logs=1&id=eb194266-68dd-4f5c-9fda-345479af8f02&created=1688718305773; _pxde=9c8d9aeef0407400dc941388795b7d1ce8d08f6736ec01ad8ecfb0b87d4e11ba:eyJ0aW1lc3RhbXAiOjE2ODg3MTg3NDIxMzMsImZfa2IiOjAsImlwY19pZCI6W119' \
  -H 'referer: https://www.matchesfashion.com/intl/search?text=candle&gender=womens' \
  -H 'sec-ch-ua: \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: \"Windows\"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
  --compressed",
    "curl 'https://www.matchesfashion.com/ajax/headerdata?_=1688718791370' \
      -H 'authority: www.matchesfashion.com' \
      -H 'accept: */*' \
      -H 'accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
      -H 'cache-control: no-store' \
      -H 'cookie: plpView=productView; pxcts=e3fb1c13-1c98-11ee-a279-4541426e464e; _pxvid=e3fb0cf3-1c98-11ee-a279-f5991535c648; gender=womens; loggedIn=false; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; JSESSIONID=sc~E4945E6D7C413E98AC7AB69F16CB3D00; _gcl_au=1.1.1954129303.1688715389; user_signin_state=anonymous; _gid=GA1.2.164560864.1688715390; _fbp=fb.1.1688715389836.1789779617; _tt_enable_cookie=1; _ttp=1xqdv3i8hr_Iu7Cef81Mi8R2Oku; _pin_unauth=dWlkPVlUUXhNekUzTTJZdE1EQXhPUzAwWW1GbExXRmtOMlV0WkRjNE1qVmhOV0psTldKag; sailthru_visitor=e00c8455-75b8-45ea-a0a1-fb5182afd40f; SESSION_TID=LJSBABPQ26NNG-1LHC261; __tmbid=sg-1688718321-d38961919a8141ac9c163e41df766e90; rskxRunCookie=0; rCookie=y24p8izh7t6dvz16r2jgeljsbadga; OptanonAlertBoxClosed=2023-07-07T08:25:27.725Z; country=HKG; language=en; saleRegion=APAC; billingCurrency=HKD; indicativeCurrency="
    "; fsm_uid=0444ffcc-4f7a-58ea-30d8-b74cc45f3e0a; fsm_sid=f2ea2e82-81eb-5d10-fc4b-489c9768b015; defaultSizeTaxonomy=WOMENSHOESEUITSEARCH; signed-up-for-updates=true; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_tm=1; lastRskxRun=1688718731944; sailthru_pageviews=12; _px3=1a68da6bcbcf925d9dc7920cc878fe797b89f73eec7dc679375e5ab30cd8bee8:ZeYcLkoHuZlRvYoPJ7gGWE1rQEcaDrB3QBTLPX6GFQ6a3NqmUOieTNMcVfm0d7NIuakzOszkk77gWczNX458oA==:1000:Igb1bBHJmvd+wdY4bmc23o3m8iu7CeQM+6d6DXZFe5S+JWuy6z7OHw3XWXrre+taBjO6O/XRg2u7hVwqG39aP65oco5TBsb3bVbjLWxPvI3SjdE9DGwx5TpRJWRQIi7qJ5gMaYuMFz5ikVqAb9EO5DtScN/YtNH86PlkASHqZjoAS0Je44hJs6U/F12Mm1KT800Pj54+Llkl7p+Q72mJTQ==; _gat_UA-4623109-1=1; AWSALBAPP-0=AAAAAAAAAADdwYk/qatQtFQKADafixvOAP2SSb34jU+A9ulZcwdEngm0+prpc9C7p6JHacfq2JI09nVU7v29rZdRkGZXPGZKJxL+aulH0WBxdne+ycZQEals9HBdUmSxglSEM02zCqFKbo8=; _uetsid=fcc758401c9811eebb1ee96f6f128af1; _uetvid=fcc786201c9811ee8cb66352d446560b; _ga_K7BPDXYMDW=GS1.1.1688715389.1.1.1688718789.59.0.0; _ga=GA1.1.1566256546.1688715390; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+07+2023+16%3A33%3A10+GMT%2B0800+(%E9%A6%99%E6%B8%AF%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.34.0&isIABGlobal=false&hosts=&consentId=3d622456-7a96-4121-bc01-c580ff4f273a&interactionCount=2&landingPath=NotLandingPage&groups=C0002%3A0%2CC0004%3A0%2CC0001%3A1%2CC0003%3A0&AwaitingReconsent=false&geolocation=HK%3BHCW; _pxde=d326e036748b0a0b742c3e1f8c7d41c11fbd33a70017ec74495c011345944f18:eyJ0aW1lc3RhbXAiOjE2ODg3MTg3ODkyNzUsImZfa2IiOjAsImlwY19pZCI6W119; _dd_s=rum=0&expire=1688719690881&logs=1&id=eb194266-68dd-4f5c-9fda-345479af8f02&created=1688718305773' \
  -H 'referer: https://www.matchesfashion.com/intl/womens/just-in/just-in-this-month' \
  -H 'sec-ch-ua: \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: \"Windows\"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
  -H 'x-datadog-origin: rum' \
  -H 'x-datadog-parent-id: 572277567263592385' \
  -H 'x-datadog-sampled: 1' \
  -H 'x-datadog-sampling-priority: 1' \
  -H 'x-datadog-trace-id: 2714652384529575143' \
  -H 'x-requested-with: XMLHttpRequest' \
  --compressed",
    "curl 'https://www.matchesfashion.com/ajax/headerdata?_=1688719413235' \
  -H 'authority: www.matchesfashion.com' \
  -H 'accept: */*' \
  -H 'accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cache-control: no-store' \
  -H 'cookie: plpView=productView; pxcts=e3fb1c13-1c98-11ee-a279-4541426e464e; _pxvid=e3fb0cf3-1c98-11ee-a279-f5991535c648; loggedIn=false; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; JSESSIONID=sc~E4945E6D7C413E98AC7AB69F16CB3D00; _gcl_au=1.1.1954129303.1688715389; user_signin_state=anonymous; _gid=GA1.2.164560864.1688715390; _fbp=fb.1.1688715389836.1789779617; _tt_enable_cookie=1; _ttp=1xqdv3i8hr_Iu7Cef81Mi8R2Oku; _pin_unauth=dWlkPVlUUXhNekUzTTJZdE1EQXhPUzAwWW1GbExXRmtOMlV0WkRjNE1qVmhOV0psTldKag; sailthru_visitor=e00c8455-75b8-45ea-a0a1-fb5182afd40f; SESSION_TID=LJSBABPQ26NNG-1LHC261; __tmbid=sg-1688718321-d38961919a8141ac9c163e41df766e90; rskxRunCookie=0; rCookie=y24p8izh7t6dvz16r2jgeljsbadga; OptanonAlertBoxClosed=2023-07-07T08:25:27.725Z; country=HKG; language=en; saleRegion=APAC; billingCurrency=HKD; indicativeCurrency="
    "; fsm_uid=0444ffcc-4f7a-58ea-30d8-b74cc45f3e0a; fsm_sid=f2ea2e82-81eb-5d10-fc4b-489c9768b015; defaultSizeTaxonomy=WOMENSHOESEUITSEARCH; signed-up-for-updates=true; _gat_UA-4623109-1=1; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_fp=1; lastRskxRun=1688719394121; _ga=GA1.1.1566256546.1688715390; _ga_K7BPDXYMDW=GS1.1.1688715389.1.1.1688719411.36.0.0; _uetsid=fcc758401c9811eebb1ee96f6f128af1; _uetvid=fcc786201c9811ee8cb66352d446560b; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+07+2023+16%3A43%3A32+GMT%2B0800+(%E9%A6%99%E6%B8%AF%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.34.0&isIABGlobal=false&hosts=&consentId=3d622456-7a96-4121-bc01-c580ff4f273a&interactionCount=2&landingPath=NotLandingPage&groups=C0002%3A0%2CC0004%3A0%2CC0001%3A1%2CC0003%3A0&AwaitingReconsent=false&geolocation=HK%3BHCW; _px3=2759ea571ad71c5c78de82da831e2d2b7dfd331a387cfff3eb6f8ab50193f803:MdzsvincDJjAZSOlLqsrSSEwpB1MAeCbbrlEk8Z6lDlGI3SNlmxMkq7pPXg7axYU/xPu+NkC7tBPByar21vd+w==:1000:hv/JE8mnmjzuADwZumhN6tahiK672FTvzfC+5XiRnxwAASWq9KFokBPw+p84A5Y8nOQ9aucRh/7WHp+Y4nkenn9G3m0hwj9M/PK3JX9egMPBwy1Cfri83TMHujhkqOTJD8I3FM+8CshT7CsxGm0SOVs86DWWQJq+zT0mDbQJ3jsS8QX3nxxhb8rhEKaMI+Q7z813Y59rEedB42dIiXdjsw==; _pxde=698c4bf1afe4aad1fd2cd6973130079a525d8485d3a07326a8171162af8fdda1:eyJ0aW1lc3RhbXAiOjE2ODg3MTk0MTEyMTUsImZfa2IiOjAsImlwY19pZCI6W119; sailthru_pageviews=17; AWSALBAPP-0=AAAAAAAAAADRmcJX5z/vA9SVHP533c+AfXK++npiey0Nb7F+FfXxf6Wi6XYdCzTuC9yjZOXHnFhsHrOEi1O6OFfdNViSLydsXpUg20i6aKJoP81spEZT3As3d/7K/AK4sht4uwbex/8bECQ=; gender=mens; _dd_s=rum=0&expire=1688720313181&logs=1&id=eb194266-68dd-4f5c-9fda-345479af8f02&created=1688718305773' \
  -H 'referer: https://www.matchesfashion.com/intl/mens' \
  -H 'sec-ch-ua: \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: \"Windows\"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
  -H 'x-datadog-origin: rum' \
  -H 'x-datadog-parent-id: 8634113360299317939' \
  -H 'x-datadog-sampled: 1' \
  -H 'x-datadog-sampling-priority: 1' \
  -H 'x-datadog-trace-id: 3517558680765415241' \
  -H 'x-requested-with: XMLHttpRequest' \
  --compressed",
    "curl 'https://www.matchesfashion.com/ajax/headerdata?_=1688719480973' \
  -H 'authority: www.matchesfashion.com' \
  -H 'accept: */*' \
  -H 'accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cache-control: no-store' \
  -H 'cookie: plpView=productView; pxcts=e3fb1c13-1c98-11ee-a279-4541426e464e; _pxvid=e3fb0cf3-1c98-11ee-a279-f5991535c648; loggedIn=false; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; JSESSIONID=sc~E4945E6D7C413E98AC7AB69F16CB3D00; _gcl_au=1.1.1954129303.1688715389; user_signin_state=anonymous; _gid=GA1.2.164560864.1688715390; _fbp=fb.1.1688715389836.1789779617; _tt_enable_cookie=1; _ttp=1xqdv3i8hr_Iu7Cef81Mi8R2Oku; _pin_unauth=dWlkPVlUUXhNekUzTTJZdE1EQXhPUzAwWW1GbExXRmtOMlV0WkRjNE1qVmhOV0psTldKag; sailthru_visitor=e00c8455-75b8-45ea-a0a1-fb5182afd40f; SESSION_TID=LJSBABPQ26NNG-1LHC261; __tmbid=sg-1688718321-d38961919a8141ac9c163e41df766e90; rskxRunCookie=0; rCookie=y24p8izh7t6dvz16r2jgeljsbadga; OptanonAlertBoxClosed=2023-07-07T08:25:27.725Z; country=HKG; language=en; saleRegion=APAC; billingCurrency=HKD; indicativeCurrency="
    "; fsm_uid=0444ffcc-4f7a-58ea-30d8-b74cc45f3e0a; fsm_sid=f2ea2e82-81eb-5d10-fc4b-489c9768b015; signed-up-for-updates=true; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; gender=mens; defaultSizeTaxonomy=MENSSHOESEUITSEARCH; lastRskxRun=1688719414499; _gat_UA-4623109-1=1; sailthru_content=64fefe8e43cf50b84c9e27a32f79b4c94e0704b273663ed7792e0864e197b85d; sailthru_pageviews=24; _uetsid=fcc758401c9811eebb1ee96f6f128af1; _uetvid=fcc786201c9811ee8cb66352d446560b; _ga=GA1.2.1566256546.1688715390; _ga_K7BPDXYMDW=GS1.1.1688715389.1.1.1688719478.31.0.0; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+07+2023+16%3A44%3A39+GMT%2B0800+(%E9%A6%99%E6%B8%AF%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.34.0&isIABGlobal=false&hosts=&consentId=3d622456-7a96-4121-bc01-c580ff4f273a&interactionCount=2&landingPath=NotLandingPage&groups=C0002%3A0%2CC0004%3A0%2CC0001%3A1%2CC0003%3A0&AwaitingReconsent=false&geolocation=HK%3BHCW; _px3=26d6c1566fccda6d1f49a4bb97a391a69de37b15bcf9671e34c6cc1b2c870255:19bRsDfQohusf/ru5+Joocr00x788bfoj9sMtAE8Y5+Kc28MkHOUrUbdwNg471cRChugFHO/tKk+N+QooUDVLA==:1000:ejb4fjq8UX8arsK51SInpQIkc8RYemf69OBEUuEFl2hjKJQK8AeBYyDNuihiCCetEbR3P/jKiru/J4Km8WvCA04yhGQxZvz7PG9tccaKrqIjKmyaolRQ2pcopreyMuKGNx2jaEhQpD7gpLZQdffk38iRImx+I8c/yG134GW24XBbtmSA7mnTYDfhr39NTB8QxNj45wK+lsxlXUVs6iRCaw==; _pxde=ad5a0260b4a0849c6aec97396e65bdb303447545d60089794974d5de388cf753:eyJ0aW1lc3RhbXAiOjE2ODg3MTk0Nzg5ODUsImZfa2IiOjAsImlwY19pZCI6W119; AWSALBAPP-0=AAAAAAAAAABcPrmSajt792g5iTGTzVmQ7x1ErMlrpOWXn6xhc9z4CP2h/4ZKFVKdV8vyg2NKAZFaJA7K8p2+2t5ZAjONIg9CdPh6yeMk2iy4dmHBxYznZTUB34eXap6e8B/aTnjlAAndtPg=; _dd_s=rum=0&expire=1688720380377&logs=1&id=eb194266-68dd-4f5c-9fda-345479af8f02&created=1688718305773' \
  -H 'referer: https://www.matchesfashion.com/intl/mens/lists/ss23-summer-style-heroes' \
  -H 'sec-ch-ua: \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: \"Windows\"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
  -H 'x-datadog-origin: rum' \
  -H 'x-datadog-parent-id: 7343599373057109417' \
  -H 'x-datadog-sampled: 1' \
  -H 'x-datadog-sampling-priority: 1' \
  -H 'x-datadog-trace-id: 68603899316785523' \
  -H 'x-requested-with: XMLHttpRequest' \
  --compressed",
    "curl 'https://www.matchesfashion.com/ajax/headerdata' \
  -H 'authority: www.matchesfashion.com' \
  -H 'accept: */*' \
  -H 'accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cookie: plpView=productView; pxcts=e3fb1c13-1c98-11ee-a279-4541426e464e; _pxvid=e3fb0cf3-1c98-11ee-a279-f5991535c648; loggedIn=false; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; JSESSIONID=sc~E4945E6D7C413E98AC7AB69F16CB3D00; _gcl_au=1.1.1954129303.1688715389; user_signin_state=anonymous; _gid=GA1.2.164560864.1688715390; _fbp=fb.1.1688715389836.1789779617; _tt_enable_cookie=1; _ttp=1xqdv3i8hr_Iu7Cef81Mi8R2Oku; _pin_unauth=dWlkPVlUUXhNekUzTTJZdE1EQXhPUzAwWW1GbExXRmtOMlV0WkRjNE1qVmhOV0psTldKag; sailthru_visitor=e00c8455-75b8-45ea-a0a1-fb5182afd40f; SESSION_TID=LJSBABPQ26NNG-1LHC261; __tmbid=sg-1688718321-d38961919a8141ac9c163e41df766e90; rskxRunCookie=0; rCookie=y24p8izh7t6dvz16r2jgeljsbadga; OptanonAlertBoxClosed=2023-07-07T08:25:27.725Z; country=HKG; language=en; saleRegion=APAC; billingCurrency=HKD; indicativeCurrency="
    "; fsm_uid=0444ffcc-4f7a-58ea-30d8-b74cc45f3e0a; fsm_sid=f2ea2e82-81eb-5d10-fc4b-489c9768b015; signed-up-for-updates=true; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; gender=mens; defaultSizeTaxonomy=MENSSHOESEUITSEARCH; sailthru_content=64fefe8e43cf50b84c9e27a32f79b4c94e0704b273663ed7792e0864e197b85d; sailthru_pageviews=25; lastRskxRun=1688719484118; _gat_UA-4623109-1=1; _px3=9d262ff1d604408c308fcd9e84b90e6d6160112f641e60fafc1677ecba5858ef:eZ+tcywmaJZELUaDK2AO4M3ODSnsu9/Nec9EbgiPG3NUZwp2mHdKyDyL4mramF0Y4/0JW2oXGZ88USuNWKHghA==:1000:d59wh2JbqXLL9l1EqTN5/MX0FVIV37Yodsp34wjbzwuwAo8LsBKH6OtfZzq/EjQHE3zVMSdO2r18ejrNs8Gup147ytC269Tcb2ykyvULhAhOIRvByzTHYSHnfaOtPb/b/W2s7dGFHF0XixRdx2HkIyLV1gA19Um8vhtzpGRkoXv0FCEbGAmoug47ewVL40YhBjNwHvawR+rHWGqiCrJ6Kw==; _pxde=d54e1d2aad9bafdb3bd9f6053a21fed827d0ef8217e03c48137f312fa47f3db3:eyJ0aW1lc3RhbXAiOjE2ODg3MTk1MzYwMzcsImZfa2IiOjAsImlwY19pZCI6W119; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+07+2023+16%3A45%3A41+GMT%2B0800+(%E9%A6%99%E6%B8%AF%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.34.0&isIABGlobal=false&hosts=&consentId=3d622456-7a96-4121-bc01-c580ff4f273a&interactionCount=2&landingPath=NotLandingPage&groups=C0002%3A0%2CC0004%3A0%2CC0001%3A1%2CC0003%3A0&AwaitingReconsent=false&geolocation=HK%3BHCW; AWSALBAPP-0=AAAAAAAAAAB0w/ipo3sAPY6Y6ITvLsiUGzKQ3VjEoBM1vhMMy5Xamo+C8s7+X835PidfSeVY0FRT+XKtEEoFTHwxV2vEwgIJGItuIRNF8jmWPt3/g3uMPFUwo20jD4+q16JpUp4PlKVKCQU=; _ga_K7BPDXYMDW=GS1.1.1688715389.1.1.1688719542.58.0.0; _ga=GA1.1.1566256546.1688715390; _uetsid=fcc758401c9811eebb1ee96f6f128af1; _uetvid=fcc786201c9811ee8cb66352d446560b; _dd_s=rum=0&expire=1688720442543&logs=1&id=eb194266-68dd-4f5c-9fda-345479af8f02&created=1688718305773' \
  -H 'referer: https://www.matchesfashion.com/intl/mens/shop/clothing' \
  -H 'sec-ch-ua: \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: \"Windows\"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
  --compressed",
    "curl 'https://www.matchesfashion.com/ajax/headerdata' \
  -H 'authority: www.matchesfashion.com' \
  -H 'accept: */*' \
  -H 'accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cookie: plpView=productView; pxcts=e3fb1c13-1c98-11ee-a279-4541426e464e; _pxvid=e3fb0cf3-1c98-11ee-a279-f5991535c648; loggedIn=false; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; JSESSIONID=sc~E4945E6D7C413E98AC7AB69F16CB3D00; _gcl_au=1.1.1954129303.1688715389; user_signin_state=anonymous; _gid=GA1.2.164560864.1688715390; _fbp=fb.1.1688715389836.1789779617; _tt_enable_cookie=1; _ttp=1xqdv3i8hr_Iu7Cef81Mi8R2Oku; _pin_unauth=dWlkPVlUUXhNekUzTTJZdE1EQXhPUzAwWW1GbExXRmtOMlV0WkRjNE1qVmhOV0psTldKag; sailthru_visitor=e00c8455-75b8-45ea-a0a1-fb5182afd40f; SESSION_TID=LJSBABPQ26NNG-1LHC261; __tmbid=sg-1688718321-d38961919a8141ac9c163e41df766e90; rskxRunCookie=0; rCookie=y24p8izh7t6dvz16r2jgeljsbadga; OptanonAlertBoxClosed=2023-07-07T08:25:27.725Z; country=HKG; language=en; saleRegion=APAC; billingCurrency=HKD; indicativeCurrency="
    "; fsm_uid=0444ffcc-4f7a-58ea-30d8-b74cc45f3e0a; fsm_sid=f2ea2e82-81eb-5d10-fc4b-489c9768b015; signed-up-for-updates=true; _pxff_tm=1; gender=womens; defaultSizeTaxonomy=WOMENSHOESEUITSEARCH; sailthru_content=64fefe8e43cf50b84c9e27a32f79b4c94e0704b273663ed7792e0864e197b85dc17a6999d5b6a09eb22a8071dd7e51b55635a73cc4e8601555b761474abdd78e; lastRskxRun=1688719609941; _px3=2d6ecad247c1fcc1cedacd80bf4d82b01f678d555a6b3beab8cd4d836dfffaed:iUJhIh8VKCgxtjj265LHXcoYpR0K6h+iDBUQAhJyD05YLSi96psVEY0FwSLI/kDwgBzfLAFIvjUpovQE5fpPJw==:1000:gj63kQ8QYAK+Tixp2Ltg++FN8TK7M6FmtiGS4cKPZW6GqlIiPu69NLNPM+B2uHOqL6NcNgxztX2RxposPLATlN+mYMG7niVuQmlZ1nhQZ/Ats/lJ61s/bFnNEDKzM0qpksaSMl45g1hvkGzbdt1xN+gsXvIPWBUYCOL15A0yPa/nXvNu0YdBGCb/2EYlnyli1k2hUK84eEqeahMj+OsrXQ==; _pxde=e56040e5dd1a255a1e17543eea33cfafe2a1d7fce692118eddd60d3e7fa9bd22:eyJ0aW1lc3RhbXAiOjE2ODg3MTk2NjQzMjEsImZfa2IiOjAsImlwY19pZCI6W119; _gat_UA-4623109-1=1; _dd_s=rum=0&expire=1688720569782&logs=1&id=eb194266-68dd-4f5c-9fda-345479af8f02&created=1688718305773; _ga_K7BPDXYMDW=GS1.1.1688715389.1.1.1688719670.60.0.0; sailthru_pageviews=32; _uetsid=fcc758401c9811eebb1ee96f6f128af1; _uetvid=fcc786201c9811ee8cb66352d446560b; _ga=GA1.2.1566256546.1688715390; AWSALBAPP-0=AAAAAAAAAACY9hI4q9GlJ0CRn3EdgI7aI2dS7xEul/BR7ZS0zF5RKanI4COa8Z2rK7laFtTIjTjQ6qpPjrTApHL+xiND7DtIsxE7Q3ABw2VQ+G7wGwiRcQ1I7CssGW/7O4YTUXn0fORykNo=; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+07+2023+16%3A47%3A50+GMT%2B0800+(%E9%A6%99%E6%B8%AF%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.34.0&isIABGlobal=false&hosts=&consentId=3d622456-7a96-4121-bc01-c580ff4f273a&interactionCount=2&landingPath=NotLandingPage&groups=C0002%3A0%2CC0004%3A0%2CC0001%3A1%2CC0003%3A0&AwaitingReconsent=false&geolocation=HK%3BHCW' \
  -H 'referer: https://www.matchesfashion.com/intl/womens/shop/accessories/fine-jewellery' \
  -H 'sec-ch-ua: \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: \"Windows\"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
  --compressed",
    "curl 'https://www.matchesfashion.com/ajax/headerdata?_=1688719716863' \
  -H 'authority: www.matchesfashion.com' \
  -H 'accept: */*' \
  -H 'accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cache-control: no-store' \
  -H 'cookie: plpView=productView; pxcts=e3fb1c13-1c98-11ee-a279-4541426e464e; _pxvid=e3fb0cf3-1c98-11ee-a279-f5991535c648; loggedIn=false; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; JSESSIONID=sc~E4945E6D7C413E98AC7AB69F16CB3D00; _gcl_au=1.1.1954129303.1688715389; user_signin_state=anonymous; _gid=GA1.2.164560864.1688715390; _fbp=fb.1.1688715389836.1789779617; _tt_enable_cookie=1; _ttp=1xqdv3i8hr_Iu7Cef81Mi8R2Oku; _pin_unauth=dWlkPVlUUXhNekUzTTJZdE1EQXhPUzAwWW1GbExXRmtOMlV0WkRjNE1qVmhOV0psTldKag; sailthru_visitor=e00c8455-75b8-45ea-a0a1-fb5182afd40f; SESSION_TID=LJSBABPQ26NNG-1LHC261; __tmbid=sg-1688718321-d38961919a8141ac9c163e41df766e90; rskxRunCookie=0; rCookie=y24p8izh7t6dvz16r2jgeljsbadga; OptanonAlertBoxClosed=2023-07-07T08:25:27.725Z; country=HKG; language=en; saleRegion=APAC; billingCurrency=HKD; indicativeCurrency="
    "; fsm_uid=0444ffcc-4f7a-58ea-30d8-b74cc45f3e0a; fsm_sid=f2ea2e82-81eb-5d10-fc4b-489c9768b015; signed-up-for-updates=true; _pxff_tm=1; gender=womens; defaultSizeTaxonomy=WOMENSHOESEUITSEARCH; sailthru_content=64fefe8e43cf50b84c9e27a32f79b4c94e0704b273663ed7792e0864e197b85dc17a6999d5b6a09eb22a8071dd7e51b55635a73cc4e8601555b761474abdd78e; lastRskxRun=1688719609941; _gat_UA-4623109-1=1; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; sailthru_pageviews=33; _px3=ffd042550788207d9b8f232343e87974ca2dd2d678ee17355494a52bf8397f76:OcRycfCd4PRa7z4OesKMrZPhCYlz2qwr5TNHPyGFXPNFccqZDBzSRxY2Uvpw639mFy0dETR04pTqHgAur8ND6w==:1000:t6oJ92I6RmoT6+P+kPCYkU8f8cfnBtPp9y/JQe90FunF/OJiWiTSWEAxyt+xsVlW+ZLyfIirsUuAQ+6ICQBZEM4SxwdnvktroaWsrvbuUdkxF4kpxgZZWYzPG2ITFKteq3hvekvypQBe77kHYAcLtnGFduOfZUbPnCoKtZybbUeQkTxG5AWB11C99nBS1Fg5EjaHXkjkbTGrlCEKV58APg==; _ga_K7BPDXYMDW=GS1.1.1688715389.1.1.1688719706.24.0.0; _ga=GA1.2.1566256546.1688715390; _pxde=79f90dfd6a75dba1352e337211366d7dab5e2e0d6b19d526b0b066cc2fecc8b3:eyJ0aW1lc3RhbXAiOjE2ODg3MTk3MDY0NjgsImZfa2IiOjAsImlwY19pZCI6W119; _uetsid=fcc758401c9811eebb1ee96f6f128af1; _uetvid=fcc786201c9811ee8cb66352d446560b; AWSALBAPP-0=AAAAAAAAAADCJIJAhh8VXSjcJRLcWcAkJpPL1NrtkPaS1asSfHEpdoII5ScedxXL1jqzAC9KZR3z01tZKN12FQK/eURcbHneKM0c1L9NsAN2BGXkPvYo+AKKiJIXcwaX0fgJIifc/S8B9tU=; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+07+2023+16%3A48%3A36+GMT%2B0800+(%E9%A6%99%E6%B8%AF%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.34.0&isIABGlobal=false&hosts=&consentId=3d622456-7a96-4121-bc01-c580ff4f273a&interactionCount=2&landingPath=NotLandingPage&groups=C0002%3A0%2CC0004%3A0%2CC0001%3A1%2CC0003%3A0&AwaitingReconsent=false&geolocation=HK%3BHCW; _dd_s=rum=0&expire=1688720616692&logs=1&id=eb194266-68dd-4f5c-9fda-345479af8f02&created=1688718305773' \
  -H 'referer: https://www.matchesfashion.com/intl/womens' \
  -H 'sec-ch-ua: \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: \"Windows\"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
  -H 'x-datadog-origin: rum' \
  -H 'x-datadog-parent-id: 952373154600872447' \
  -H 'x-datadog-sampled: 1' \
  -H 'x-datadog-sampling-priority: 1' \
  -H 'x-datadog-trace-id: 5977958938612266896' \
  -H 'x-requested-with: XMLHttpRequest' \
  --compressed",
]


def get_product_links(url):
    # request header
    curl = "curl 'https://www.matchesfashion.com/ajax/headerdata' \
      -H 'authority: www.matchesfashion.com' \
      -H 'accept: */*' \
      -H 'accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
      -H 'cookie: billingCurrency=GBP; country=GBR; indicativeCurrency=; plpView=productView; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; pxcts=e3fb1c13-1c98-11ee-a279-4541426e464e; _pxvid=e3fb0cf3-1c98-11ee-a279-f5991535c648; _pxff_rf=1; _pxff_fp=1; _pxff_tm=1; gender=womens; loggedIn=false; saleRegion=ROW; defaultSizeTaxonomy=WOMENSSHOESUKSEARCH; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; JSESSIONID=sc~E4945E6D7C413E98AC7AB69F16CB3D00; language=en_GB; _gcl_au=1.1.1954129303.1688715389; user_signin_state=anonymous; _uetsid=fcc758401c9811eebb1ee96f6f128af1; _uetvid=fcc786201c9811ee8cb66352d446560b; _gid=GA1.2.164560864.1688715390; _gat_UA-4623109-1=1; _fbp=fb.1.1688715389836.1789779617; _tt_enable_cookie=1; _ttp=1xqdv3i8hr_Iu7Cef81Mi8R2Oku; _pin_unauth=dWlkPVlUUXhNekUzTTJZdE1EQXhPUzAwWW1GbExXRmtOMlV0WkRjNE1qVmhOV0psTldKag; AWSALBAPP-0=AAAAAAAAAADKttwZ9mAKUmbvMCWNhT7PUZrWvS99kl69iq9pLjhGzkExihXgMnGMnLB0IZKdspoUlLGao+YTOuBqpJ1KcZ6nXCuqLfHC4DlyCYSY+B+YCPZoMaQLaenNJsyDYYU0zfL9hdw=; sailthru_pageviews=1; _px3=b0bd2ea845c9434bad2bea2cece96bd7c99483da34836f695ef3229c729043c9:USlNnlZfsRyX0Gs31PFtmPg6VxNdpiGSD9m+/pDZd5CnQzmCgH0KUBEvnlF9CcIghIc8NxLjf4NsoSEOyDPk/Q==:1000:tU0bT4umcLi5Yejn8ORQpj5Oqe2W+9y5EE1wZ1hnVMqK8YlFmyMEzZkWSKKgwX4+EykjLyRxpfhyogNszYSe3DZLiU58nfcYj/BXnM04RSakBdFsc8oHHagpPwowsCQvAjND3rJabp5qpvLwa2y8krFt9ViBg76Ihc76r4ECLnOLF22MHFG4ylgNMhXiWtvccwYLqVVT90JOxiJKCIOhhA==; _ga=GA1.2.1566256546.1688715390; sailthru_visitor=e00c8455-75b8-45ea-a0a1-fb5182afd40f; _pxde=8e2af7a562d73595afb89c22fb7bcaa5dda0497e8422a83e9f604760f4e8269a:eyJ0aW1lc3RhbXAiOjE2ODg3MTU0MTAwNjUsImZfa2IiOjAsImlwY19pZCI6W119; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+07+2023+15%3A36%3A56+GMT%2B0800+(%E9%A6%99%E6%B8%AF%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.34.0&isIABGlobal=false&hosts=&consentId=3d622456-7a96-4121-bc01-c580ff4f273a&interactionCount=1&landingPath=https%3A%2F%2Fwww.matchesfashion.com%2Fwomens%2Fshop%2Fhomeware%2Fcandles-and-home-fragrance%3Fis%3DCandles%2520and%2520Home%2520Fragrance&groups=C0002%3A0%2CC0004%3A0%2CC0001%3A1%2CC0003%3A0; _dd_s=rum=0&expire=1688716302701&logs=1&id=66ef0c28-aa80-401f-8f51-c9c63837da35&created=1688715388691; _ga_K7BPDXYMDW=GS1.1.1688715389.1.1.1688715418.31.0.0' \
      -H 'referer: https://www.matchesfashion.com/womens/shop/homeware/candles-and-home-fragrance?is=Candles%20and%20Home%20Fragrance' \
      -H 'sec-ch-ua: \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"' \
      -H 'sec-ch-ua-mobile: ?0' \
      -H 'sec-ch-ua-platform: \"Windows\"' \
      -H 'sec-fetch-dest: empty' \
      -H 'sec-fetch-mode: cors' \
      -H 'sec-fetch-site: same-origin' \
      -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
      --compressed"

    header_pattern = re.compile(r"-H '(.+?): (.+?)'")
    headers = {
        match.group(1): match.group(2) for match in header_pattern.finditer(curl)
    }

    options = webdriver.ChromeOptions()

    for key, value in headers.items():
        options.add_argument(f"--header={key}:{value}")

    driver = webdriver.Chrome(options=options)

    # Navigate to Url
    driver.get(url)

    while True:
        try:
            wait = WebDriverWait(driver, 10)
            button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'Load More')]")
                )
            )
            button.click()
        except TimeoutException:
            break
    print("Loaded all product links")

    # Get all the elements available with tag name 'p'
    products_links = []
    links = driver.find_elements(By.TAG_NAME, "a")

    for link in links:
        href = link.get_attribute("href")
        if href is not None:
            if "www.matchesfashion.com/products" in href:
                products_links.append(href)

    driver.quit()
    return products_links


def get_product_data(url, curl) -> dict:
    header_pattern = re.compile(r"-H '(.+?): (.+?)'")
    headers = {
        match.group(1): match.group(2) for match in header_pattern.finditer(curl)
    }

    response = requests.get(url, headers=headers)

    row = {"product_id": url[-7:]}
    print(response.status_code)
    # check if the request was successful
    if response.status_code == 200:
        # save the response to a text file
        soup = BeautifulSoup(response.content, "html.parser")

        brand = soup.find(
            "a",
            {
                "class": "chakra-link css-1ti2pbg",
                "data-testid": "ProductMainDescription-designer-link",
            },
        )
        if brand is not None:
            row["brand"] = brand.text

        product_name = soup.find(
            "span",
            {
                "class": "chakra-text css-uyrcxy",
                "data-testid": "ProductMainDescription-name",
            },
        )
        if product_name is not None:
            row["product_name"] = product_name.text

        price = soup.find(
            "span",
            {
                "class": "chakra-text css-k1gaaj",
                "data-testid": "ProductPrice-billing-price",
            },
        )
        if price is not None:
            row["price"] = int(price.text.replace("HK$", "").replace(",", ""))
        else:
            price = soup.find(
                "span",
                {
                    "class": "chakra-text css-1conpqb",
                    "data-testid": "ProductPrice-billing-price",
                },
            )
            if price is not None:
                row["price"] = int(price.text.replace("HK$", "").replace(",", ""))

        description = soup.find(
            "span",
            {"class": "css-cet0rr", "data-testid": "ProductsCarousel-description-text"},
        )
        if description is not None:
            row["description"] = description.text

        details = soup.find("ul", {"role": "list", "class": "css-6r7l9g"})
        if details is not None:
            row["details"] = details

        size_and_fit = soup.find("ul", {"role": "list", "class": "css-1pngbph"})
        if size_and_fit is not None:
            row["size_and_fit"] = size_and_fit

    return row


def scrape(category_url, time_min=10, time_max=15):
    product_links = get_product_links(category_url)
    df = pd.DataFrame(
        columns=[
            "product_id",
            "brand",
            "product_name",
            "price",
            "description",
            "details",
            "size_and_fit",
        ]
    )
    for l in product_links:
        row = get_product_data(l, curls[random.randint(0, len(curls) - 1)])
        df.loc[len(df.index)] = row
        time.sleep(random.uniform(time_min, time_max))
    return df


if __name__ == "__main__":
    category_url = "https://www.matchesfashion.com/womens/shop/homeware/candles-and-home-fragrance?is=Candles%20and%20Home%20Fragrance"
    result = scrape(category_url)

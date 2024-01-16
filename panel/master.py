import requests


def get_irancell_price(internet=50, call=50, sms=50, period=1):
    url = 'https://my.irancell.ir/myirancellapi/boom/calculateBoomPrice'
    body = {
        "gUnits": internet,
         "vUnits": call, 
         "sUnits": sms,
          "validityDays": period,
           "type": "TCB"
    }
    headers = {
        "Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uaWQiOiJiYTVmYmM0MC04MzYzLTExZWMtYWQ5YS03NTYzNzk3ZTBkMzctNDA1Ny43MDY3NzcyNTc5MjEiLCJwcm9maWxlIjp7Ik1TSVNETiI6Ijk4OTA1NTkwMTM4NSIsInN1YnNjcmliZXJUeXBlIjoiMSIsImZOYW1lIjoi2LPZitmG2KciLCJmYXRoZXJzTmFtZSI6Iti12YrZgdmI2LHZiiDYt9i62LEg2KfZhNis2LHYr9mKIiwiU0lNVHlwZSI6IlVTSU0iLCJhY2NvdW50VHlwZSI6IkIiLCJhY2NvdW50TGlua0NvZGUiOiI4MTUxNjk2NDU3Iiwic2VydmljZSI6MSwiU1VMVG9rZW4iOiIxMWY5NDA4NzJkZmY0NWE2ODZhZTIwYzk3Mjk0NTgzNSIsInN0YXRlIjoiYjAwMGIxODBlYjExOTVmZjI4N2IyYjdkMTJhNjRkMjMiLCJsYXN0VXBkYXRlIjoxNjQzNzIyNDg5MzQ4fSwiaWF0IjoxNjQzNzIyNDg5LCJleHAiOjI2NDM3MjI0ODl9.NG7LbPZhp5mm1BUA0HAdp3OjmosadjciMigF_kiVLKM"
    }
    response = requests.post(
        url=url,
        headers=headers,
        data=body
    )
    print(response.json())
    return response.json()['data']['TotalDiscountedPrice']

def get_hamrah_dataset():
    url = "https://chr724.ir/services/v3/EasyCharge/initializeData"
    
    response = requests.get(
        url=url
        )
    return dict(response.json())['products']['internetPackage']




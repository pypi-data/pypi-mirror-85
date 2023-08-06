**CAKE API:**   
Using this module you can create a API collection and it also has lots of utilities to validate the response, status code, store a value in collection variable etc.

**INSTALLATION:**   
>pip install CakeApi

**USAGE:**   
_from CakeApi.CakeApiUtilities import CreateApiCollection_

_demoApiCollection = CreateApiCollection(baseUrl="https://reqres.in/")  
demoApiCollection.hitTheGetRequest(url="/api/users?page=2").validateStatusCodeIs200()\\\
&nbsp;&nbsp;&nbsp;&nbsp;.validateTheResponseValue(expectedValue="Michael", responseDictPath="['data'][0]['first_name']")\\\
&nbsp;&nbsp;&nbsp;&nbsp;.hitThePostRequest(url="/api/users", data=dict(name="morpheus", job="leader")).validateStatusCodeIs201()\\\
&nbsp;&nbsp;&nbsp;&nbsp;.validateTheResponseValue(expectedValue="leader", responseDictPath="['job']")_

>Note: Refer the function comments, to get a better idea on the usage.

**CONTACT:**   
Contact me for collabration.
>Email - krishnaForTestAutomation@gmail.com

>LinkedIn - https://www.linkedin.com/in/krishna-kumar-859a73134
  
**LICENSE:**   
© 2020 Krishna Kumar Viswanathan   
This repository is licensed under the MIT license
See LICENSE for details.
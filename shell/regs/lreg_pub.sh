#curl -ik -X GET "https://localhost:8443/api/0.1.0/register" -H 'apikey: d1fd0ddee6b94d048f4bbb4a854ce56b' -H 'resourceID: iiot_pub3' -H 'serviceType: publish' > ../responses/response_reg_pub.txt
curl -ikv -X GET "https://localhost:8443/api/0.1.0/register" -H 'apikey: d1fd0ddee6b94d048f4bbb4a854ce56b' -H "resourceID: 123" -H 'serviceType: publish'

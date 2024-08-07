# How to Access the Bridgehead API

To upload data to the Bridgehead, you need a username and password provided by the administrator at the University of Heidelberg. The required API endpoint will be the IP address of your assigned service, combined with the entry point `/send` and the name of the location service. The request must be a POST request.

For example, if the service IP is `https://81.89.199.xxx` and the location service name is `receiver.gki-service`, the endpoint URL will be:

```
https://81.89.199.xxx/send/receiver.gki-service
```

An example curl command to make this request is as follows:

```sh
curl --request POST \
  --url https://81.89.199.xxx/send/receiver.gki-service \
  --header 'Authorization: Basic xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
  --header 'Content-Type: application/json' \
  --header 'filename: example.json' \
  --data '{
	"content": "File content"
}'
```

In this command, the `Authorization: Basic` header contains the base64-encoded username and password for accessing the location service. After executing the POST request, the file will be uploaded to the UNIHD Server via the Bridgehead.
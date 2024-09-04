# Tutorial: Sending Files

If your location is registered with the LeMeDaRT Project, you will gain access to a dedicated service endpoint. This endpoint allows you to send files via an API, accessible through a URL similar to `https://81.89.199.137/send/receiver.gki-service`. This POST request enables the upload of files associated with a specific patient's TTPID.

## POST Request

To successfully upload a file, the POST request must include both the file and a correctly structured filename in the header. The filename should follow this format: `<filename>-ttpid-lemedart-<ttpid>.<filetype>`. Please note that `<filename>` cannot contain spaces or underscores (`_`). The `<ttpid>` is a unique identifier for each patient, generated by one of our other services. Here is an example of how to structure the `curl` command:

```bash
curl --request POST \
  --url https://<ipaddress>/send/receiver.<location>-service \
  --header 'Authorization: Basic <usernameAndPassword>' \
  --header 'Content-Type: multipart/form-data' \
  --header 'User-Agent: insomnia/9.3.2' \
  --header 'filename: <filename>-ttpid-lemedart-<ttpid>.<filetype>' \
  --form 'files=@<filepath>/<filename>-ttpid-lemedart-<ttpid>.<filetype>'
```

To access the service, you will need a username and password, which will be provided once your service endpoint is operational.


## Viewing Files by TTPID

To view the files associated with a specific patient's TTPID, you can use the following API endpoint: `GET: http://81.89.199.150:3000/files/<ttpid>`. This request will return a list of all files saved under that TTPID, along with their upload timestamps, formatted as follows:


```
{
	"ttpId": "05RP60PX",
	"source_location": "gki-service",
	"last_updated": "2024-08-09 16:56:15",
	"documents": [
		{
			"_name": "Questionnaire3-ttpid-lemedart-05RP60PX.json",
			"_uri": "//app/uploads/sender.gki-service_1723193208_Questionnaire3-ttpid-lemedart-05RP60PX.json",
			"_timestamp": "2024-08-09 08:46:48",
			"_id": "66b63503d9d7ba3f6c057051"
		},
		{
			"_name": "Questionnaire3-ttpid-lemedart-05RP60PX.json",
			"_uri": "//app/uploads/sender.gki-service_1723193208_Questionnaire3-ttpid-lemedart-05RP60PX.json",
			"_timestamp": "2024-08-09 08:46:48",
			"_id": "66b6351ad9d7ba3f6c057055"
		},
		{
			"_name": "example.json",
			"_uri": "//app/uploads/sender.gki-service_1723193208_example_patient-ttpid-lemedart-05RP60PX.json",
			"_timestamp": "2024-08-09 08:46:48",
			"_id": "66b63c2fc4a7a4be9a22aa3b"
		},
		{
			"_name": "example patient-ttpid-lemedart-05RP60PX.json",
			"_uri": "//app/uploads/sender.gki-service_1723193208_example patient-ttpid-lemedart-05RP60PX.json",
			"_timestamp": "2024-08-09 08:46:48",
			"_id": "66b64461d3e27d90c7f89823"
		},
		{
			"_name": "example patient-ttpid-lemedart-05RP60PX.json",
			"_uri": "//app/uploads/sender.gki-service_1723193208_example patient-ttpid-lemedart-05RP60PX.json",
			"_timestamp": "2024-08-09 08:46:48",
			"_id": "66b64a17d3e27d90c7f8982f"
		},
		{
			"_name": "example patient-ttpid-lemedart-05RP60PX.json",
			"_uri": "//app/uploads/sender.gki-service_1723193208_example patient-ttpid-lemedart-05RP60PX.json",
			"_timestamp": "2024-08-09 08:46:48",
			"_id": "66b64a2fd3e27d90c7f89837"
		}
	]
}
```

## Downloading Data by TTPID

To download all files associated with a specific TTPID, use the following API endpoint: `GET http://81.89.199.150:3000/downloadData/<ttpid>`. This will retrieve all data linked to that TTPID.

## Connecting to the Database

To access the database using MongoDB Compass, use the following connection string:

`mongodb://LeMeDaRT_user:V%5E%235a4dt3%40*%24%25y7@81.89.199.150:5015/`

## Debug

To debug all the services in between connect to the following IP addresses:

```
I.      81.89.199.137 gki-service           using dev-key.pem
II.     81.89.199.185 unihd-bridgehead      using dev-key.pem
III.    81.89.199.150 mdat                  using dev-key.pem
```

For instances I and II, the `/home/ubuntu/data` directory stores all uploaded data. All services are located in the `/srv/docker/bridgehead` folder, with the main services in the `leme` and `standort_preprocessing` subdirectories.

In instance III, all services are located in the `/home/ubuntu` directory. The MongoDB database is in the `/mongo` directory, and the Express API server is in the `/mongo_setup` directory.
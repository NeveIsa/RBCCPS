## Server to collect 3D printer job information

### Steps to use the server with help of Google Forms


1. Create a google form with all the questions necessary
2. Add a question (of response type short text) named **'recordID'**
3. Link the google form to a response spreadsheet
4. Get the sharable URL of the google form and paste it in the file named **'gformurl.txt'**
5. Run the server and check if the Google Form renders well in the browser


### Steps to run the Data Acquisition script

1. Create a script, lets name it AQscript,  which checks the file **status.txt** which may contain one of 3 words from the set {"active","intermediate","inactive"}
2. When a new 3D printer job is registered, the **status.txt** content is changed to **intermediate** and a file named **recordID.txt** is created which contains a random unique identifier string.
3. AQscript, on finding **intermediate** in status.txt, changes the content of **status.txt** to **active** starts its aquisition task while storing the file with a name same as the content of the file **recordID.txt**
4. After the AQscript is done with its acquisition task, it must change content of **status.txt** to **inactive** and delete the **recordID.txt** file.

Name:Huaxin Tang
Email:htang28@binghamton.edu



It's tested on remote machine, totally working.
There is a results png in this dirctory.

Genrate the certificate: 
please replace the IP and hostname to run this
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes \
-subj "/CN=hostname" \
-addext "subjectAltName = DNS:hostname,IP:192.168.1.18"

After genrating the certicifcate

To run server:
python3 sftpserv.py 1967

To run the client:
python3 sftpcli.py domain 1967

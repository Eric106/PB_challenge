# PB challenge 
```text
├── README.md
├── requirements.txt
├── set_workers.py
├── src
│   ├── __init__.py
│   ├── modules
│   │   ├── auth.py
│   │   ├── config
│   │   │   ├── config.json
│   │   │   └── __init__.py
│   │   ├── model.py
│   │   └── sql.py
│   ├── routes.py
│   ├── ssl_data
│   │   ├── playbusiness.test.crt
│   │   ├── playbusiness.test.csr
│   │   ├── playbusiness.test.key
│   │   └── ssl.conf
│   └── webapp.py
├── start_server.sh
├── startup.py
└── stop_server.sh
```
## Install **tmux & conda**
> `NOTE ✅` You need to install  `tmux` and `conda`.

To install `tumx` use this command:
```console
sudo apt install tmux
```
For `conda` you can download the latest installer from [conda.io](https://docs.conda.io/en/latest/miniconda.html) for your linux distro, for example x86_64: 
```console
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```
And then installing it with
> NOTE 👀: When the installer prompt if you want to execute "conda init" select yes. 
```console
bash Miniconda3-latest-Linux-x86_64.sh
```
`OPTIONAL ->` To avoid the automatic activation of the conda base environment use this: 
```console
conda config --set auto_activate_base false
```
## **Install App**

Once you have installed `tmux` and `conda`, clone this repo.
```console
git clone "https://github.com/Eric106/PB_challenge"
```

Then you need to create the environment and install all the python dependencies.

```console
conda create -n back_end python==3.10.* -y
conda activate back_end
pip install -r PB_challenge/requirements.txt
```
### **MYSQL Setup**
To set up the DB you can use the [playbusiness_test.sql](./db_restore/playbusiness_test.sql) file. Execute the next command to restore the schema
```console
mysql -u user -p playbusiness_test < PB_challenge/db_restore/playbusiness_test.sql
```

### **SSL certificates**
If you want to set a different SSL keys, then modify the [start_server.sh](./start_server.sh) script, at the beginning of it just change the route of your SSL files.
```bash
#!/bin/bash
ssl_cert="src/ssl_data/playbusiness.test.crt"
ssl_key="src/ssl_data/playbusiness.test.key"
```
Also at `src/ssl_data/` you can use the self signed SSL keys that are included in this repo

### **Server Config**
To set the secret keys and DB connection credentials, you need to provide the `config.json` file, at `src/modules/config/config.json`
```json
{
    "secret_key":"$#th43&JYRMNj45eYJM%68I%8kYUT9",
    "jwt_key":"dS6cggck878$J$JY45y$5J%#h35hg#",
    "db_host":"server.mysql.db.host",
    "db_user":"server_user01",
    "db_pass":"<YOUR_PASSWORD>",
    "db_schema":"playbusiness_test"
}
```
In the same folder `src/modules/config/` is a [config_template.json](./src/modules/config/config_template.json)

---
## Start server
Command to start the web server
```console
bash start_server.sh
```

## Stop server
Command to stop the web server
```console
bash stop_server.sh
```
---
### Check server console
Command to check the web server console
```console
tmux a -t back_end
```


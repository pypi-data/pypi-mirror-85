# fserver

File Sharing Server implemented with flask and gevent


### install 

```shell
$ pip install fserver -U
```


### usage 

```text
usage: fserver [-h] [-d] [-u] [-o] [-i IP] [-p PORT] [-r PATH]
               [-a PATH [PATH ...]] [-b PATH [PATH ...]] [-s STRING]

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           run with debug mode
  -u, --upload          run with upload file function
  -o, --override        override mode for upload file
  -i IP, --ip IP        ip address for listening, default 0.0.0.0
  -p PORT, --port PORT  port for listening, default 2000
  -r PATH, --root PATH  root path for server, default current path
  -a PATH [PATH ...], --allow PATH [PATH ...]
                        run with allow_list. Only [PATH ...] will be accessed
  -b PATH [PATH ...], --block PATH [PATH ...]
                        run with block_list. [PATH ...] will not be accessed
  -s STRING, --string STRING
                        share string only
  -v, --version         print version info
```


### license
[MIT](LICENSE)
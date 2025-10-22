前端 dist 目录改为 web

启动服务：uvicorn main:app  
启动服务：uvicorn main:app --reload

一些依赖
```shell


pip install requests --index-url https://mirrors.cloud.tencent.com/pypi/simple/
pip install bs4 --index-url https://mirrors.cloud.tencent.com/pypi/simple/
pip install lxml --index-url https://mirrors.cloud.tencent.com/pypi/simple/
pip install selenium --index-url https://mirrors.cloud.tencent.com/pypi/simple/
pip install fastapi --index-url https://mirrors.cloud.tencent.com/pypi/simple/
pip install "uvicorn[standard]" --index-url https://mirrors.cloud.tencent.com/pypi/simple/
pip install sqlalchemy pymysql --index-url https://mirrors.cloud.tencent.com/pypi/simple/
pip install  schedule --index-url https://mirrors.cloud.tencent.com/pypi/simple/
pip install  dotenv  --index-url https://mirrors.cloud.tencent.com/pypi/simple/
pip install fake-useragent --index-url https://mirrors.cloud.tencent.com/pypi/simple/
```

打包依赖

```shell
pip freeze > requirements.txt
pip install -r requirements.txt

```
linux 安装  chromedriver
```shell

sudo apt update
sudo apt --fix-broken install
sudo apt-get install -y libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
google-chrome --version   
sudo apt install chromium-chromedriver
 chromedriver --version
which chromedriver
sudo chmod +x /usr/bin/chromedriver


```


# try  two method
chromedriver 下载地址
https://googlechromelabs.github.io/chrome-for-testing/



nginx config


```nginx
server {
		listen 80;
		#填写证书绑定的域名
		server_name www.xxx.com;
	
#	access_log  logs/host.access.log  main;
        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

 location / {
        root /xxx/aws_server/web;  # Vue 应用的构建目录路径
        try_files $uri $uri/ /index.html;
    }

    location /api {  # 假设你的 FastAPI 路由以 /api 开头
        proxy_pass http://127.0.0.1:8000;  # FastAPI 运行的端口和地址
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}


```
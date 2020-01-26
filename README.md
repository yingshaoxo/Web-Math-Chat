# Web-Math-Chat
A simple real time math chat web app built on `parcel`, `bootstript` and `flask`.

### Demo
heroku: [https://web-math-chat.herokuapp.com](https://web-math-chat.herokuapp.com)

### Usage
```
sudo docker-compose up -d

or 

sudo docker run -d -v ~/.mathchat:/root/mathchat -p 5000:5000 --name mathchat yingshaoxo/mathchat
```

### Python Env
```
sudo pip3 install -r requirements.txt
```

### Javascript Env
```
cd front-end_app
yarn
```

### Reverse-Proxy configuration for HTTPS
#### Important!
Make sure your server `Cross-Origin Controls` is set to `'*'` to allow Cross-Origin Access

For `flask-socketio`, is to use `flask_socketio.SocketIO(app, cors_allowed_origins = '*')`

#### For Nginx
```
server {
    listen 80;
    server_name ai-tools-online.xyz;
    return 301 https://ai-tools-online.xyz$request_uri;
}

server {
    listen 443 ssl http2;

    ssl_certificate       /data/v2ray.crt;
    ssl_certificate_key   /data/v2ray.key;
    ssl_protocols         TLSv1.2 TLSv1.3;
    #ssl_ciphers           3DES:RSA+3DES:!MD5;
    server_name ai-tools-online.xyz;

    location / {
        proxy_pass http://127.0.0.1:5000;
    }

    location /socket.io {
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_pass http://127.0.0.1:5000/socket.io;
    }
}
```

#### For Caddy:
```
ai-tools-online.xyz {
    proxy / 127.0.0.1:5000 {
        except /socket.io
        transparent
    }

    proxy /socket.io 127.0.0.1:5000 { 
        websocket 
        transparent
    } 
}
import sites/*
```

or

```
ai-tools-online.xyz {
    proxy / 127.0.0.1:5000 {
        except /socket.io
    }
    proxy /socket.io 127.0.0.1:5000 { 
        header_upstream Host {host} 
        header_upstream X-Real-IP {remote} 
        header_upstream X-Forwarded-For {remote} 
        websocket 
    } 
}
import sites/*
```

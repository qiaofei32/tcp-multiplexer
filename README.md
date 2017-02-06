# tcp-multiplexer
A TCP service multiplexer in Python

## 用途
    在远程服务器只开放特定端口，但是需要支持不同应用访问的时候，如某服务器/防火墙只允许9000端口进行通信，但是此时我想要使用ssh服务，同时使用其http服务，或者其他服务。此时，可以使用该程序进行端口多路复用。
    `tcp-multiplexer-demo.py`中的`PROTOCOL_RULES`可以根据需要进行配置，监听在本地的端口如：9000，接收到客户端的请求之后，会根据正则表达式去匹配相应的规则进行应用选择。

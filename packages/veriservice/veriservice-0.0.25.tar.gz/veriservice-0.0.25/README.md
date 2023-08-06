# Veri Python Client
Python client for veri

```shell script
pip install veriservice
```


```python
import veriservice
```


```python
service = "localhost:5678"

veriservice.init_service(service, "./tmp")

client = veriservice.VeriClient(service, "example_data")
data_conf = {}
client.create_data_if_not_exists(data_conf)
data = [
            {
                'label': 'a',
                'feature': [0.5, 0.1, 0.2]
            },
            {
                'label': 'b',
                'feature': [0.5, 0.1, 0.3]
            },
            {
                'label': 'c',
                'feature': [0.5, 0.1, 1.4]
            },
        ]

for d in data:
    client.insert(d['feature'], d['label'].encode())

result = client.search([[0.1, 0.1, 0.1]])
for i in result:
    print(i)

result = client.data()
for i in result:
    print(i)
```
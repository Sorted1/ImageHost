# ImageHost
ShareX Image Host Made In Flask

## Installation

Install ImageHost with git

```bash
  git clone https://github.com/Sorted1/ImageHost.git
  cd ImageHost
  pip3 install requirements.txt
  SET API Keys In app.py
  python3 app.py
```


## Usage/Examples

```bash
curl -X POST -H "apikey: YOUR_API_KEY" -H "title: Image Title" -H "hexcolor: #AABBCC" -H "description: Image Description" -F "file=@/path/to/your/image.jpg" http://your-server/upload
```
Or Create Via ShareX
## API Reference

#### Get all items

```http
  POST /upload
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `apikey` | `string` | **Required**. Your API key |
| `title` | `string` | Embed Title |
| `description` | `string` | Embed Description |
| `hexcolor` | `string` | Embed HexColor |

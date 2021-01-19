# Auto Clean Cloudreve Trashes

## Usage

### Directly from shell

```bash
chmod +x main.py
./main.py --work_dir=/path/to/your/cloudreve
```

### Python

```bash
/path/to/your/Python main.py
```

## Service

```bash
sudo cp ./cloudreve-trash-cleaner.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable cloudreve-trash-cleaner
sudo service cloudreve-trash-cleaner start
```

# awtrix-push
Push custom info to Awtrix's CustomApp

## Preparation
1. Make sure CustomApp is installed.
2. Create python3.x env.
3. Install package: `pip install -r requirement.txt`

## Config
1. Copy `template.cfg` as `config.cfg`, and change it.
2. In `parse/__init__.py`, write function to resolve your tasks. The function's name name needs to be the same as you defined in the `confg.cfg`, but use lower case.


## Run
```bash
# Run celery worker
CFG_PATH=config.cfg make

# Run celery beat
CFG_PATH=config.cfg make beat
```
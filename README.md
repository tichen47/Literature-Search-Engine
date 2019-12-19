# i-Search

### 0. Prerequest
1. python version: 3.6
2. package: `waitress, flask, pickle, metapy`

### 1. Data preprocessing
1. add `grobid_processed` data under the root project
2. run `python3 MeTA/preprocessor.py`
3. run `python3 MeTA/inv_idx_config_builder.py`
4. run `python3 MeTA/query.py`

### 2. Run the server locally
1. run `python3 app.py`
2. open your browser and visit `http://0.0.0.0/`

## Remote server: 18.190.124.145

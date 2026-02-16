

requirements: 
- python 3.8
- Fastapi
- uvicorn [standaed]


create environment with conda 
conda create -n mega

active it using  : conda activate ...
conda activate mega


# optional :  put in teminal 
```bash
$ notepad $PROFILE
```

function prompt {
    "$env:USERNAME@$env:COMPUTERNAME $(Get-Location)`n> "
}




## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.
# cvtool-ingestion-pipeline


Create a `settings.bash` file which will export the necessary environment variables

```bash
cat <<EOF > settings.bash
#!/usr/bin/env bash

export JOBS_API_HOST='https://mydomain.com/v1'
export IMAGES_API_HOST='https://mydomain.com/v1'
export DEBUG='True'
EOF
```

### Install dependencies

```bash
pip install -r requirements.txt -t lib
```

### Running locally

```bash

dev_appserver.py .

```

### Deploying

```bash
./deploy.sh ${PROJECT_ID} ${VERSION}
```
# Instructions

Copy `.env.example` file to `.env` file to work in local.

```bash
APIKEY=<paste your IAM APIKEY>
REGION=eu-gb
SPACE_UID=<paste your space uid>
DEPLOYMENT_UID=<paste your deploymennt uid>
```

## Replace all entries with your values

### APIKEY

To create an APIKEY from terminal:

```bash
ibmcloud login
ibmcloud iam api-key-create API_KEY_NAME
```

### REGION

Region is the location where you create your services. Create all your services in the same region: e.g. London or Dallas.

### SPACE_UID and DEPLOYMENT_UID

You have to [create a watson studio](https://cloud.ibm.com/catalog/services/watson-studio) service and a [watson machine learning](https://cloud.ibm.com/catalog/services/machine-learning) service.

Then create a deployment space in watson studio. Don't forget to attach your watson machine learning instance to it. You can copy **SPACE_UID** fom settings tab in deployment details.

Deploy your model to your deployment service using AUTO AI or Jupyter notebook. You can follow [this documentation](https://eu-gb.dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/ml-samples.html?audience=wdp&context=wdp).

> You can also run `python3 get_uids.py` command to get you space and deployment uids. You have to set your **REGION** and **APIKEY** first in `.env` file.

[Detailed watson studio and machine learning documentation is here].

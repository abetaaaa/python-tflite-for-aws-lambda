<div id="top">

<img src="https://img.shields.io/badge/Python-3776AB.svg?logo=python&logoColor=white">
<img src="https://img.shields.io/badge/-AWS%20Lambda-232F3E.svg?logo=awslambda&style=flat">
<img src="https://img.shields.io/badge/-AWS%20ECR-232F3E.svg?logo=amazonecs&style=flat">
<img src="https://img.shields.io/badge/-Docker-2496ED.svg?logo=docker&logoColor=white">
<img src="https://img.shields.io/badge/-TensorFlow%20Lite-FF6F00?logo=tensorflow&logoColor=white">
<img src="https://img.shields.io/badge/-WSL2-E95420?logo=ubuntu&logoColor=white">

</br>
</div>

# Deploying Tensorflow Lite on AWS Lambda using Docker and AWS Elastic Container Registry(ECR)
This repository contains the necessary resources to deploy TensorFlow Lite on AWS Lambda using Docker and ECR.  
TensorFlow Lite allows you to run lightweight deep learning models on resource-limited environment like AWS Lambda.  

![architecture](https://github.com/abetaaaa/python-tflite-for-aws-lambda/assets/78013610/d350841c-ab3d-447d-a638-550865201dbf)


## Environment
| Language/Library   | Version |
| ------------------ | ------- | 
| Python             | 3.9.18  |
| tflite-runtime     | 2.7.0   |

## Structure
```
.  
├── Dockerfile  
├── README.md  
├── awsconf
├── build_and_deploy_ecr.sh
├── models/  
│   └── (put your tflite models here)  
├── requirements.txt  
└── update_ecr.sh  
```

## Prerequisites
Before getting started, ensure you have the following:
- Docker installed on your local machine.
    - if you don't have, install from https://www.docker.com/.
- An AWS account with access to Elastic Container Registry (ECR) and AWS Lambda.
- AWS CLI installed on your local machine and setup config and credentials.
    - if you don't have, click [here](https://docs.aws.amazon.com/latest/cli/latest/userguide/getting-started-install.html).


## Getting Started

Follow these steps to deploy TensorFlow Lite on AWS Lambda:

### 1. Clone the Repository:
Run the folloing commands in a directory where you want to develop.
```bash
git clone https://github.com/abetaaaa/python-tflite-for-aws-lambda.git
```

### 2. Prepare TFlite Model
Create TensorFlow Lite models and store them in the `models` directory.  
If you already have a TF model (e.g. .keras), you can convert it to .tflite with [Tensorflow Lite Converter](https://www.tensorflow.org/lite/models/convert).


### 3. Build Docker Image, upload it to ECR, create execution role and Lambda function.
Edit the `awsconf` file match your AWS environment settings.  
After that, all you need is execute the batch script `build_and_deploy_ecr.sh`.  

Details of `build_and_deploy_ecr.sh` are as follows.

---

#### Build Docker image:
```sh
docker build --platform linux/amd64 -t $IMAGE_NAME:test .
``` 

#### Tag Docker image:
```sh
docker tag docker-image:test $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY_NAME:latest
```

#### Login to AWS ECR and push Docker Image to ECR:
```sh
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
aws ecr create-repository --repository-name $REPOSITORY_NAME --region $REGION --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY_NAME:latest
```

#### Deploy to AWS Lambda:
```sh
aws lambda create-function \
  --function-name $FUNCTION_NAME \
  --package-type Image \
  --code ImageUri=$AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY_NAME:latest \
  --role arn:aws:iam::$AWS_ACCOUNT_ID:role/$IAM_ROLE_NAME
```


> [!CAUTION]
> When using a tflite-runtime version newer than 2.7.0, you may encounter the following error.  
>```bash
>[ERROR] Runtime.ImportModuleError: Unable to import module 'lambda_function': /lib64/libm.so.6: version 'GLIBC_2.27' not found (required by /opt/python/lib/python3.9/site-packages/tflite_runtime/_pywrap_tensorflow_interpreter_wrapper.so)
>```

## References
- https://docs.aws.amazon.com/lambda/latest/dg/python-image.html
- https://github.com/tpaul1611/python_tflite_for_amazonlinux 

# Run this script when you have made any changes to the Docker image or lambda_function.py.
. ./awsconf

# Build the Docker image from Dockerfile
docker build --platform linux/amd64 -t $IMAGE_NAME:test .

# Deploying the image
docker tag docker-image:test $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY_NAME:latest
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY_NAME:latest

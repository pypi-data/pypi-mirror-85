# Postal
A light Docker control tool designed around compose and swarm  
[Documentation](https://github.com/obe-de/postal)  
[PyPi Package](https://pypi.org/project/docker-postal/)  


# Getting Started
Postal requires that you have python >= 3.6, docker, and docker-compose installed. Postal is designed for use on Linux.

# Installing Client
To install:  
`pip install docker-postal`

For the console script to be installed you may need to install with:  
`pip install --user docker-postal`

Or unfortunately if (~/.local/bin) is not on your system path:  
`sudo pip install docker-postal`

# Installing Service
To install the postal server, you must first setup a secure S3 bucket to store configurations.

### S3 Bucket
To setup S3, create a secure, private, encrypted bucket. Then create user to access this bucket with the following
permissions:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObjectAcl",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::example-bucket-name/*",
                "arn:aws:s3:::example-bucket-name"
            ]
        }
    ]
}
```

### Postal Service
The postal service runs an openssh server than enables remote access to the docker daemon/swarm.


On swarm manager, login to a docker repository where images will be pushed and retrieved:
```
docker login
```


Create postal config folder and add an authorized key:
```
mkdir /data/postal
touch /data/postal/authorized_keys
chmod 600 /data/postal/authorized_keys
sudo chown -R root:root /data/postal
sudo nano /data/postal/authorized_keys # paste in your public key and save
```

Clone postal repository:
```
git clone https://github.com/obe-de/postal
cd postal
```

Create an environment file:
```
nano stack/production.env
```

Then paste:
```
POSTAL_AWS_BUCKET=example-bucket-name
POSTAL_AWS_REGION=us-east-2
AWS_ACCESS_KEY_ID=YOURKEY
AWS_SECRET_ACCESS_KEY=yoursecret
```

Deploy postal stack:
```
docker stack rm postal # (optional)
docker build -t postal:latest -f stack/postal/Dockerfile .
docker stack deploy -c stack/production.yml postal
```

Check that everything is working:
```
docker service ls | grep postal
```

(Optional) Check that you can exec bash in the container:
```
docker exec -it $(docker ps -aqf "name=postal_postal") bash
```

Login from the client:
```
postal login -u root -a yourdomain -p 5020
```

# Connecting and Deploying
After you have deployed the postal service check that your public key has been added (instructions below) so
you have permission to connect.

1. Login to the postal service using `postal login`.  
2. Double check that you have connected by running a swarm command like `postal swarm ps`.  
3. Enter project directory that you want to deploy.  
4. Configure project environment variables: `postal config ls` and `postal config set` etc.
5. Create a `production.yml` file in the stack with `env_file: production.env` if you want the
   project's production configuration injected.
6. Make sure the ports you have selected in `production.yml` aren't going to clash with an
   existing service.
7. Deploy working directory using `postal swarm deploy -w`.  
8. Check the status of your service using `postal swarm service ls`
9. Debug services that fail to replicate using `docker service ps --no-trunc your_service_name_here`
10. Your service should be accessible via any node on the swarm if you used the swarms overlay network.

# Todo
* Don't use disk backed temp files for RPC input / output
* Deploy from git origin

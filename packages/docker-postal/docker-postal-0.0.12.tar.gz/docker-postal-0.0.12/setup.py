# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['postal', 'postal.commands', 'postal.core']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0', 'boto>=2.49.0,<3.0.0']

entry_points = \
{'console_scripts': ['postal = postal.cli:main']}

setup_kwargs = {
    'name': 'docker-postal',
    'version': '0.0.12',
    'description': 'A light Docker control tool designed around compose and swarm',
    'long_description': '# Postal\nA light Docker control tool designed around compose and swarm  \n[Documentation](https://github.com/obe-de/postal)  \n[PyPi Package](https://pypi.org/project/docker-postal/)  \n\n\n# Getting Started\nPostal requires that you have python >= 3.6, docker, and docker-compose installed. Postal is designed for use on Linux.\n\n# Installing Client\nTo install:  \n`pip install docker-postal`\n\nFor the console script to be installed you may need to install with:  \n`pip install --user docker-postal`\n\nOr unfortunately if (~/.local/bin) is not on your system path:  \n`sudo pip install docker-postal`\n\n# Installing Service\nTo install the postal server, you must first setup a secure S3 bucket to store configurations.\n\n### S3 Bucket\nTo setup S3, create a secure, private, encrypted bucket. Then create user to access this bucket with the following\npermissions:\n\n```\n{\n    "Version": "2012-10-17",\n    "Statement": [\n        {\n            "Sid": "VisualEditor0",\n            "Effect": "Allow",\n            "Action": [\n                "s3:PutObject",\n                "s3:GetObjectAcl",\n                "s3:GetObject",\n                "s3:ListBucket",\n                "s3:DeleteObject",\n                "s3:PutObjectAcl"\n            ],\n            "Resource": [\n                "arn:aws:s3:::example-bucket-name/*",\n                "arn:aws:s3:::example-bucket-name"\n            ]\n        }\n    ]\n}\n```\n\n### Postal Service\nThe postal service runs an openssh server than enables remote access to the docker daemon/swarm.\n\n\nOn swarm manager, login to a docker repository where images will be pushed and retrieved:\n```\ndocker login\n```\n\n\nCreate postal config folder and add an authorized key:\n```\nmkdir /data/postal\ntouch /data/postal/authorized_keys\nchmod 600 /data/postal/authorized_keys\nsudo chown -R root:root /data/postal\nsudo nano /data/postal/authorized_keys # paste in your public key and save\n```\n\nClone postal repository:\n```\ngit clone https://github.com/obe-de/postal\ncd postal\n```\n\nCreate an environment file:\n```\nnano stack/production.env\n```\n\nThen paste:\n```\nPOSTAL_AWS_BUCKET=example-bucket-name\nPOSTAL_AWS_REGION=us-east-2\nAWS_ACCESS_KEY_ID=YOURKEY\nAWS_SECRET_ACCESS_KEY=yoursecret\n```\n\nDeploy postal stack:\n```\ndocker stack rm postal # (optional)\ndocker build -t postal:latest -f stack/postal/Dockerfile .\ndocker stack deploy -c stack/production.yml postal\n```\n\nCheck that everything is working:\n```\ndocker service ls | grep postal\n```\n\n(Optional) Check that you can exec bash in the container:\n```\ndocker exec -it $(docker ps -aqf "name=postal_postal") bash\n```\n\nLogin from the client:\n```\npostal login -u root -a yourdomain -p 5020\n```\n\n# Connecting and Deploying\nAfter you have deployed the postal service check that your public key has been added (instructions below) so\nyou have permission to connect.\n\n1. Login to the postal service using `postal login`.  \n2. Double check that you have connected by running a swarm command like `postal swarm ps`.  \n3. Enter project directory that you want to deploy.  \n4. Configure project environment variables: `postal config ls` and `postal config set` etc.\n5. Create a `production.yml` file in the stack with `env_file: production.env` if you want the\n   project\'s production configuration injected.\n6. Make sure the ports you have selected in `production.yml` aren\'t going to clash with an\n   existing service.\n7. Deploy working directory using `postal swarm deploy -w`.  \n8. Check the status of your service using `postal swarm service ls`\n9. Debug services that fail to replicate using `docker service ps --no-trunc your_service_name_here`\n10. Your service should be accessible via any node on the swarm if you used the swarms overlay network.\n\n# Todo\n* Don\'t use disk backed temp files for RPC input / output\n* Deploy from git origin\n',
    'author': 'Stephen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/leviat-tech/postal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

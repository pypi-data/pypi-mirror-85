# Fargate supported run configs interms of vCPUs and memory
fargate_configs = {

    '0.25': [0.5, 1, 2],
    '0.5': [1, 2, 3, 4],
    '1': [2, 3, 4, 5, 6, 7, 8],
    '2': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    '4': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
          20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
}

# Taskdefinition template to be used when creating a new one
taskdef_template = {
    "taskRoleArn": "____TASKROLE____",
    "executionRoleArn": "____EXECUTIONROLE____",
    "networkMode": "awsvpc",
    "requiresCompatibilities": [
        "FARGATE"
    ],
    "cpu": "____CORES____",
    "memory": "____MEMORY____",
    "family": "____FAMILY____",
    "containerDefinitions": [
        {
            "name": "airflow",
            "image": "____CONTAINER_IMAGE____",
            "cpu": 0,
            "links": [],
            "portMappings": "____CONTAINER_PORTS____",
            "essential": True,
            "entryPoint": [],
            "command": [],
            "environment": [],
            "mountPoints": [],
            "volumesFrom": [],
            "secrets": [],
            "dnsServers": [],
            "dnsSearchDomains": [],
            "dockerSecurityOptions": [],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "____AIRFLOW_STACK____/____FAMILY____",
                    "awslogs-region": "____AWS_REGION____",
                    "awslogs-stream-prefix": "____FAMILY____"
                }
            },
            "systemControls": []
        }
    ],
    "volumes": []
}

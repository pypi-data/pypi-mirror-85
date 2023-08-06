# aws_ecs_services

## Why
I would like to easily ssh into the instance an ECS service is running on. When deployed into a cluster with several instances you cannot accomplish this using `awscli`.

I work through a VPN, so I am only interested in the instances' private IP addresses. When using the AWS Session Manager I am interested in the instances' ids.

The script provides two ways to get the instance's information:
* **1. approach**: For **ECS services that use service discovery** and register a DNS name with AWS Route53, it's possible to get the services's/container's private IP and then check which EC2 instance contains the same private IP.
* **2. approach**: When using AWS SSM (with `ssm-agent` on EC2 instances and AWS Session Manager Plugin locally) the tool will connect to every ECS cluster instance and compares a given service with running ones (running docker containers).

In case the infrastructure is deployed with terraform, the service names as well as the DNS names of the services become predictable.

## How

The tool is best used with `aws-vault`. So far I did not implement reading AWS profiles with `boto3` e.g.

**1. approach** (services with service discovery only) using `by-service-dns`:

```
aws_ecs_services by-service-dns --region <aws_region> --cluster <ecs_cluster_name> --dns <service_dns_name> [--output <output_info>]
```

The tool gets the DNS name of the service (AWS Route53). It also gets the name of the cluster the service was created in. Also the tool gets the AWS region to use.

The association between the service's DNS name and the instance private IP:
* Get the IP of the service by DNS name (host name).
  - IP is changing constantly (with every deployment), DNS name is not.
* Get all the cluster instances.
  - Make sure you configure the correct cluster (The service nneds to be located in there.).
* Get the private IP addresses of these instances and compareto the IP address of the service.
* The match reveals the correct instance.

**2. approach** (all services, requires a working AWS SSM setup) using `by-service-name`:

```
aws_ecs_services by-service-name --region <aws_region> --cluster <ecs_cluster_name> --name <part_of_service_name_even_regex>
```

The tool gets the name of the service (AWS ECS service) or part of it (regular expressions allowed). It also gets the name of the cluster the service was created in. Also the tool gets the AWS region to work in.

All cluster instances are checked for running docker containers. Using regular expressions the given service name is searched for in the list of docker container names. If a match is found the according instance id will be returned.

Only the first match will be considered.


## Usage
For better readability I will leave out `aws-vault` in the examples below.

There are 4 sub commands:
* `by-service-dns` - Get instance information by service's dns name.
* `by-service-name` - Get instance id by service's name.
* `list-instances` - Get all cluster instances (instance ids).
* `list-services` - Get all active cluster services.
* `list-configured-services` - Get all configured services, in the config file. Requires a config file.
* `list-configured-projects` - Get all configured projects, in the config file. Requires a config file.

Here you can find some examples to ssh into the appropriate EC2 instance:
```
# Get instance IP address by service DNS name
ssh ec2-user@"$(aws_ecs_services by-service-dns --region eu-west-2 --cluster my-cluster --dns dns.name.com)"
# Get instance ID by service DNS name
aws ssm start-session --target "$(aws_ecs_services by-service-dns --region eu-west-2 --cluster my-cluster --dns dns.name.com --output id)"
# Get instance ID by service name
aws ssm start-session --target "$(aws_ecs_services by-service-name --region eu-west-2 --cluster my-cluster --name part_of_service_name_even_regex)"
```

**_Note_**:
* The configuration can be done within a configuration file as well (see **Use with configuration file**).

Here you can find further examples of how to use this tool:
```
# List all instance IDs in cluster
aws_ecs_services list-instances --region eu-west-2 --cluster my-cluster
# List all service names deployed in the cluster
aws_ecs_services list-services --region eu-west-2 --cluster my-cluster
```
Using regular expressions
`aws_ecs_services by-service-name --region eu-west-2 --cluster dev --name "price-redis-[a-z0-9]*$" --debug`


**_Note_**:
* `--debug` shows additional output in order to really get the correct container (service) in case more than one was found e.g..


The default output of the subcommand `by-service-dns` is the instance's private IP address.
* If called with `--output id` it displays the instance's id.
    ```
        # Get instance id by service DNS name
        aws ssm start-session --target "$(aws_ecs_services by-service-dns --region eu-west-2 --cluster my-cluster --dns dns.name.com --output id)"
    ```
* If called with `--output all` it displays both of the values above. In addition it returns the instance's private DNS name.
* If called with `--output service` it displays the service's IP address only.

## Use with configuration file

When using a configuration file most of the cli options can be left out.

The default location is `~/.config/aws_tools/config`.

The configuration file template looks like this, also see `./config.template`:
```
{
    "region": "eu-west-1",
    "projects": {
        "projectA": {
            "region": "eu-west-2",
            "cluster": "default",
            "dns": "{service}.domain.com",
            "services": {
                "serviceA": {
                    "description": "Service is using project-level default values for 'cluster' and 'dns'."
                },
                "serviceB": {
                    "description": "Service name is part of cluster name. Using variable replacement for 'cluster'",
                    "cluster": "{cluster}-serviceB"
                },
                "serviceC": {
                    "description": "Service name is part of cluster name. Using variable replacement for 'service'. Eventually same as with 'serviceB'.",
                    "cluster": "{cluster}-{service}"
                },
                "serviceD": {
                    "description": "Same as 'serviceC', even runs in the same AWS ECS service - Is configured as additional container in the task definition of 'serviceC'.",
                    "cluster": "{cluster}-serviceC",
                    "dns": "serviceC.domain.com"
                },
                "serviceE": {
                    "description": "Service is not deployed with 'awsvpc', no dedicated IP, no DNS name.",
                    "dns": ""
                }
            }
        },
        "projectB": {
            "cluster": "projectB",
            "dns": "{cluster}-{service}.domain.com",
            "services": {
                "serviceA": {
                    "description": "Service is using project-level default values for 'cluster' and 'dns'."
                }
            }
        }
    }
}
```

**_Note_**:
* For the following examples the `./config.template` configuration can be assumed.

There is a top-level `region` specified.
Additionally, on project-level (for every configured project), you can set another `region`.

A project can also have a name for the `cluster` as well as a `dns` name, which is necessary when AWS ECS services are deployed with the `awsvpc` network mode and get their own IP address, register with AWS CloudMap and AWS Route53 etc.

To list all the configured projects:
```
    aws_ecs_services list-configured-projects
    # Result:
    projectA
    projectB
```

Each project has `services`.

To list all the configured services:
```
    # aws_ecs_services --project <configured_project> list-configured-services
    aws_ecs_services --project projectA list-configured-services
    # Result:
    serviceA
    serviceB
    serviceC
    serviceD
    serviceE
```

The service-level configuration for `cluster` and `dns` overrules the project-level configuration.

Example calls (see **Usage** for using cli options):
- List instances in the cluster:
     + Right now, this only checks instances in the **project-level** cluster. **service-level** clusters are not considered, yet.
     + You can list instances using the cli options (see **Usage**).
```
    # aws_ecs_services --project <configured_project> list-instances
    aws_ecs_services --project projectA list-instances
    # Result is a string of AWS EC2 instance ids of instances in the  cluster. Something like:
    i-04d153c42e9b71b8a i-05169fb090fb6a68b i-03029360ad379566d i-01b155c39d4324ad7
```
- List running services in the cluster:
     + Right now, this only checks instances in the **project-level** cluster. **service-level** clusters are not considered, yet.
     + You can list running services using the cli options (see **Usage**).
```
    # aws_ecs_services --project <configured_project> list-services
    aws_ecs_services --project projectA list-services
    # Result is a list of AWS ECS services running in the cluster. Something like:
    ecs-default-serviceA-1-default-serviceA-b4cedd8899a7cba90b00
    ecs-deafult-serviceB-serviceB-1-default-serviceB-serviceB-b4cedd8899a7cba90b01
    ecs-default-serviceC-serviceC-1-default-serviceC-serviceC-b4cedd8899a7cba90b02
    ecs-default-serviceC-serviceD-1-default-serviceC-serviceD-b4cedd8899a7cba90b04
    ecs-default-serviceE-1-default-serviceE-b4cedd8899a7cba90b05
```
- Get a service by its DNS name: `by-service-dns`:
```
    # aws_ecs_services --project <configured_project> --service <configured_service> by-service-dns --output id
    aws_ecs_services --project projectA --service serviceA by-service-dns --output id
    # Result:
    i-00epg17383ba1e1cg
```
- Get a service by its ECS service name: `by-service-name`:
    + `--service` is used to search for the project's service in the configuration file.
    + By default `--service` is also used as the running AWS ECS service to search for.
    + It is possible to additionally add the `--name` option to `by-service-name`, which allows regular expressions. `--name` is preferred over the value of `--service` when it comes to searching for the running AWS ECS service (see **Usage**).
        - **Use case**: Different services where one service name is part of another one's name.
            + With services like `serviceA` and `serviceA1`, when running with `--service serviceA` it is possible that the ECS service `serviceA1` is found instead.
            + This issue can be resolved by passing `--service serviceA by-service-name --name "serviceA-[0-9]+"`.
            + Instead of `--name` you can also configure `"name": "serviceA-[0-9]+" per service` in the configuration file.
            + This makes sure to use service-level configuration for `serviceA` but specifies the AWS ECS service name to search for in greater detail.
```
    # aws_ecs_services --project <configured_project> --service <configured_service> by-service-name
    aws_ecs_services --project projectA --service serviceA by-service-name
    INFO:AwsGetInstance:Instance 'i-04ef6e335a618932a' runs container 'ecs-default-serviceA1-1-default-serviceA1-g6frgg3388d1hjb63f01'
    # Result:
    i-04ef6e335a618932a

    # aws_ecs_services --project <configured_project> --service <configured_service> by-service-name --name <part_of_service_name_even_regex>
    aws_ecs_services --project projectA --service serviceA by-service-name --name "serviceA-[0-9]+"
    INFO:AwsGetInstance:Instance 'i-00epg17383ba1e1cg' runs container 'ecs-default-serviceA-1-default-serviceA-b4cedd8899a7cba90b00'
    # Result:
    i-00epg17383ba1e1cg
```

### Variable replacement

In the configuraiton file it is possible to define values for:
* `cluster` (AWS ECS cluster name)
* `dns` (AWS Route53 DNS name)

As you can see in `./config.template` it's possible to hardcode them, That means it would be necessary to set e.g. `dns` for each and every service.

Making use of variable replacement really is depending on your infrastructure setup and naming schemes.

`aws_ecs_services` makes it possible to reuse some variables.
* The value of the **project-level** `"cluster"` configuration is used to replace occurrences of `{cluster}`.
* The value of the cli option `--service` is used to replace occurrences of `{service}`.

On the **project-level**, the following variable replacement is possible:

| configuration (JSON key) | variable replacement     |
|--------------------------|--------------------------|
| `"cluster"`              | `{service}`              |
| `"dns"`                  | `{cluster}`, `{service}` |


**_Note_**:
* It's not possible to replace the variable `{cluster}` in `"cluster"` on **project-level**, because this is the value that is used to replace `{cluster}`. It would end up replacing itself.

On the **service-level**, the following variable replacement is possible:

| configuration (JSON key) | variable replacement     |
|--------------------------|--------------------------|
| `"cluster"`              | `{cluster}`, `{service}` |
| `"dns"`                  | `{cluster}`, `{service}` |
| `"name"`                 | `{cluster}`, `{service}` |

**_Note_**:
* It's possible to replace the variable `{cluster}` in `"cluster"` on **service-level**, because in this case the **project-level** value for `"cluster"` is used to replace `{cluster}` on **service-level**.


**Examples** - Assume the configuration from `./config.template`:
```
    # aws_ecs_services  --project <configured_project> --service <configured_service> by-service-dns --output id
    aws_ecs_services  --project projectA --service serviceD by-service-dns --output id
    # Raw configuration:
    {
        "region": "eu-west-1",
        "projects": {
            "projectA": {
                "region": "eu-west-2",
                "cluster": "default",
                "dns": "{service}.domain.com",
                "services": {
                    "serviceD": {
                        "cluster": "{cluster}-serviceC",
                        "dns": "serviceC.domain.com"
                    }
                }
            },
            ...
        }
    }
    # Loaded/Actual configuration:
    -> service = "serviceD"
    At first it loads:
    "region" = "eu-west-1"
    However, the final value is:
    -> "region" = "eu-west-2"
    At first it loads:
    "cluster" = "default"
    However, the final value is:
    -> "cluster" = "default-serviceC"
    At first it loads:
    "dns" = "servcieD.domain.com"
    However, the final value is:
    -> "dns" = "serviceC.domain.com"
    # Result:
    i-00epg17383ba1e1cg
```

## requirements.txt vs. setup.py

According to these sources:
* [python documentation](https://packaging.python.org/discussions/install-requires-vs-requirements/)
* [stackoverflow - second answer by jonathan Hanson](https://stackoverflow.com/questions/14399534/reference-requirements-txt-for-the-install-requires-kwarg-in-setuptools-setup-py)

I try to stick to:
* `requirements.txt` lists the necessary packages to make a deployment work.
* `setup.py` declares the loosest possible dependency versions.

### Creating `requirements.txt`

You won't ever need this probably - This is helpful when developing.

`pip-tools` is used to create `requirements.txt`.
* There is `requirements.in` where dependencies are set and pinned.
* To create the `requirements.txt`, run `update_requirements.sh` which basically just calls `pip-compile`.

**_Note_**:
* There also is `build_requirements.txt` which only contains `pip-tools`. I found, when working with virtual environments, it is necessary to install `pip-tools` inside the virtual environment as well. Otherwise `pip-sync` would install outside the virtual environment.

A development environment can be created like this:
```bash
    # Create a virtual environment 'venv'.
    python -m venv venv
    # Activate the virtual environment 'venv'.
    . /venv/bin/activate
    # Install 'pip-tools'.
    pip install --upgrade -r build_requirements.txt
    # Install dependencies.
    pip-sync requirements.txt
    ...
    aws-vault -- python -m aws_ecs_services.aws_ecs_services by-service-name --region eu-west-2 --cluster dev --name "price-redis-[a-z0-9]*$
    # or (assuming an according configuration file)
    aws-vault -- python -m aws_ecs_services.aws_ecs_services --project prices --service=price-redis by-service-name
    ...
    # Deactivate the virtual environment 'venv'.
    deactivate
```

# RDS Auto Start and Stop

An AWS lambda implementation to start and stop MySQL RDS instances based on the usage. This feature, when implemented in Dev environment, can reduce RDS costs by 30-40%. Most of the Dev instances dont need 24X7 availability. Using this feature we can control the start and stop time of an RDS instance based on your usage or based on working hours of your Dev team. This can be implemented in INTEGRATION, QA and PERF environment RDS fleets.

## Getting Started

This feature is implemented by using the RDS Tags. Using these tags, you need to mention the start and stop time of the RDS. 
* `start_time` - Signifies the time when RDS needs to be started. Timestamp format is `HH:MM:SS`.
* `stop_time` - Signifies the time when RDS needs to be stopped. Timestamp format is `HH:MM:SS`.
* `auto_schhedule` - Acts as flag to enable/disable this feature on the RDS instance. Valid values : TRUE/FALSE.  

Currently this feature assumes that the timestamp mentioned above are in **IST (UTC +0530)**.

### Architecture

![Alt text](/execution_flow.png?raw=true)

A Cloudwatch event will trigger the *Controller Lambda Function* every one hour and it will check the tags of each RDS. This lambda function then performs the necessary action by asynchronously invoking other lambda functions in parallel.

### Prerequisites

Dependency packages:
* **Pytz** - [Python Timezone package](https://pypi.python.org/pypi/pytz)

> This is already packaged as part of ZIP files in the repo.

### Installing

1. Import the CloudFormation template and the *ZIP packages* into an S3 Bucket of a particular *region*.
2. Create a CloudFormation Stack and provide the S3 path of the template and pass the region.
3. Once the stack creation is complete, carry out an lambda TestEvent.

> NOTE: The S3 bucket, the CloudFormation Stack and the Lambda functions must be created in the same **REGION**.

## Running the tests
1. Add the below tags to an RDS instance in the *region* where you have the setup ready.
```
start_time: 06:00:00
stop_time: 21:00:00
auto_schedule: TRUE
```

2. You can simulate a lambda testevent by passing the below json to *controller_lambda_function*.

```
{
  "db_instance_region": "us-east-1"
}
```

### Repo Structure

- `scripts` : *location of python lambda scripts.*
- `templates` : *location of cloudformation template.*
- `packages` : *location of all *ZIP* files which are includes 3PP libararies.*

### Built With
* AWS Lambda
* AWS CLoudwatch
* AWS IAM
* Python 3.6

### Authors

* **Madhukar Mohanraju** - *Initial work* - [MadhukarMohanraju](https://github.com/madhukar-mohanraju)

### License

This project is licensed under the MIT License - see the [LICENSE.md](/LICENSE?raw=true) file for details

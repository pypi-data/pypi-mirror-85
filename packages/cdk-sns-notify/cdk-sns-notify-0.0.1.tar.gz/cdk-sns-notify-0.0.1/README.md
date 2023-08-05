[![NPM version](https://badge.fury.io/js/cdk-sns-notify.svg)](https://badge.fury.io/js/cdk-sns-notify)
[![PyPI version](https://badge.fury.io/py/cdk-sns-notify.svg)](https://badge.fury.io/py/cdk-sns-notify)
![Release](https://github.com/clarencetw/cdk-sns-notify/workflows/Release/badge.svg)

# cdk-sns-notify

A CDK construct library to send line notify or discord webhook

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_sns as sns
import aws_cdk.aws_cloudwatch as cloudwatch
import aws_cdk.aws_cloudwatch_actions as cw_actions

from cdk_sns_notify import SnsNotify

topic = sns.Topic(stack, "Topic")

metric = cloudwatch.Metric(
    namespace="AWS/EC2",
    metric_name="CPUUtilization",
    dimensions={
        "InstanceId": instance.instance_id
    },
    period=cdk.Duration.minutes(1)
)

alarm = cloudwatch.Alarm(stack, "Alarm",
    metric=metric,
    threshold=5,
    evaluation_periods=1
)

alarm.add_alarm_action(cw_actions.SnsAction(topic))

sns_line_notify = SnsNotify(stack, "sns-line-notify",
    line_notify_token="lineNotifyToken"
)
```

# Deploy

```sh
cdk deploy
```

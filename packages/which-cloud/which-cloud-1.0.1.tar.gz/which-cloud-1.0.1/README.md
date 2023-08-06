# which-cloud

Given an ip address, return which cloud provider it belongs to.

## Preprocess

Convert raw ip ranges of different platforms into a single pickle file to speed up data load time.

## Data Sources

### GCP

- document: <https://cloud.google.com/compute/docs/faq#find_ip_range>
- data: <https://www.gstatic.com/ipranges/cloud.json>

### AWS

- document: <https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html>
- data: <https://ip-ranges.amazonaws.com/ip-ranges.json>

### Azure

- document: <https://www.microsoft.com/en-us/download/details.aspx?id=56519>
- data: <https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20201109.json>

### Digital Ocean

> Not implemented yet.

No official documented ip ranges ([thread](https://www.digitalocean.com/community/questions/please-publish-the-digitalocean-public-ip-ranges))

### IBM

> Not implemented yet.

- document: <https://cloud.ibm.com/docs/hardware-firewall-dedicated?topic=hardware-firewall-dedicated-ibm-cloud-ip-ranges>
- data: no formatted data source

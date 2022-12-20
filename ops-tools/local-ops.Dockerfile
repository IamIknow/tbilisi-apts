FROM amazon/aws-cli:2.0.43


RUN yum install -y jq gzip nano tar git unzip wget

RUN yum install -y yum-utils shadow-utils
RUN yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
RUN yum -y install terraform

ENTRYPOINT [ "/bin/sh" ]

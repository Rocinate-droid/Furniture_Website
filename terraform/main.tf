terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
        }
    }
}

provider "aws" {
  region = "us-east-1"
}

module "vpc" {
  source = "./modules/vpc"
  vpc-cidr = "10.0.2.0/24"
  subnet-cidr = "10.0.2.0/24"
}

module "security-group" {
  source = "./modules/security-group"
  vpc_id = module.vpc.vpc_id
}

module "ec2" {
  source = "./modules/ec2"
  instance_type = "t2.micro"
  key_name = "demokey"
  ami = "ami-020cba7c55df1f615"
  sg-id = module.security-group.sg-id
  subnet_id = module.vpc.subnet-id
}
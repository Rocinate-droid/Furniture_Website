resource "aws_instance" "module_host" {
    ami = var.ami
    instance_type = var.instance_type
    key_name = var.key_name

    primary_network_interface {
        network_interface_id = aws_network_interface.niw-prod.id
    }
    tags = {
        Name = "module-prod"
    }

    user_data = <<-EOF
            #!/bin/bash
            apt update -y
            apt upgrade -y
            apt install -y python3-pip python3-venv
            apt install openjdk-21-jdk -y
            wget -O /etc/apt/keyrings/jenkins-keyring.asc \
            https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
            echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc]" \
            https://pkg.jenkins.io/debian-stable binary/ | tee \
            /etc/apt/sources.list.d/jenkins.list > /dev/null
            apt update -y
            apt install jenkins -y
            EOF
}
resource "aws_network_interface" "niw-prod" {
    subnet_id       = var.subnet_id
    security_groups = [var.sg-id]
}

resource "aws_eip" "eip-prod" {
domain = "vpc"
}

resource "aws_eip_association" "eip-assoc-prod" {
    allocation_id = aws_eip.eip-prod.id
    network_interface_id = aws_network_interface.niw-prod.id
} 

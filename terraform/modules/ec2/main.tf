resource "aws_instance" "django-host" {
  ami = var.ami
  instance_type = var.instance_type
  key_name = var.key_name

  network_interface {
    network_interface_id = aws_network_interface.niw-master.id
    device_index = 0
    }

    tags = {
      Name = "django-instance"
    }

  user_data = <<-EOF
            #!/bin/bash
            apt update -y
            apt upgrade -y
            apt install -y python3-pip python3-venv
            EOF

}

resource "aws_ec2_instance_state" "test" {
  instance_id = aws_instance.django-host.id
  state       = "running"
}

resource "aws_network_interface" "niw-master" {
  subnet_id       = var.subnet_id
  security_groups = [var.sg-id]
}

resource "aws_eip" "eip-master" {
    domain = "vpc"
}

resource "aws_eip_association" "eip-assoc-master" {
    allocation_id = aws_eip.eip-master.id
    network_interface_id = aws_network_interface.niw-master.id
}


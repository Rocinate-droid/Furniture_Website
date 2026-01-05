resource "aws_lightsail_instance" "module_lg_server" {
  name              = "module-server"
  availability_zone = "us-east-1a"
  blueprint_id      = "ubuntu_22_04"
  bundle_id         = "micro_3_0"
  key_pair_name     = "module_key"

  user_data = "apt update -y && apt upgrade -y && apt install -y python3-pip python3-venv && apt install openjdk-21-jdk -y && apt install nginx -y"
}

resource "aws_lightsail_static_ip" "module_ip" {
  name = "module_ip"
}
resource "aws_lightsail_static_ip_attachment" "module_static_ip" {
  static_ip_name = aws_lightsail_static_ip.module_ip.id
  instance_name  = aws_lightsail_instance.module_lg_server.id
}
resource "aws_lightsail_instance_public_ports" "module_public_ports" {
    instance_name = aws_lightsail_instance.module_lg_server.id
    port_info {
      protocol = "tcp"
      from_port = 22
      to_port = 22
    }
    port_info {
      protocol = "tcp"
      from_port = 80
      to_port = 80
    }
    port_info {
      protocol = "tcp"
      from_port = 8000
      to_port = 8000
    }
    port_info {
      protocol = "tcp"
      from_port = 8080
      to_port = 8080
    }
    port_info {
      protocol = "tcp"
      from_port = 443
      to_port = 443
    }

}
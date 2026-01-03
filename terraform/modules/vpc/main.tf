resource "aws_vpc" "module-vpc" {
  cidr_block = var.vpc-cidr
  tags = {
            Name = "module-vpc"
        }
}

resource "aws_internet_gateway" "module-igw" {
        vpc_id = aws_vpc.module-vpc.id

        tags = {
            Name = "module-igw"
        }
}

resource  "aws_route_table" "module-route" {
        vpc_id = aws_vpc.module-vpc.id

        route { 
            cidr_block = "0.0.0.0/0"
            gateway_id = aws_internet_gateway.module-igw.id
        }

        tags = {
            Name = "module-route"
        }
}

resource "aws_route_table_association" "module_table-assoc" {
        subnet_id = aws_subnet.module-subnet.id
        route_table_id = aws_route_table.module-route.id
}

resource "aws_subnet" "module-subnet" {
        vpc_id = aws_vpc.module-vpc.id
        cidr_block = var.subnet-cidr

         tags = {
            Name = "module-subnet"
        }
}
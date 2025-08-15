resource "aws_vpc" "django-vpc" {
  cidr_block = var.vpc-cidr
  tags = {
            Name = "django-vpc"
        }
}

resource "aws_internet_gateway" "django-igw" {
        vpc_id = aws_vpc.django-vpc.id

        tags = {
            Name = "django-igw"
        }
}

resource  "aws_route_table" "django-route" {
        vpc_id = aws_vpc.django-vpc.id

        route { 
            cidr_block = "0.0.0.0/0"
            gateway_id = aws_internet_gateway.django-igw.id
        }

        tags = {
            Name = "django-route"
        }
}

resource "aws_route_table_association" "django_table-assoc" {
        subnet_id = aws_subnet.django-subnet.id
        route_table_id = aws_route_table.django-route.id
}

resource "aws_subnet" "django-subnet" {
        vpc_id = aws_vpc.django-vpc.id
        cidr_block = var.subnet-cidr

         tags = {
            Name = "django-subnet"
        }
}




output "vpc_id" {
  value = aws_vpc.django-vpc.id
}
output "subnet-id" {
  value = aws_subnet.django-subnet.id
}
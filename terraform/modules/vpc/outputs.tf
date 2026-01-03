output "vpc_id" {
  value = aws_vpc.module-vpc.id
}
output "subnet-id" {
  value = aws_subnet.module-subnet.id
}
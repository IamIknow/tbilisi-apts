
resource "aws_db_subnet_group" "tbilisi_apts" {
  name       = "tbilisi-apts"
  subnet_ids = module.vpc.public_subnets

  tags = {
    Name = "tbilisi_apts_subnet_group"
  }
}

resource "aws_security_group" "rds" {
  name   = "tbilisi-apts-rds"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "tbilisi_apts_rds"
  }
}

resource "aws_db_parameter_group" "tbilisi_apts" {
  name   = "tbilisi-apts"
  family = "postgres14"

  parameter {
    name  = "log_connections"
    value = "1"
  }
}

resource "aws_db_instance" "tbilisi_apts" {
  identifier             = "tbilisi-apts"
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "14.1"
  username               = "tbilisi_apts"
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.tbilisi_apts.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = aws_db_parameter_group.tbilisi_apts.name
  publicly_accessible    = true
  skip_final_snapshot    = true
}

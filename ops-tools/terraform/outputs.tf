output "rds_hostname" {
  description = "RDS instance hostname"
  value       = aws_db_instance.tbilisi_apts.address
  sensitive   = true
}

output "rds_port" {
  description = "RDS instance port"
  value       = aws_db_instance.tbilisi_apts.port
  sensitive   = true
}

output "rds_username" {
  description = "RDS instance root username"
  value       = aws_db_instance.tbilisi_apts.username
  sensitive   = true
}

output "ecr_scraper_repository_uri" {
  description = "Scraper service ECR repository URI"
  value       = aws_ecrpublic_repository.scraper_ecr_repo.repository_uri
}

output "ecr_scheduler_repository_uri" {
  description = "Scheduler service ECR repository URI"
  value       = aws_ecrpublic_repository.scheduler_ecr_repo.repository_uri
}

output "ecr_bot_repository_uri" {
  description = "Bot service ECR repository URI"
  value       = aws_ecrpublic_repository.bot_ecr_repo.repository_uri
}

output "endpoint" {
  value       = aws_eks_cluster.example.endpoint
}
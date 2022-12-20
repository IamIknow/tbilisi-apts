resource "aws_ecrpublic_repository" "scraper_ecr_repo" {
  repository_name = "tbilisi_apts_scraper"
}

resource "aws_ecrpublic_repository" "bot_ecr_repo" {
  repository_name = "tbilisi_apts_bot"
}

resource "aws_ecrpublic_repository" "scheduler_ecr_repo" {
  repository_name = "tbilisi_apts_scheduler"
}

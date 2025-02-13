package email

import (
	"net/smtp"
	"os"
)

var mailClient smtp.Auth

func InitEmailAuth() {
	mailClient = smtp.PlainAuth("", os.Getenv("EMAIL_USERNAME"), os.Getenv("EMAIL_PASSWORD"), "smtp.mail.ru")
}

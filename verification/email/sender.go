package email

import (
	"net/smtp"
	"os"
)

func sendMail(to string, body string) (err error) {
	msg := []byte("To: " + to + "\r\n" +
		"Subject: Подтверждение аккаунта\r\n" +
		"\r\n" + os.Getenv("SERVER_ADDR") + "/verify_code?email=" + to + "&link=" + body + "\r\n")

	err = smtp.SendMail(os.Getenv("SMTP_SERVER"), mailClient, os.Getenv("EMAIL_USERNAME"), []string{to}, msg)

	return
}

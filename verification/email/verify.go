package email

import (
	"errors"
	"net/mail"
	"verification/db"
)

func VerifyEmail(email string) (err error) {
	var user db.Users
	err = db.FindUserByEmail(email, &user)
	if err != nil {
		return
	}
	if user.Verificated {
		err = errors.New("email already verificated")
	} else {
		var randomSeq string = db.Generator.Generate(24)
		var userVerification db.EmailVerification
		err = db.FindUserVerificationByEmail(email, &userVerification)
		if err != nil {
			return
		} else if userVerification.SecretCode != "" {
			err = errors.New("verification link already requested")
			return
		} else {
			err = sendMail(email, randomSeq)
			if err != nil {
				return
			}
			db.Db.Model(&userVerification).Updates(map[string]interface{}{"secret_code": randomSeq})
		}
	}
	return
}

func ValidEmail(email string) bool {
	_, err := mail.ParseAddress(email)
	return err == nil
}

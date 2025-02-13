package db

import (
	"errors"
	"github.com/nicday/randSequence"
)

var Generator *randSequence.RandGenerator = randSequence.New()

func FindUserByEmail(email string, users *Users) (err error) {
	err = Db.Where("email = ?", email).First(users).Error
	if err != nil {
		err = errors.New("Email verification failed")
	} else if users.Email == "" {
		err = errors.New("User is not exists")
	}
	return
}

func FindUserVerificationByEmail(email string, userVerification *EmailVerification) (err error) {
	err = Db.Where("email = ?", email).First(userVerification).Error
	if err != nil {
		err = errors.New("Email verification failed")
	} else if userVerification.Email == "" {
		err = errors.New("Verification is not exists")
	}
	return
}

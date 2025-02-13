package db

import (
	"time"
)

type Users struct {
	UserID      uint   `gorm:"column:user_id;primaryKey"`
	Password    string `gorm:"column:password"`
	Username    string `gorm:"column:username"`
	Email       string `gorm:"column:email"`
	Avatar      string `gorm:"column:avatar"`
	GreenScores uint   `gorm:"column:green_scores"`
	GreenPoints uint   `gorm:"column:green_points"`
	Verificated bool   `gorm:"column:verificated"`
}

func (Users) TableName() string {
	return "users"
}

type EmailVerification struct {
	ID             uint      `gorm:"column:id;primaryKey"`
	Email          string    `gorm:"column:email"`
	SecretCode     string    `gorm:"column:secret_code"`
	ExpirationTime time.Time `gorm:"column:expiration_time"`
}

func (EmailVerification) TableName() string {
	return "email_verification"
}

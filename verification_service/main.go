package main

import (
	"errors"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"github.com/nicday/randSequence"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"net/http"
	"net/mail"
	"os"
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

var db *gorm.DB
var generator *randSequence.RandGenerator = randSequence.New()

func initDbConnection() {
	var link string = os.Getenv("DB_USERNAME") + ":" + os.Getenv("DB_PASSWORD") + "@tcp(" + os.Getenv("DB_HOST") + ":" + os.Getenv("DB_PORT") + ")/" + os.Getenv("DB_NAME") + "?charset=utf8mb4&parseTime=True&loc=Local"
	var err error
	db, err = gorm.Open(mysql.Open(link), &gorm.Config{})
	if err != nil {
		panic(err)
	}

}

func initDotenv(filename string) {
	var err error = godotenv.Load(filename)
	if err != nil {
		panic(err)
	}
	return
}

func findUserByEmail(email string, users *Users) (err error) {
	err = db.Where("email = ?", email).First(users).Error
	if err != nil {
		err = errors.New("Email verification failed")
	} else if users.Email == "" {
		err = errors.New("User is not exists")
	}
	return
}

func findUserVerificationByEmail(email string, userVerification *EmailVerification) (err error) {
	err = db.Where("email = ?", email).First(userVerification).Error
	if err != nil {
		err = errors.New("Email verification failed")
	} else if userVerification.Email == "" {
		err = errors.New("Verification is not exists")
	}
	return
}

func verifyEmail(email string) (err error) {
	var user Users
	err = findUserByEmail(email, &user)
	if err != nil {
		return
	}
	if user.Verificated {
		err = errors.New("email already verificated")
	} else {
		var randomSeq string = generator.Generate(24)
		var userVerification EmailVerification
		err = findUserVerificationByEmail(email, &userVerification)
		if err != nil {
			return
		} else if userVerification.SecretCode != "" {
			err = errors.New("verification link already requested")
			return
		} else {
			db.Model(&userVerification).Updates(map[string]interface{}{"secret_code": randomSeq})
		}
	}
	return
}

func validEmail(email string) bool {
	_, err := mail.ParseAddress(email)
	return err == nil
}

func verifyEmailRouter(c *gin.Context) {
	var email string = c.PostForm("email")
	if email == "" {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"message": "Email address is empty!"})
		return
	}
	if validEmail(email) {
		var err error = verifyEmail(email)
		if err != nil {
			c.IndentedJSON(http.StatusBadRequest, gin.H{"message": err.Error()})
		} else {
			c.IndentedJSON(http.StatusOK, gin.H{"email": email})
		}
	} else {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"message": "Email address is not valid"})
	}
}

func verifyByLinkRouter(c *gin.Context) {
	var email string = c.Query("email")
	var secret_link string = c.Query("link")
	var user Users

	var err error = findUserByEmail(email, &user)

	if user.Verificated {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"message": "email already verificated"})
	} else if err != nil {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"message": err.Error()})
	} else {
		var userVerification EmailVerification
		err = findUserVerificationByEmail(email, &userVerification)

		if err != nil {
			c.IndentedJSON(http.StatusBadRequest, gin.H{"message": err.Error()})
		} else if secret_link != userVerification.SecretCode {
			c.IndentedJSON(http.StatusBadRequest, gin.H{"message": "invalid secret link"})
		} else {
			db.Model(&user).Updates(map[string]interface{}{"verificated": 1})
			c.IndentedJSON(http.StatusOK, gin.H{"email": email})
		}

	}
}

func main() {
	initDotenv(".env")

	initDbConnection()
	router := gin.Default()

	router.POST("/verify", verifyEmailRouter)
	router.GET("/verify_code", verifyByLinkRouter)

	var err error = router.Run("localhost:8080")

	if err != nil {
		panic(err)
	}
}

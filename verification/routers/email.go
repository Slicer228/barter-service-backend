package routers

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"verification/db"
	emailPack "verification/email"
)

func verifyEmailRouter(c *gin.Context) { //POST
	var email string = c.PostForm("email")
	if email == "" {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"message": "Email address is empty!"})
		return
	}
	if emailPack.ValidEmail(email) {
		var err error = emailPack.VerifyEmail(email)
		if err != nil {
			c.IndentedJSON(http.StatusBadRequest, gin.H{"message": err.Error()})
		} else {
			c.IndentedJSON(http.StatusOK, gin.H{"email": email})
		}
	} else {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"message": "Email address is not valid"})
	}
}

func verifyByLinkRouter(c *gin.Context) { //GET
	var email string = c.Query("email")
	var secret_link string = c.Query("link")
	var user db.Users

	var err error = db.FindUserByEmail(email, &user)

	if user.Verificated {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"message": "email already verificated"})
	} else if err != nil {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"message": err.Error()})
	} else {
		var userVerification db.EmailVerification
		err = db.FindUserVerificationByEmail(email, &userVerification)

		if err != nil {
			c.IndentedJSON(http.StatusBadRequest, gin.H{"message": err.Error()})
		} else if secret_link != userVerification.SecretCode {
			c.IndentedJSON(http.StatusBadRequest, gin.H{"message": "invalid secret link"})
		} else {
			db.Db.Model(&user).Updates(map[string]interface{}{"verificated": 1})
			c.IndentedJSON(http.StatusOK, gin.H{"email": email})
		}

	}
}

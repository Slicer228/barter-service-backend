package routers

import (
	"github.com/gin-gonic/gin"
)

func Set_routers() {
	router := gin.Default()

	router.POST("/verify", verifyEmailRouter)
	router.GET("/verify_code", verifyByLinkRouter)

	err := router.Run("localhost:8080")

	if err != nil {
		panic(err)
	}
}

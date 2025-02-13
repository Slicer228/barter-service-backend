package main

import (
	"verification/db"
	"verification/email"
	"verification/routers"
)

func main() {
	initDotenv(".env")
	db.InitDbConnection()
	email.InitEmailAuth()
	routers.Set_routers()
}

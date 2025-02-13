package main

import (
	"github.com/joho/godotenv"
)

func initDotenv(filename string) {
	var err error = godotenv.Load(filename)
	if err != nil {
		panic(err)
	}
	return
}

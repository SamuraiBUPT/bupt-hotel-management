package routers

import (
	"backend_go/handlers"

	"github.com/gin-gonic/gin"
)

func SetupRoutes(router *gin.Engine) {
	api := router.Group("/api")
	{
		api.POST("/login", handlers.Login)
		api.POST("/rooms/checkIn", handlers.CheckIn)
		api.POST("/rooms/checkOut", handlers.CheckOut)
	}
}

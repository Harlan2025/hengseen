# FastAPI Health Check Endpoints

def add_health_check(app: FastAPI):
    @app.get("/health")
    async def health_check():
        return {
            "name": "衡简叙约",
            "version": "1.4.0",
            "mode": settings.MODE,
            "status": "running"
        }
    
    @app.get("/ready")
    async def readiness_check():
        return {"status": "ready"}
    
    @app.get("/live")
    async def liveness_check():
        return {"status": "live"}

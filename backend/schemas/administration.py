
# --- Pydantic Schemas ---
class AdminCreate(BaseModel):
    username: str
    password: str     # mot de passe en clair (sera hashé avant insertion)
    role: str
    description: str | None = None


class AdminResponse(BaseModel):
    id: int
    username: str
    role: str
    description: str | None = None

    class Config:
        from_attributes = True


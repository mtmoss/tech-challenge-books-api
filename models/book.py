from pydantic import BaseModel, Field
from typing import Optional

class BookBase(BaseModel):
    """Campos comuns a operações de criação/atualização."""
    title: str = Field(..., min_length=1, description="Título do livro")
    author: str = Field(..., min_length=1, description="Autor(a) do livro")
    year: Optional[int] = Field(None, ge=0, le=2100, description="Ano de publicação")
    isbn: Optional[str] = Field(None, min_length=5, description="ISBN (opcional)")

class BookCreate(BookBase):
    """Entrada para criar um livro (sem id)."""
    pass

class BookUpdate(BaseModel):
    """Entrada para atualizar um livro (todos os campos opcionais)."""
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)
    year: Optional[int] = Field(None, ge=0, le=2100)
    isbn: Optional[str] = Field(None, min_length=5)

class BookOut(BookBase):
    """Saída/retorno para o cliente (inclui id)."""
    id: int = Field(..., ge=1, description="Identificador interno")

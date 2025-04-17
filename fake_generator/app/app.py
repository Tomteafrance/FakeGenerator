from fastapi import FastAPI
from pydantic import BaseModel
from fake_generator.engine.fake_gen import FakeGenerator

app = FastAPI()

class GenerationRequest(BaseModel):
    schema_config: list
    num_rows: int
    seed: int

@app.post("/generate_data")
async def generate_data(request: GenerationRequest):
    generator = FakeGenerator(request.schema_config, seed=request.seed)
    return generator.generate_dataframe(request.num_rows).to_dict(orient='records')

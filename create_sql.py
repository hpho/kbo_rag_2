from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_openai import AzureChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain

# .env 로드
load_dotenv()

# 환경 변수
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
version = os.getenv("AZURE_OPENAI_API_VERSION")

if not all([api_key, endpoint, deployment, version]):
    raise ValueError("env check")

# LLM 설정
llm = AzureChatOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version=version,
    deployment_name=deployment
)

# DB 설정
engine = create_engine("sqlite:///kbo_stats.db")
db = SQLDatabase(engine)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# FastAPI 앱
app = FastAPI()

# 요청 Body 모델
class QueryRequest(BaseModel):
    question: str

# 라우팅
@app.post("/query")
async def ask_question(req: QueryRequest):
    try:
        result = db_chain.run(req.question)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

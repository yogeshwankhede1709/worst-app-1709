from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Utils
def strip_mongo_id(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    doc = dict(doc)
    doc.pop("_id", None)
    return doc

# Base models
class BaseDoc(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(extra="ignore")

# Status check (existing)
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_obj = StatusCheck(**input.model_dump())
    d = status_obj.model_dump()
    d["_id"] = status_obj.id
    await db.status_checks.insert_one(d)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**strip_mongo_id(x)) for x in status_checks]

# Blogs
class Blog(BaseDoc):
    title: str
    excerpt: str
    tags: List[str] = []
    author: str
    date: datetime = Field(default_factory=datetime.utcnow)

class BlogCreate(BaseModel):
    title: str
    excerpt: str
    tags: List[str] = []
    author: str
    date: Optional[datetime] = None

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    date: Optional[datetime] = None

@api_router.post("/blogs", response_model=Blog)
async def create_blog(b: BlogCreate):
    blog_data = b.model_dump()
    if blog_data.get("date") is None:
        blog_data["date"] = datetime.utcnow()
    obj = Blog(**blog_data)
    d = obj.model_dump()
    d["_id"] = obj.id
    await db.blogs.insert_one(d)
    return obj

@api_router.get("/blogs")
async def list_blogs(search: Optional[str] = None, tags: Optional[str] = None, page: int = 1, limit: int = 20):
    page = max(page, 1)
    limit = min(max(limit, 1), 100)
    query: Dict[str, Any] = {}
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"excerpt": {"$regex": search, "$options": "i"}},
            {"tags": {"$regex": search, "$options": "i"}},
        ]
    if tags:
        tag_list = [t.strip() for t in tags.split(',') if t.strip()]
        if tag_list:
            query["tags"] = {"$in": tag_list}

    total = await db.blogs.count_documents(query)
    cursor = db.blogs.find(query).sort("date", -1).skip((page - 1) * limit).limit(limit)
    items = [Blog(**strip_mongo_id(x)) for x in await cursor.to_list(length=limit)]
    return {"items": items, "page": page, "limit": limit, "total": total}

@api_router.get("/blogs/{id}", response_model=Blog)
async def get_blog(id: str):
    doc = await db.blogs.find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Blog not found")
    return Blog(**strip_mongo_id(doc))

@api_router.patch("/blogs/{id}", response_model=Blog)
async def update_blog(id: str, patch: BlogUpdate):
    update = {k: v for k, v in patch.model_dump(exclude_unset=True).items() if v is not None}
    update["updated_at"] = datetime.utcnow()
    res = await db.blogs.find_one_and_update({"_id": id}, {"$set": update}, return_document=True)
    if not res:
        raise HTTPException(status_code=404, detail="Blog not found")
    return Blog(**strip_mongo_id(res))

@api_router.delete("/blogs/{id}")
async def delete_blog(id: str):
    res = await db.blogs.delete_one({"_id": id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"ok": True}

# Tools
class Tool(BaseDoc):
    name: str
    category: str
    description: str
    url: str
    tags: List[str] = []

class ToolCreate(BaseModel):
    name: str
    category: str
    description: str
    url: str
    tags: List[str] = []

class ToolUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    tags: Optional[List[str]] = None

@api_router.post("/tools", response_model=Tool)
async def create_tool(t: ToolCreate):
    obj = Tool(**t.model_dump())
    d = obj.model_dump(); d["_id"] = obj.id
    await db.tools.insert_one(d)
    return obj

@api_router.get("/tools")
async def list_tools(category: Optional[str] = None, sort: str = Query("name", pattern="^(name|category)$"), page: int = 1, limit: int = 20):
    page = max(page, 1)
    limit = min(max(limit, 1), 100)
    query: Dict[str, Any] = {}
    if category and category.lower() != "all":
        query["category"] = category
    total = await db.tools.count_documents(query)
    sort_field = "name" if sort == "name" else "category"
    cursor = db.tools.find(query).sort(sort_field, 1).skip((page - 1) * limit).limit(limit)
    items = [Tool(**strip_mongo_id(x)) for x in await cursor.to_list(length=limit)]
    return {"items": items, "page": page, "limit": limit, "total": total}

@api_router.get("/tools/{id}", response_model=Tool)
async def get_tool(id: str):
    doc = await db.tools.find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Tool not found")
    return Tool(**strip_mongo_id(doc))

@api_router.patch("/tools/{id}", response_model=Tool)
async def update_tool(id: str, patch: ToolUpdate):
    update = {k: v for k, v in patch.model_dump(exclude_unset=True).items() if v is not None}
    update["updated_at"] = datetime.utcnow()
    res = await db.tools.find_one_and_update({"_id": id}, {"$set": update}, return_document=True)
    if not res:
        raise HTTPException(status_code=404, detail="Tool not found")
    return Tool(**strip_mongo_id(res))

@api_router.delete("/tools/{id}")
async def delete_tool(id: str):
    res = await db.tools.delete_one({"_id": id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"ok": True}

# Path
class PathStep(BaseDoc):
    label: str
    durationMin: int

class PathStepCreate(BaseModel):
    label: str
    durationMin: int

class PathStepUpdate(BaseModel):
    label: Optional[str] = None
    durationMin: Optional[int] = None

@api_router.post("/path", response_model=PathStep)
async def create_path_step(p: PathStepCreate):
    obj = PathStep(**p.model_dump())
    d = obj.model_dump(); d["_id"] = obj.id
    await db.path.insert_one(d)
    return obj

@api_router.get("/path", response_model=List[PathStep])
async def list_path():
    items = await db.path.find().sort("created_at", 1).to_list(1000)
    return [PathStep(**strip_mongo_id(x)) for x in items]

@api_router.patch("/path/{id}", response_model=PathStep)
async def update_path_step(id: str, patch: PathStepUpdate):
    update = {k: v for k, v in patch.model_dump(exclude_unset=True).items() if v is not None}
    update["updated_at"] = datetime.utcnow()
    res = await db.path.find_one_and_update({"_id": id}, {"$set": update}, return_document=True)
    if not res:
        raise HTTPException(status_code=404, detail="Path step not found")
    return PathStep(**strip_mongo_id(res))

@api_router.delete("/path/{id}")
async def delete_path_step(id: str):
    res = await db.path.delete_one({"_id": id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Path step not found")
    return {"ok": True}

# Community
class Channel(BaseDoc):
    name: str

class ChannelCreate(BaseModel):
    name: str

class Message(BaseDoc):
    channel: str
    author: str
    text: str
    ts: datetime = Field(default_factory=datetime.utcnow)

class MessageCreate(BaseModel):
    channel: str
    author: str
    text: str

@api_router.get("/community/channels", response_model=List[Channel])
async def list_channels():
    items = await db.channels.find().sort("name", 1).to_list(1000)
    return [Channel(**strip_mongo_id(x)) for x in items]

@api_router.post("/community/channels", response_model=Channel)
async def create_channel(c: ChannelCreate):
    obj = Channel(**c.model_dump())
    d = obj.model_dump(); d["_id"] = obj.id
    await db.channels.insert_one(d)
    return obj

@api_router.get("/community/messages")
async def list_messages(channel: str = Query(...), page: int = 1, limit: int = 50):
    page = max(page, 1)
    limit = min(max(limit, 1), 200)
    query = {"channel": channel}
    total = await db.messages.count_documents(query)
    cursor = db.messages.find(query).sort("ts", 1).skip((page - 1) * limit).limit(limit)
    items = [Message(**strip_mongo_id(x)) for x in await cursor.to_list(length=limit)]
    return {"items": items, "page": page, "limit": limit, "total": total}

@api_router.post("/community/messages", response_model=Message)
async def create_message(m: MessageCreate):
    obj = Message(**m.model_dump())
    d = obj.model_dump(); d["_id"] = obj.id
    await db.messages.insert_one(d)
    return obj

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
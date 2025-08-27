# API Contracts (Frontend ↔ Backend)

Scope
- Replace frontend mocks with real FastAPI + MongoDB endpoints (all routes prefixed with /api)
- Unauthenticated MVP suitable for microservices behind API Gateway later

Data Models (pydantic v2 style)
- Blog: { id, title, excerpt, tags[], author, date, created_at, updated_at }
- Tool: { id, name, category, description, url, tags[], created_at, updated_at }
- PathStep: { id, label, durationMin }
- Channel: { id, name }
- Message: { id, channel, author, text, ts }

General Notes
- All ids are UUID strings generated server-side
- Mongo docs include _id which is stripped in responses
- Timestamps are UTC ISO strings
- Pagination uses page (1-based) and limit

Endpoints
1) Blogs
- GET /api/blogs?search=&tags=tag1,tag2&page=1&limit=20
  - Returns: { items: Blog[], page, limit, total }
- POST /api/blogs
  - Body: { title, excerpt, tags[], author, date? }
  - Returns: Blog
- GET /api/blogs/{id}
- PATCH /api/blogs/{id}
  - Body: Partial of Blog fields (title/excerpt/tags/author/date)
- DELETE /api/blogs/{id}

2) Tools
- GET /api/tools?category=&sort=name|category&page=1&limit=20
  - Returns: { items: Tool[], page, limit, total }
- POST /api/tools { name, category, description, url, tags[] }
- GET /api/tools/{id}
- PATCH /api/tools/{id}
- DELETE /api/tools/{id}

3) Path
- GET /api/path
  - Returns: PathStep[]
- POST /api/path { label, durationMin }
- PATCH /api/path/{id}
- DELETE /api/path/{id}

4) Community (public, no auth)
- GET /api/community/channels -> Channel[]
- POST /api/community/channels { name } -> Channel
- GET /api/community/messages?channel=#general&page=1&limit=50 -> { items: Message[], page, limit, total }
- POST /api/community/messages { channel, author, text } -> Message

Frontend Mapping (current)
- Landing uses GET /api/ for health check only
- Blogs page: will swap mock.blogs with GET /api/blogs (search client-side & server-side compatible)
- Tools page: will use GET /api/tools with category/sort params
- Path page: will use GET /api/path
- Community: will use GET /api/community/channels + GET/POST /api/community/messages

Migration Plan
1. Implement endpoints (this commit)
2. Test backend via deep_testing_backend_v2
3. Update frontend to replace mock.js calls with axios(REACT_APP_BACKEND_URL)/api
4. Remove mock.js usage incrementally, keeping temporary fallback in UI during rollout

Sample Payloads
- Blog POST: { "title": "Supply Chain Security", "excerpt": "Why SBOMs matter.", "tags": ["slsa","sbom"], "author": "Maya" }
- Tool POST: { "name": "Trivy", "category": "Scanning", "description": "Scanner", "url": "https://example.com", "tags": ["containers"] }
- PathStep POST: { "label": "Kubernetes: Core Workloads", "durationMin": 300 }
- Channel POST: { "name": "#general" }
- Message POST: { "channel": "#general", "author": "You", "text": "Hello world" }

Error Format
- { "detail": "message" } for 4xx/5xx

Security
- CORS: wide-open for MVP; tighten later behind gateway/auth

Testing
- Create → Get → List with filters → Update → Delete for each entity
- Community: ensure message listing filters by channel and paginates
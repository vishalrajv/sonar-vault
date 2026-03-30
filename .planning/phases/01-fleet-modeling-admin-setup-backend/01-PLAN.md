---
wave: 1
depends_on: []
files_modified:
  - app/schemas.py
  - api/v1/auth.py
  - models/fleet.py
  - app/main.py
  - api/v1/hierarchy.py
autonomous: true
requirements_addressed:
  - AUTH-01
  - FLEET-01
---

# Phase 1: Fleet Modeling & Admin Setup (Backend)

<objective>
Establish the foundational backend logic: admin approval workflows, SQLite hierarchical data models for Platforms, Projects, and Subsystems, and the API to serve the entire hierarchy as a nested payload.
</objective>

## Task 1: Update Admin Approval Workflow
<read_first>
- app/schemas.py
- api/v1/auth.py
- .planning/phases/01-fleet-modeling-admin-setup-backend/01-CONTEXT.md
</read_first>

<action>
Modify `app/schemas.py`:
1. Update `UserSchema` to include the `department` and `role_designation` fields natively (`Optional[str] = None`).

Modify `api/v1/auth.py`:
2. Create an `UserApprovalUpdate` schema (or just Pydantic model at the top of the file) that contains `department: Optional[str] = None` and `role_designation: Optional[str] = None`.
3. Update the `POST /admin/approve-user/{user_id}` route to optionally accept `update_data: UserApprovalUpdate` as the request body to confirm or update the `department` and `role_designation` at the time of approval.
4. Ensure the endpoint still flips `is_approved = True` and `is_active = True`.
</action>

<acceptance_criteria>
- `app/schemas.py` contains `department: Optional[str]` inside `UserSchema`.
- `api/v1/auth.py` contains an approval endpoint that confirms/updates user roles upon approval via the request body.
</acceptance_criteria>

## Task 2: Create Fleet Database Models
<read_first>
- models/base.py
- app/main.py
- .planning/phases/01-fleet-modeling-admin-setup-backend/01-CONTEXT.md
</read_first>

<action>
Create `models/fleet.py`:
1. Import `Column`, `Integer`, `String`, `ForeignKey`, `Table` from `sqlalchemy`.
2. Import `relationship` from `sqlalchemy.orm`.
3. Import `Base` from `models.base`.
4. Define a many-to-many association table `platform_project_association = Table('platform_projects', Base.metadata, Column('platform_id', Integer, ForeignKey('platforms.id'), primary_key=True), Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True))`
5. Define `Platform` model (`__tablename__ = "platforms"`): `id`, `name`. Add a `projects` relationship using `secondary=platform_project_association`.
6. Define `Project` model (`__tablename__ = "projects"`): `id`, `name`. Add a `platforms` relationship using `secondary=platform_project_association`.
7. Define `Subsystem` model (`__tablename__ = "subsystems"`): `id`, `name`, `project_id` (ForeignKey `"projects.id"`), `platform_id` (ForeignKey `"platforms.id"`, `nullable=True`). Add appropriate foreign key relationships to Project and Platform.

Modify `app/main.py`:
8. Import `models.fleet` (and `models.user` if not already imported directly).
9. Import `engine` from `database.db` and call `models.base.Base.metadata.create_all(bind=engine)` after imports (or in a startup event/lifespan).
</action>

<acceptance_criteria>
- `models/fleet.py` exists and contains `Platform`, `Project`, and `Subsystem` models inheriting from `Base`.
- The many-to-many relationship translates Project-to-Platform mappings.
- `app/main.py` explicitly calls `create_all()` to generate tables in the db.
</acceptance_criteria>

## Task 3: Create Nested Hierarchy API
<read_first>
- models/fleet.py
- app/schemas.py
- .planning/phases/01-fleet-modeling-admin-setup-backend/01-CONTEXT.md
</read_first>

<action>
Modify `app/schemas.py`:
1. Define Pydantic models for the hierarchy response:
   - `SubsystemSchema`: `id: int`, `name: str`, `project_id: int`, `platform_id: Optional[int] = None`
   - `ProjectSchema`: `id: int`, `name: str`, `subsystems: list[SubsystemSchema] = []`
   - `PlatformSchema`: `id: int`, `name: str`, `projects: list[ProjectSchema] = []`
   - Use `ConfigDict(from_attributes=True)` on all of them.

Create `api/v1/hierarchy.py`:
2. Add a new `APIRouter` with prefix `/api/v1/hierarchy` and tags `["hierarchy"]`.
3. Create `GET /` endpoint that returns `list[PlatformSchema]`. 
4. Inject `db: Session = Depends(get_db)` and `current_user = Depends(get_current_active_user)`.
5. The endpoint logic MUST fetch all active Platforms and eager-load their linked Projects and related Subsystems using SQLAlchemy's `joinedload` (e.g. `db.query(Platform).options(joinedload(Platform.projects).joinedload(Project.subsystems)).all()`).

Modify `app/main.py`:
6. Import `api.v1.hierarchy.router as hierarchy_router`.
7. Call `app.include_router(hierarchy_router)`.
</action>

<acceptance_criteria>
- `app/schemas.py` contains `PlatformSchema`, `ProjectSchema`, `SubsystemSchema`.
- `api/v1/hierarchy.py` exists and exposes `GET /api/v1/hierarchy/` containing the full nested payload.
- `app/main.py` explicitly mounts the new hierarchy API router.
</acceptance_criteria>

<verification>
### Goal-Backward Verification
1. Is the many-to-many relationship established? Confirmed by `models/fleet.py` building `platform_projects` table.
2. Is the hierarchy served as a single payload? Confirmed by the `GET /api/v1/hierarchy/` nested schema approach returning the entire object tree.
3. Is admin approval secure and reflective of review? Confirmed by `POST /admin/approve-user` optionally accepting department changes.

### must_haves
- SQLite successfully generates `platforms`, `projects`, `subsystems`, and `platform_projects` tables automatically.
- Admin UI /pending-users call returns the `department` of unapproved users.
</verification>

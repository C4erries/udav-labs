from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.application.services import InsuranceService
from app.infrastructure.repositories import InsuranceRepository
from app.web.schemas import ClaimCreate, ClientCreate, PolicyCreate


router = APIRouter()
TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
service = InsuranceService(InsuranceRepository())


@router.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "clients_count": len(service.list_clients()),
            "policies_count": len(service.list_policies()),
            "claims_count": len(service.list_claims()),
        },
    )


@router.get("/clients", response_class=HTMLResponse)
def clients_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "clients.html",
        {"request": request, "clients": service.list_clients()},
    )


@router.get("/policies", response_class=HTMLResponse)
def policies_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "policies.html",
        {"request": request, "policies": service.list_policies()},
    )


@router.get("/claims", response_class=HTMLResponse)
def claims_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "claims.html",
        {"request": request, "claims": service.list_claims()},
    )


@router.get("/statistics", response_class=HTMLResponse)
def statistics_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "statistics.html",
        {"request": request, "statistics": service.get_statistics()},
    )


@router.get("/clients/new", response_class=HTMLResponse)
def new_client_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("client_form.html", {"request": request})


@router.post("/clients/new")
def create_client_from_form(
    full_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    birth_date: str = Form(...),
) -> RedirectResponse:
    data = ClientCreate(
        full_name=full_name,
        phone=phone,
        email=email,
        birth_date=birth_date,
    )
    service.create_client(data.model_dump())
    return RedirectResponse("/clients", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/policies/new", response_class=HTMLResponse)
def new_policy_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "policy_form.html",
        {"request": request, "clients": service.list_clients()},
    )


@router.post("/policies/new")
def create_policy_from_form(
    client_id: int = Form(...),
    policy_number: str = Form(...),
    product_type: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    premium: float = Form(...),
    insured_amount: float = Form(...),
) -> RedirectResponse:
    data = PolicyCreate(
        client_id=client_id,
        policy_number=policy_number,
        product_type=product_type,
        start_date=start_date,
        end_date=end_date,
        premium=premium,
        insured_amount=insured_amount,
    )
    service.create_policy(data.model_dump())
    return RedirectResponse("/policies", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/claims/new", response_class=HTMLResponse)
def new_claim_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "claim_form.html",
        {"request": request, "policies": service.list_policies()},
    )


@router.post("/claims/new")
def create_claim_from_form(
    policy_id: int = Form(...),
    claim_date: str = Form(...),
    description: str = Form(...),
    amount: float = Form(...),
    status_value: str = Form(..., alias="status"),
) -> RedirectResponse:
    data = ClaimCreate(
        policy_id=policy_id,
        claim_date=claim_date,
        description=description,
        amount=amount,
        status=status_value,
    )
    service.create_claim(data.model_dump())
    return RedirectResponse("/claims", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/api/clients")
def get_clients() -> list[dict]:
    return service.list_clients()


@router.post("/api/clients", status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreate) -> dict:
    return service.create_client(payload.model_dump())


@router.get("/api/policies")
def get_policies() -> list[dict]:
    return service.list_policies()


@router.post("/api/policies", status_code=status.HTTP_201_CREATED)
def create_policy(payload: PolicyCreate) -> dict:
    return service.create_policy(payload.model_dump())


@router.get("/api/claims")
def get_claims() -> list[dict]:
    return service.list_claims()


@router.post("/api/claims", status_code=status.HTTP_201_CREATED)
def create_claim(payload: ClaimCreate) -> dict:
    return service.create_claim(payload.model_dump())


@router.get("/api/statistics")
def get_statistics() -> dict[str, list[dict]]:
    return service.get_statistics()


@router.get("/api/export/{table_name}")
def export_table(table_name: str) -> Response:
    try:
        content = service.export_table_to_json(table_name)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return Response(content=content, media_type="application/json")


@router.post("/api/import/{table_name}")
async def import_table(table_name: str, request: Request) -> dict[str, int]:
    content = (await request.body()).decode("utf-8")
    try:
        inserted = service.import_table_from_json(table_name, content)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"inserted": inserted}

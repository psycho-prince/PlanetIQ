from fastapi import APIRouter
router=APIRouter()
@router.get('/')
def home(): return {'project':'PlanetIQ','version':'2.0.0'}
@router.get('/health')
def health(): return {'status':'ok'}

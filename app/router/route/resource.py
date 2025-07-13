from fastapi import APIRouter
from starlette.staticfiles import StaticFiles

from app.config import conf

router = APIRouter()

# NOT loaded since they don't get pulled unless loaded at base app??
# # Static Files
# editor_dir = f'{conf.static_dir}/res/js/editor'
# router.mount('/res/app/editor', StaticFiles(directory=editor_dir), name="editor")


@router.get("/res/app/editor/")
async def import_map():
    editor_root = f"{conf.static_root}/res/js/editor/"
    return {
        "imports": {
            "editor": f"{conf.static_root}/res/js/editor.mjs",
        },
        "scopes": {
            editor_root: {
                "": f"{conf.editor_root}",
            }
        }
    }

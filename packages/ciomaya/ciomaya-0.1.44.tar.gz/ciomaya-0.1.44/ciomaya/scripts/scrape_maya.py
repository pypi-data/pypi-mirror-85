"""
A basic scraper to collect paths from Maya nodes.
"""
import pymel.core as pm
import re
from ciomaya.lib import scraper_utils

 
ATTRS = {
    "AbcImport": {
        "AlembicNode": ["abc_File"]
    },
    "MayaBuiltin": {
        "file": ["computedFileTextureNamePattern"],
        "cacheFile": ["cachePath"],
        "gpuCache": ["cacheFileName"]
    }
}

TOKENS = (
    r"#+"  # image.####.exr - hash
    , r"_MAPID_"  # image_MAPID_.exr - mapid
    , r"%0\d+d"  # image.%04d.exr - percent
    , r"<UDIM>"  # image.<UDIM>.exr - udim_mari
    , r"<UVTILE>"  # image.<UVTILE>.exr - udim_mudbox
    , r"\$\d*U.*\$\d*V"  # image.u$2U_v$2V.exr or image.u$Uv$V.exr, etc - udim_vray
    , r"u<U>_v<V>"  # image.u<U>_v<V>.exr - udim_zbrush
    , r"u<U>_v<V>_<f>"  # image.u<U>_v<V>_<f>.exr - udim_zbrush_f
    , r"<f\d?>"  # image.<f>.exr or image.<f4>.exr - frame_seq
    , r"<FrameNum>"  # image.<FrameNum>.ext - Redshift
    , r"<Frame>"  # image.<Frame>.ext - Redshift
)


 
def run(_):
    """
    Find paths in Maya nodes.

    Since Maya nodes may be rendered by other renderers, and those renderers may
    support a variety of tokens, we include all tokens here. 

    Example: Renderman uses _MAPID_, but it could be found in a Maya file node. Leaky abstraction?
    Perhaps the better solution is to include the file node in the renderman scraper?

    Image file textures may have a sibling ".tx file".
    """

    paths = scraper_utils.get_paths(ATTRS)
    paths = scraper_utils.starize_tokens(paths, *TOKENS)
    paths = scraper_utils.expand_workspace(paths)
    paths = scraper_utils.extend_with_tx_paths(paths)
    paths.extend(_get_scene_files())

    return paths



def _get_scene_files():
    result = []
    depth_regex = re.compile(r".*{(\d+)\}$")
    for p in pm.listReferences(recursive=True):
        path = unicode(p)
        match = depth_regex.match(path)
        depth = 1
        if match:
            path = re.sub("{(\d+)\}$", "", path)
            depth = int(match.group(1))+1

        result.append({"path":path, "depth":depth})

    scene_name =  unicode(pm.sceneName())
    if scene_name:
        result.append({"path": scene_name, "depth":0})
    return result


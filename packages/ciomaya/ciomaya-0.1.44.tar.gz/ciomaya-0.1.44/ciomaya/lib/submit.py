"""
Submit.

"""
import json
import os
import sys
import traceback
from contextlib import contextmanager

import pymel.core as pm
from ciocore import conductor_submit
from ciocore.expander import Expander
from ciomaya.lib import const as k
from ciomaya.lib import layer_utils, validation, window
from ciocore.validator  import ValidationError
 

@contextmanager
def full_output(node):
    task_limit = node.attr("taskLimit").get()
    do_scrape = node.attr("doScrape").get()
    node.attr("taskLimit").set(-1)
    node.attr("doScrape").set(True)
    yield
    node.attr("taskLimit").set(task_limit)
    node.attr("doScrape").set(do_scrape)


@contextmanager
def transient_save(filepath, cleanup=True):
    original = pm.sceneName()
    pm.saveAs(filepath)
    yield
    pm.renameFile(original)
    if cleanup:
        try:
            os.remove(filepath)
        except OSError:
            pm.displayWarning("Couldn't cleanup file: {}".format(filepath))


def valid(node):

    try:
        validation.run(node)
    except ValidationError as ex:
        pm.displayWarning(str(ex))
        return False
    return True


def submit(node):
    # Dependencies are cached the first time calculated so that we dont have to
    # scrape for every layer.
    filepath = pm.sceneName()
    if filepath and node.attr("autosave").get():
        cleanup = node.attr("cleanupAutosave").get(
        ) and not node.attr("useUploadDaemon").get()
        filepath = _resolve_autosave_template(node)
        with transient_save(filepath, cleanup=cleanup):
            if valid(node):
                handle_submissions(node)
        return

    if pm.isModified():
        filepath = browse_save_as()
        if not filepath:
            pm.warning('No file Selected')
            return
        pm.saveAs(filepath)

    if valid(node):
        handle_submissions(node)


def handle_submissions(node):
    submissions = get_submissions(node)
    responses = do_submissions(submissions, node)
    window.show_submission_responses(responses)


def get_submissions(node):

    submissions = []
    layer_policy = node.attr("renderLayers").get()

    if layer_policy == k.CURRENT_LAYER:
        submissions.append(get_submission(node))
    else:
        for layer in layer_utils.get_renderable_legacy_layers():
            with layer_utils.layer_context(layer):
                submissions.append(get_submission(node))
    return list(filter(None, submissions))


def do_submissions(submissions, node):
    results = []
    show_tracebacks = node.attr("showTracebacks").get()
    for submission in submissions:
        try:
            remote_job = conductor_submit.Submit(submission)
            response, response_code = remote_job.main()
            results.append({"code": response_code, "response": response})
        except BaseException as ex:
            if show_tracebacks:
                msg = traceback.format_exc()
            else:
                msg = ex.message
            pm.displayError(msg)
            results.append({"code": "undefined", "response": msg})

    return results


def _resolve_autosave_template(node):

    scene_path = pm.sceneName()
    if not scene_path:
        scene_path = os.path.join(
            pm.workspace.getPath(),
            pm.workspace.fileRules.get("mayaAscii").split(":")[0],
            "untitled.ma"
        )

    scene_name = os.path.splitext(os.path.split(scene_path)[1])[0]
    context = {
        "Scene": scene_name,
        "scene": scene_name
    }
    expander = Expander(**context)
    resolved_name = expander.evaluate(node.attr("autosaveTemplate").get())
    return os.path.join(os.path.dirname(scene_path), "{}.ma".format(resolved_name))


def browse_save_as():
    filters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"

    entries = pm.fileDialog2(
        caption="Save File As",
        okCaption="Save As",
        fileFilter=filters,
        dialogStyle=2,
        fileMode=0,
        dir=os.path.dirname(pm.sceneName()))

    if entries:
        return entries[0]


def get_submission(node):
    out_attr = pm.PyNode(node).attr("output")
    with full_output(node):
        pm.dgdirty(out_attr)
        result = out_attr.get()
        if result:
            return json.loads(result)

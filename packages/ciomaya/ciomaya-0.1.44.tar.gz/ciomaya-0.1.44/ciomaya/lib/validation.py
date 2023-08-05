import abc
import importlib
import inspect
import os
import re
import pymel.core as pm
from ciocore.gpath import Path
from ciocore.gpath_list import GLOBBABLE_REGEX, PathList
from ciocore.validator import Validator, ValidationError


from ciomaya.lib import const as k
from ciomaya.lib import layer_utils
from ciomaya.lib import asset_cache
from ciomaya.lib import software

RENDERER_PACKAGE_REQUIREMENTS = {
    "arnold": "arnold-maya",
    "vray": "v-ray-maya",
    "renderman": "renderman-maya",
    "redshift": "redshift-maya",
}

WARNING_ICON = "ConductorWarning_18x18.png"
INFO_ICON = "ConductorInfo_18x18.png"


class ValidateCamera(Validator):
    def run(self, _):
        if not any(cam.attr("renderable").get() for cam in pm.ls(type="camera")):
            self.add_warning(
                "No renderable cameras. You may want to make at least one camera renderable in Render Settings.")


class ValidateUploadDaemon(Validator):
    def run(self, _):
        use_daemon = self._submitter.attr("useUploadDaemon").get()
        if not use_daemon:
            return
        module_path = pm.moduleInfo(path=True, moduleName="conductor")
        conductor_executable = os.path.join(
            os.path.dirname(module_path), "bin", "conductor")
        msg = 'This submission expects an uploader daemon to be running.\n After you press submit you can open a shell and enter: "{}" uploader'.format(
            conductor_executable)

        location = (self._submitter.attr("locationTag").get() or "").strip()
        if location:
            msg = 'This submission expects an uploader daemon to be running and set to a specific location tag.\nAfter you press submit you can open a shell and type: "{}" uploader --location {}'.format(
                conductor_executable,
                location)
        msg += "\nCheck the script editor for details"
        self.add_notice(msg)
        # By also printing the message, the user can copy paste
        # `/path/to/conductor uploader --location blah` from the console.
        print msg


class ValidateTaskCount(Validator):
    def run(self, _):
        count = self._submitter.attr("taskCount").get()
        if count > 1000:
            self.add_notice(
                "This submission contains over 1000 tasks ({}). Are you sure this is correct?".format(count))


class ValidateSelectedRenderer(Validator):
    def run(self, layername):

        current_renderer = pm.PyNode(
            "defaultRenderGlobals").attr("currentRenderer").get()
        try:
            required_package = RENDERER_PACKAGE_REQUIREMENTS[current_renderer]
        except KeyError:
            return

        self._submitter.attr("pluginSoftware").get()
        if required_package not in [p.split(" ")[0] for p in self._submitter.attr("pluginSoftware").get() if p]:
            self.add_warning(
                "The renderer for layer '{}' is set to '{}' but no versions of the plugin software '{}' are selected in the submitter. Are you sure this is correct?".format(layername, current_renderer, required_package))


class ValidateArnoldTiledTextures(Validator):
    def run(self, _):

        if not pm.PyNode("defaultRenderGlobals").attr("currentRenderer").get() == "arnold":
            return
        try:
            render_options = pm.PyNode("defaultArnoldRenderOptions")
        except pm.MayaNodeError:
            self.add_warning(
                "Current renderer is set to Arnold, but there's no defaultArnoldRenderOptions node")
            return

        msg = "It is recommended to generate Arnold Tiled Textures (TX files) locally as they can't be generated efficiently on the render nodes.\n"
        msg += "Use the Arnold Texture Manager to generate tx files, then set the following attributes in the Arnold tab of Render Settings.\n"
        msg += "Switch Auto Convert Textures to Off\n"
        msg += "Switch Use Existing TX Textures to On\n"

        auto_tx = render_options.attr("autotx").get()
        use_existing = render_options.attr("use_existing_tiled_textures").get()

        if auto_tx or not use_existing:
            self.add_warning(msg)


class ValidateArnoldRenderOptions(Validator):
    def run(self, _):
        if not pm.PyNode("defaultRenderGlobals").attr("currentRenderer").get() == "arnold":
            return

        try:
            render_options = pm.PyNode("defaultArnoldRenderOptions")
        except pm.MayaNodeError:
            self.add_warning(
                "Current renderer is set to Arnold, but there's no defaultArnoldRenderOptions node")
            return

        if not render_options.attr("threads_autodetect").get():
            self.add_warning(
                "Autodetect-Threads is turned off which could cause suboptimal machine usage and incur unnecessary costs. You may want to switch it back on in the Render Settings window, System tab.")

        if render_options.attr("denoiseBeauty").get():
            self.add_warning(
                "You have the Optix denoiser turned on. This will not work unless you also select a machine with a capable GPU. Also note, the Optix denoiser is not temporally coherent. To turn off Optix denoiser, enter the following in the MEL script editor: setAttr \"defaultArnoldRenderOptions.denoiseBeauty\" 0;")


class ValidateMissingAssets(Validator):

    def run(self, _):

        path_list = PathList()

        for gpath in asset_cache.data(self._submitter):

            # we can assunme that all globbable paths, (those containing glob
            # characters) cannot possibly represent missing files because they are
            # literally resolved  by checking what matches on disk. Ignore them.
            if not GLOBBABLE_REGEX.search(gpath.posix_path()):
                path_list.add(gpath)

        # path_list has taken care of deduplication
        missing = []
        for gpath in path_list:
            pp = gpath.posix_path()
            if not os.path.exists(pp):
                missing.append(pp)

        if missing:
            self.add_warning(
                "Some assets do not exist on disk. See the script editor for details. You can continue if you don't need them.")

            print "----- Conductor Asset Validation -------"
            for asset in missing:
                print "Missing: {}".format(asset)


class ValidateDestinationDirectory(Validator):
    def run(self, _):
        dest_directory = Path(self._submitter.attr(
            "destinationDirectory").get()).posix_path(with_drive=False)
        for gpath in asset_cache.data(self._submitter):
            asset_path = gpath.posix_path(with_drive=False)
            if asset_path.startswith(dest_directory):
                print "Some of your upload assets exist in the specified output destination directory\n. {} contains {}".format(
                    dest_directory, asset_path)
                self.add_error(
                    "The destination directory for output files contains assets that are in the upload list. This will cause your render to fail. See the script editor for details.")
                break
            if dest_directory.startswith(asset_path):
                print "You are trying to upload a directory that contains your destination directory.\n. {} contains {}".format(
                    asset_path, dest_directory)
                self.add_error(
                    "One of your assets is a directory that contains the specified output destination directory. This will cause your render to fail. See the script editor for details.")
                break


class ValidateGeneralRenderSettings(Validator):
    def run(self, _):
        if pm.PyNode("defaultRenderGlobals").attr("modifyExtension").get():
            self.add_warning(
                "You have 'renumber frames' turned on in render settings. All your files will be renamed to frame 1. We strongly recommend that you turn this setting OFF.")


class ValidateYeti(Validator):
    def run(self, _):
        # 
        if not (software.detect_yeti() and pm.about(ntOS=True)  and pm.ls(type="pgYetiMaya")  ):
            return
 
        msg = """You have the YETI plugin loaded and Yeti nodes in your scene.

Since Conductor render nodes run on Linux, you must ensure that every Yeti asset
can be found on the Linux filesystem. To do this, you should define the
PG_IMAGE_PATH variable and make sure it contains an entry for every directory
where your assets are, but with the drive letter removed and backslashes
replaced with forward slashes. Specifically, in the Submitter UI, open the Extra
Environment section and add an entry for each directory like the following
example:

Suppose you have these assets 
C:\\Users\\roberto\\textures\\texture.1.tif
C:\\Users\\roberto\\textures\\texture.2.tif
W:\\Production\\assets\\textures\\texture.3.tif

Then add these extra environment entries.

PG_IMAGE_PATH /Users/roberto/textures
PG_IMAGE_PATH /Production/assets/textures
"""
        self.add_notice("{}\nThis information has been printed to the script editor.".format(msg))

        print(msg)


# Implement more validators here
####################################
####################################


def run(node, dry_run=False):

    errors, warnings, notices = _run_validators(node)

    if errors:
        for error in errors:
            pm.displayError(error)
        msg = "There are some critical issues. See the script editor for details."
        raise ValidationError(msg)
    if notices or warnings:
        dialog_result = pm.layoutDialog(
            ui=pm.Callback(result_window, warnings, notices, dry_run), title="Validation")
        if not dialog_result == "okay":
            msg = "Submission cancelled by user."
            raise ValidationError(msg)


def _run_validators(node):

    layer_policy = node.attr("renderLayers").get()
    validators = [plugin(node) for plugin in Validator.plugins()]
    if layer_policy == k.CURRENT_LAYER:
        layers = [pm.editRenderLayerGlobals(q=True, currentRenderLayer=True)]
    else:
        layers = layer_utils.get_renderable_legacy_layers()
    for layer in layers:
        layername = layer_utils.get_layer_name(layer)
        with layer_utils.layer_context(layer):
            for validator in validators:
                validator.run(layername)

    errors = list(set.union(*[validator.errors for validator in validators]))
    warnings = list(
        set.union(*[validator.warnings for validator in validators]))
    notices = list(set.union(*[validator.notices for validator in validators]))
    return errors, warnings, notices


def result_window(warnings, notices, dry_run):
    form = pm.setParent(q=True)
    text = pm.text(
        label="Please read the notices before you continue!")

    if not dry_run:
        cancel_button = pm.button(label="Cancel", command=pm.Callback(
            pm.layoutDialog, dismiss="abort"))

    okay_label = "Close" if dry_run else "Submit"

    okay_button = pm.button(label=okay_label, command=pm.Callback(
        pm.layoutDialog, dismiss="okay"))

    scroll = pm.scrollLayout(bv=True)
    pm.setParent("..")

    pm.formLayout(form, edit=True, width=600)
    form.attachForm(text, "left", 2)
    form.attachForm(text, "right", 2)
    form.attachForm(text, "top", 2)
    form.attachNone(text, "bottom")

    form.attachForm(scroll, "left", 2)
    form.attachForm(scroll, "right", 2)
    form.attachControl(scroll, "top", 2, text)
    form.attachControl(scroll, "bottom", 2, okay_button)

    if not dry_run:
        form.attachForm(cancel_button, "left", 2)
        form.attachNone(cancel_button, "top")
        form.attachForm(cancel_button, "bottom", 2)
        form.attachPosition(cancel_button, "right", 2, 50)

    if not dry_run:
        form.attachPosition(okay_button, "left", 2, 50)
    else:
        form.attachForm(okay_button, "left", 2)

    form.attachForm(okay_button, "right", 2)
    form.attachNone(okay_button, "top")
    form.attachForm(okay_button, "bottom", 2)

    pm.setParent(scroll)
    col = pm.columnLayout(adj=True)

    for warning in warnings:
        _create_notice_widget(col, warning, WARNING_ICON)
        pm.setParent(col)
        pm.separator(height=8, style="in")
    for notice in notices:
        _create_notice_widget(col, notice, INFO_ICON)
        pm.setParent(col)
        pm.separator(height=8, style="in")
    pm.setParent(form)


def _create_notice_widget(column, notice, image):

    pm.setParent(column)

    form = pm.formLayout(nd=100, width=600)
    icon = pm.iconTextStaticLabel(style="iconOnly", image1=image)
    text = pm.text(label=notice.strip(), ww=True, align="left")

    form.attachForm(icon, "left", 2)
    form.attachNone(icon, "right")
    form.attachForm(icon, "top", 4)
    form.attachForm(icon, "bottom", 4)

    form.attachControl(text, "left", 10, icon)
    form.attachForm(text, "right", 2)
    form.attachForm(text, "top", 4)
    form.attachForm(text, "bottom", 4)

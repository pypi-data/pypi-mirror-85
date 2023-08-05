import pymel.core as pm
import os
import glob
import webbrowser
from ciomaya.lib import window
from ciomaya.lib import software
from ciomaya.lib import const as k

MAYA_PARENT_WINDOW = 'MayaWindow'
CONDUCTOR_MENU = 'ConductorMenu'
CONDUCTOR_DOCS = 'https://docs.conductortech.com/'
LOG_LEVELS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
DEFAULT_LOG_LEVEL = LOG_LEVELS[2]


def unload():

    if pm.menu(CONDUCTOR_MENU, q=True, exists=True):
        pm.menu(CONDUCTOR_MENU, e=True, deleteAllItems=True)
        pm.deleteUI(CONDUCTOR_MENU)


def load():
    unload()
    ConductorMenu()


class ConductorMenu(object):

    def __init__(self):
        if not pm.about(batch=True):
            pm.setParent(MAYA_PARENT_WINDOW)
            self.menu = pm.menu(CONDUCTOR_MENU, label="Conductor",
                                tearOff=True, pmc=pm.Callback(self.post_menu_command))
            self.jobs_menu = pm.menuItem(label="Submitter", subMenu=True)

            pm.setParent(self.menu, menu=True)

            pm.menuItem(divider=True)

            self.log_level_menu = self.build_log_level_menu()
            pm.setParent(self.menu, menu=True)

            pm.menuItem(divider=True)

            self.help_menu = pm.menuItem(label="Help", command=pm.Callback(
                webbrowser.open, CONDUCTOR_DOCS, new=2))
            self.about_menu = pm.menuItem(
                label="About", command=pm.Callback(window.show_about))

    def build_log_level_menu(self):
        result = pm.menuItem(label="Log level", subMenu=True)

        for level in LOG_LEVELS:
            pm.menuItem(label=level, radioButton=(level == DEFAULT_LOG_LEVEL),
                        command=pm.Callback(self.set_log_level, level))
        return result

    def post_menu_command(self):
        """
        Build the Select/Create submenu just before the menu is opened.
        """
        pm.setParent(self.jobs_menu,   menu=True)
        pm.menu(self.jobs_menu, edit=True, deleteAllItems=True)
        for j in pm.ls(type="conductorRender"):

            pm.menuItem(label="Select {}".format(str(j)),
                        command=pm.Callback(select_and_show, j))
        pm.menuItem(divider=True)

        pm.menuItem(label="Create",  command=pm.Callback(create_render_node))
        pm.setParent(self.menu, menu=True)

    def set_log_level(self, level):
        print "Setting Conductor log level to '{}'".format(level)


def create_render_node():
    node = pm.createNode("conductorRender")

    setup_render_node(node)
    select_and_show(node)


def select_and_show(node):
    pm.select(node)

    if not pm.mel.isAttributeEditorRaised():
        pm.mel.openAEWindow()


def setup_render_node(node):
    dest_path = os.path.join(
        pm.workspace(q=True, rd=True),

        pm.workspace.fileRules.get("images")
    )

    node.attr("destinationDirectory").set(dest_path)
    node.attr("hostSoftware").set(software.detect_host())


    ##### WE MUST DRY THIS UP ()TODAY! Why? Read John Ousterhout. #######
    # Combine with stuff ins AEsoftware Also - make each detection routine
    # discoverable through introspection, perhapes by making a SoftwareDetect()
    # class and deriving from it? 
    i = 0
    for plugin_software_name in filter(None, [
        software.detect_mtoa(),
        software.detect_rfm(),
        software.detect_vray(),
        software.detect_redshift(),
        software.detect_yeti(),
        
    ]):
        node.attr("pluginSoftware")[i].set(plugin_software_name)
        i += 1

    node.attr("taskTemplate").set(k.DEFAULT_TEMPLATE)
    node.attr("autosaveTemplate").set(k.DEFAULT_AUTOSAVE_TEMPLATE)
    node.attr("instanceTypeName").set(k.DEFAULT_INSTANCE_TYPE)
    node.attr("title").set(k.DEFAULT_TITLE)

    node.attr("customRange").set("1-10")
    node.attr("scoutFrames").set("auto:3")

    pm.Attribute("defaultRenderGlobals.startFrame") >> node.attr("startFrame")
    pm.Attribute("defaultRenderGlobals.endFrame") >> node.attr("endFrame")
    pm.Attribute("defaultRenderGlobals.byFrameStep") >> node.attr("byFrame")
    pm.Attribute("defaultRenderGlobals.animation") >> node.attr("animation")
    pm.Attribute("defaultRenderGlobals.currentRenderer") >> node.attr(
        "currentRenderer")
    pm.Attribute("renderLayerManager.currentRenderLayer") >> node.attr(
        "currentRenderLayer")
    pm.Attribute("time1.outTime") >> node.attr("currentFrame")

    # asset scrapers
    script_path = os.path.join(pm.moduleInfo(
        path=True, moduleName="conductor"), "scripts")

    files = sorted(glob.glob("{}/scrape_*.py".format(script_path)))
    for i, scraper in enumerate(files):
        scraper_name = os.path.splitext(os.path.basename(scraper))[0]
        node.attr("assetScrapers[{:d}].assetScraperName".format(i)).set(
            scraper_name)

"""
Handle the UI for environment:
"""

import pymel.core as pm
from ciomaya.lib import const as k
from ciomaya.lib.ae import AEcommon


def create_ui(node_attr):
    """Build static UI."""
    with AEcommon.ae_template():

        pm.rowLayout(
            width=290,
            numberOfColumns=2,
            columnWidth2=(k.AE_TEXT_WIDTH, 210),
            columnAttach=((1, "right", 0), (2, "both", 0)),
        )

        pm.text(label="")
        pm.button("environmentAddButton",
                  label="Add Environment Variable", height=24)
        pm.setParent("..")  # out rowLayout
        pm.separator()

        _form_layout(pm.text(label="Key", align="left", width=k.AE_TEXT_WIDTH),
                     pm.text(label="Value", align="left"),
                     pm.text(label="Excl", align="left", width=36),
                     pm.text(label="", width=36)
                     )

        pm.setParent("..")  # out _form_layout

        pm.columnLayout("environmentColumn", adj=True)

        pm.setParent("..")  # out columnLayout

        populate_ui(node_attr)


def populate_ui(node_attr):
    """Reconfigure action buttons when node changes."""

    attr = pm.Attribute(node_attr)
    widgets = _get_widgets()

    pm.button(widgets["button"], edit=True,
              command=pm.Callback(_add_entry, attr))

    for widget in pm.columnLayout(widgets["column"], q=True, childArray=True) or []:
        pm.deleteUI(widget)

    pm.setParent(widgets["column"])
    for attr_element in attr:

        key_att = attr_element.attr("extraEnvironmentKey")
        val_att = attr_element.attr("extraEnvironmentValue")
        exc_att = attr_element.attr("extraEnvironmentExclusive")

        key_ctl = pm.textField(
            placeholderText="VAR_NAME", width=k.AE_TEXT_WIDTH)
        val_ctl = pm.textField(placeholderText="Value")
        exc_ctl = pm.checkBox(label="", width=36)
        del_ctl = pm.symbolButton(
            image="smallTrash.xpm", width=36, command=pm.Callback(
                pm.removeMultiInstance, attr_element, b=True
            )
        )

        _form_layout(key_ctl, val_ctl, exc_ctl, del_ctl)
        pm.setParent("..")  # out _form_layout

        pm.connectControl(key_ctl, key_att)
        pm.connectControl(val_ctl, val_att)
        pm.connectControl(exc_ctl, exc_att)

        pm.setParent(widgets["column"])


def _get_widgets(parent=None):
    if not parent:
        parent = pm.setParent(q=True)
    return {
        "button":  AEcommon.find_ui("environmentAddButton", parent),
        "column":  AEcommon.find_ui("environmentColumn", parent)
    }


def _add_entry(attr):
    AEcommon.next_available_element_plug(
        attr).attr("extraEnvironmentKey").set("")


def _form_layout(*widgets):
    # There must be 3 widgets.
    form = pm.formLayout(nd=100)
    for widget in widgets:
        pm.control(widget, edit=True, parent=form)

    form.attachForm(widgets[0], "left", 2)
    form.attachNone(widgets[0], "right")
    form.attachForm(widgets[0], "top", 2)
    form.attachForm(widgets[0], "bottom", 2)

    form.attachControl(widgets[1], "left", 2, widgets[0])
    form.attachControl(widgets[1], "right", 2, widgets[2])
    form.attachForm(widgets[1], "top", 2)
    form.attachForm(widgets[1], "bottom", 2)

    form.attachNone(widgets[2], "left")
    form.attachControl(widgets[2], "right", 2, widgets[3])
    form.attachForm(widgets[2], "top", 2)
    form.attachForm(widgets[2], "bottom", 2)

    form.attachNone(widgets[3], "left")
    form.attachForm(widgets[3], "right", 2)
    form.attachForm(widgets[3], "top", 2)
    form.attachForm(widgets[3], "bottom", 2)

    return form


class AEenvironment(object):
    def __init__(self, aet):
        self.add_btn = None
        self.col = None
        aet.callCustom(self.create_ui, self.populate_ui, "extraEnvironment")

    def create_ui(self, node_attr):
        """Build static UI"""
        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)
        node = pm.Attribute(node_attr).node()
        pm.rowLayout(
            width=290,
            numberOfColumns=2,
            columnWidth2=(k.AE_TEXT_WIDTH, 210),
            columnAttach=((1, "right", 0), (2, "both", 0)),
        )

        pm.text(label="")
        self.add_btn = pm.button(
            label="Add Environment Variable",
            height=24,
            command=pm.Callback(on_add_btn, node),
        )
        pm.setParent("..")
        pm.separator()
        pm.rowLayout(
            width=290,
            numberOfColumns=4,
            adjustableColumn=2,
            columnWidth4=(k.AE_TEXT_WIDTH, 150, 36, 24),
            columnAttach=(
                (1, "both", 6),
                (2, "both", 6),
                (3, "both", 6),
                (4, "both", 0),
            ),
        )
        pm.text(label="Key", align="left")
        pm.text(label="Value", align="left")
        pm.text(label="Excl", align="left")
        pm.text(label="")
        pm.setParent("..")

        self.col = pm.columnLayout(adj=True)
        pm.setUITemplate(ppt=True)
        self.populate_ui(node_attr)

    def populate_ui(self, node_attr):
        """Reconfigure UI for the current node"""
        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)
        node = pm.Attribute(node_attr).node()
        pm.button(self.add_btn, edit=True,
                  command=pm.Callback(on_add_btn, node))

        for widget in pm.columnLayout(self.col, q=True, childArray=True) or []:
            pm.deleteUI(widget)

        pm.setParent(self.col)
        for attr in pm.Attribute(node_attr):
            pm.rowLayout(
                width=290,
                numberOfColumns=4,
                adjustableColumn=2,
                columnWidth4=(k.AE_TEXT_WIDTH, 150, 36, 24),
                columnAttach=(
                    (1, "both", 0),
                    (2, "both", 0),
                    (3, "both", 0),
                    (4, "both", 0),
                ),
            )

            key_att = attr.attr("extraEnvironmentKey")
            val_att = attr.attr("extraEnvironmentValue")
            exc_att = attr.attr("extraEnvironmentExclusive")

            key_tf = pm.textField(text=key_att.get(),
                                  placeholderText="VAR_NAME")
            val_tf = pm.textField(text=val_att.get(), placeholderText="Value")
            exc_cb = pm.checkBox(value=exc_att.get(), label="")
            pm.symbolButton(
                image="smallTrash.xpm", command=pm.Callback(on_remove_var, attr)
            )

            pm.textField(
                key_tf,
                edit=True,
                changeCommand=pm.Callback(on_text_changed, key_tf, key_att),
            )
            pm.textField(
                val_tf,
                edit=True,
                changeCommand=pm.Callback(on_text_changed, val_tf, val_att),
            )
            pm.checkBox(
                exc_cb,
                edit=True,
                changeCommand=pm.Callback(on_excl_cb_changed, exc_cb, exc_att),
            )

            pm.setParent(self.col)

        pm.setUITemplate(ppt=True)


def on_add_btn(node):
    indices = node.attr("extraEnvironment").getArrayIndices()
    next_available = next(a for a, b in enumerate(indices + [-1]) if a != b)
    node.attr("extraEnvironment")[next_available].attr(
        "extraEnvironmentKey").set("")
    node.attr("extraEnvironment")[next_available].attr(
        "extraEnvironmentValue").set("")


def on_text_changed(text_field, attribute):
    val = pm.textField(text_field, q=True, text=True)
    attribute.set(val)


def on_excl_cb_changed(checkbox, attribute):
    val = pm.checkBox(checkbox, q=True, value=True)
    attribute.set(val)


def on_remove_var(attribute):
    pm.removeMultiInstance(attribute, b=True)

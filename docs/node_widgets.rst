Node Embedded Widgets
#####################

Node embedded widgets are the widgets that can be embedded into a
:class:`nodegraph.BaseNode` and displayed in the node graph.

See :ref:`Embedding Custom Widgets` example to adding your own widget into a node.

NodeBaseWidget
**************

.. autoclass:: nodegraph.NodeBaseWidget
    :members:
    :exclude-members: node, setToolTip, type_, value, widget

-----

Below are builtin node widgets inherited from :class:`nodegraph.NodeBaseWidget`

NodeCheckBox
************

.. autoclass:: nodegraph.widgets.node_widgets.NodeCheckBox
    :members:
    :exclude-members: widget, type_

NodeComboBox
************

.. autoclass:: nodegraph.widgets.node_widgets.NodeComboBox
    :members:
    :exclude-members: widget, type_

NodeLineEdit
************

.. autoclass:: nodegraph.widgets.node_widgets.NodeLineEdit
    :members:
    :exclude-members: widget, type_

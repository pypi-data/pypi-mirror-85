from fury.ui import UI, Rectangle2D, TextBlock2D, TextBox2D, Checkbox


class CheckBox2D(UI):
    """ UI component that allows the user to select items from a list.
    Attributes
    ----------
    on_change: function
        Callback function for when the selected items have changed.
    """

    def __init__(self, values, position=(0, 0), size=(100, 300),
                 multiselection=True, reverse_scrolling=False,
                 font_size=20, line_spacing=1.4,
                 text_color=(0.2, 0.2, 0.2),
                 selected_color=(0.9, 0.6, 0.6),
                 unselected_color=(0.6, 0.6, 0.6),
                 scroll_bar_active_color=(0.6, 0.2, 0.2),
                 scroll_bar_inactive_color=(0.9, 0.0, 0.0),
                 background_opacity=1.):
        """
        Parameters
        ----------
        values: list of objects
            Values used to populate this listbox. Objects must be castable
            to string.
        position : (float, float)
            Absolute coordinates (x, y) of the lower-left corner of this
            UI component.
        size : (int, int)
            Width and height in pixels of this UI component.
        multiselection: {True, False}
            Whether multiple values can be selected at once.
        reverse_scrolling: {True, False}
            If True, scrolling up will move the list of files down.
        font_size: int
            The font size in pixels.
        line_spacing: float
            Distance between listbox's items in pixels.
        text_color : tuple of 3 floats
        selected_color : tuple of 3 floats
        unselected_color : tuple of 3 floats
        scroll_bar_active_color : tuple of 3 floats
        scroll_bar_inactive_color : tuple of 3 floats
        background_opacity : float
        """
        self.view_offset = 0
        self.slots = []
        self.selected = []

        self.panel_size = size
        self.font_size = font_size
        self.line_spacing = line_spacing
        self.slot_height = int(self.font_size * self.line_spacing)

        self.text_color = text_color
        self.selected_color = selected_color
        self.unselected_color = unselected_color
        self.background_opacity = background_opacity

        # self.panel.resize(size)
        self.values = values
        self.multiselection = multiselection
        self.last_selection_idx = 0
        self.reverse_scrolling = reverse_scrolling
        super(CheckBox2D, self).__init__()

        denom = len(self.values) - self.nb_slots
        if not denom:
            denom += 1
        self.scroll_step_size = (self.slot_height * self.nb_slots -
                                 self.scroll_bar.height) / denom

        self.scroll_bar_active_color = scroll_bar_active_color
        self.scroll_bar_inactive_color = scroll_bar_inactive_color
        self.scroll_bar.color = self.scroll_bar_inactive_color
        self.scroll_bar.opacity = self.background_opacity

        self.position = position
        self.scroll_init_position = 0
        self.update()

        # Offer some standard hooks to the user.
        self.on_change = lambda: None

    def _setup(self):
        """ Setup this UI component.
        Create the ListBox (Panel2D) filled with empty slots (ListBoxItem2D).
        """
        self.margin = 10
        size = self.panel_size
        font_size = self.font_size
        # Calculating the number of slots.
        self.nb_slots = int((size[1] - 2 * self.margin) // self.slot_height)

        # This panel facilitates adding slots at the right position.
        self.panel = Panel2D(size=size, color=(1, 1, 1))

        # Add a scroll bar
        scroll_bar_height = self.nb_slots * (size[1] - 2 * self.margin) \
            / len(self.values)
        self.scroll_bar = Rectangle2D(size=(int(size[0]/20),
                                      scroll_bar_height))
        if len(self.values) <= self.nb_slots:
            self.scroll_bar.set_visibility(False)
        self.panel.add_element(
            self.scroll_bar, size - self.scroll_bar.size - self.margin)

        # Initialisation of empty text actors
        slot_width = size[0] - self.scroll_bar.size[0] - \
            2 * self.margin - self.margin
        x = self.margin
        y = size[1] - self.margin
        for _ in range(self.nb_slots):
            y -= self.slot_height
            item = CheckBoxItem2D(list_box=self,
                                  size=(slot_width, self.slot_height),
                                  text_color=self.text_color,
                                  selected_color=self.selected_color,
                                  unselected_color=self.unselected_color,
                                  background_opacity=self.background_opacity)
            item.textblock.font_size = font_size
            self.slots.append(item)
            self.panel.add_element(item, (x, y + self.margin))

        # Add default events listener for this UI component.
        self.scroll_bar.on_left_mouse_button_pressed = \
            self.scroll_click_callback
        self.scroll_bar.on_left_mouse_button_released = \
            self.scroll_release_callback
        self.scroll_bar.on_left_mouse_button_dragged = \
            self.scroll_drag_callback

        # Handle mouse wheel events on the panel.
        up_event = "MouseWheelForwardEvent"
        down_event = "MouseWheelBackwardEvent"
        if self.reverse_scrolling:
            up_event, down_event = down_event, up_event  # Swap events

        self.add_callback(self.panel.background.actor, up_event,
                          self.up_button_callback)
        self.add_callback(self.panel.background.actor, down_event,
                          self.down_button_callback)

        # Handle mouse wheel events on the slots.
        for slot in self.slots:
            self.add_callback(slot.background.actor, up_event,
                              self.up_button_callback)
            self.add_callback(slot.background.actor, down_event,
                              self.down_button_callback)
            self.add_callback(slot.textblock.actor, up_event,
                              self.up_button_callback)
            self.add_callback(slot.textblock.actor, down_event,
                              self.down_button_callback)

    def resize(self, size):
        pass

    def _get_actors(self):
        """ Get the actors composing this UI component.
        """
        return self.panel.actors

    def _add_to_scene(self, scene):
        """ Add all subcomponents or VTK props that compose this UI component.
        Parameters
        ----------
        scene : scene
        """
        self.panel.add_to_scene(scene)

    def _get_size(self):
        return self.panel.size

    def _set_position(self, coords):
        """ Position the lower-left corner of this UI component.
        Parameters
        ----------
        coords: (float, float)
            Absolute pixel coordinates (x, y).
        """
        self.panel.position = coords

    def up_button_callback(self, i_ren, _obj, _list_box):
        """ Pressing up button scrolls up in the combo box.
        Parameters
        ----------
        i_ren: :class:`CustomInteractorStyle`
        obj: :class:`vtkActor`
            The picked actor
        _list_box: :class:`ListBox2D`
        """
        if self.view_offset > 0:
            self.view_offset -= 1
            self.update()
            scroll_bar_idx = self.panel._elements.index(self.scroll_bar)
            self.scroll_bar.center = (self.scroll_bar.center[0],
                                      self.scroll_bar.center[1] +
                                      self.scroll_step_size)
            self.panel.element_offsets[scroll_bar_idx] = (
                self.scroll_bar,
                (self.scroll_bar.position - self.panel.position))

        i_ren.force_render()
        i_ren.event.abort()  # Stop propagating the event.

    def down_button_callback(self, i_ren, _obj, _list_box):
        """ Pressing down button scrolls down in the combo box.
        Parameters
        ----------
        i_ren: :class:`CustomInteractorStyle`
        obj: :class:`vtkActor`
            The picked actor
        _list_box: :class:`ListBox2D`
        """
        view_end = self.view_offset + self.nb_slots
        if view_end < len(self.values):
            self.view_offset += 1
            self.update()
            scroll_bar_idx = self.panel._elements.index(self.scroll_bar)
            self.scroll_bar.center = (self.scroll_bar.center[0],
                                      self.scroll_bar.center[1] -
                                      self.scroll_step_size)
            self.panel.element_offsets[scroll_bar_idx] = (
                self.scroll_bar,
                (self.scroll_bar.position - self.panel.position))

        i_ren.force_render()
        i_ren.event.abort()  # Stop propagating the event.

    def scroll_click_callback(self, i_ren, _obj, _rect_obj):
        """ Callback to change the color of the bar when it is clicked.
        Parameters
        ----------
        i_ren: :class:`CustomInteractorStyle`
        obj: :class:`vtkActor`
            The picked actor
        _rect_obj: :class:`Rectangle2D`
        """
        self.scroll_bar.color = self.scroll_bar_active_color
        self.scroll_init_position = i_ren.event.position[1]
        i_ren.force_render()
        i_ren.event.abort()

    def scroll_release_callback(self, i_ren, _obj, _rect_obj):
        """ Callback to change the color of the bar when it is released.
        Parameters
        ----------
        i_ren: :class:`CustomInteractorStyle`
        obj: :class:`vtkActor`
            The picked actor
        rect_obj: :class:`Rectangle2D`
        """
        self.scroll_bar.color = self.scroll_bar_inactive_color
        i_ren.force_render()

    def scroll_drag_callback(self, i_ren, _obj, _rect_obj):
        """ Dragging scroll bar in the combo box.
        Parameters
        ----------
        i_ren: :class:`CustomInteractorStyle`
        obj: :class:`vtkActor`
            The picked actor
        rect_obj: :class:`Rectangle2D`
        """
        position = i_ren.event.position
        offset = int((position[1] - self.scroll_init_position) /
                     self.scroll_step_size)
        if offset > 0 and self.view_offset > 0:
            offset = min(offset, self.view_offset)

        elif offset < 0 and (
                self.view_offset + self.nb_slots < len(self.values)):
            offset = min(-offset,
                         len(self.values) - self.nb_slots - self.view_offset)
            offset = - offset
        else:
            return

        self.view_offset -= offset
        self.update()
        scroll_bar_idx = self.panel._elements.index(self.scroll_bar)
        self.scroll_bar.center = (self.scroll_bar.center[0],
                                  self.scroll_bar.center[1] +
                                  offset * self.scroll_step_size)

        self.scroll_init_position += offset * self.scroll_step_size

        self.panel.element_offsets[scroll_bar_idx] = (
            self.scroll_bar, (self.scroll_bar.position - self.panel.position))
        i_ren.force_render()
        i_ren.event.abort()

    def update(self):
        """ Refresh listbox's content. """
        view_start = self.view_offset
        view_end = view_start + self.nb_slots
        values_to_show = self.values[view_start:view_end]

        # Populate slots according to the view.
        for i, choice in enumerate(values_to_show):
            slot = self.slots[i]
            slot.element = choice
            slot.set_visibility(True)
            if slot.element in self.selected:
                slot.select()
            else:
                slot.deselect()

        # Flush remaining slots.
        for slot in self.slots[len(values_to_show):]:
            slot.element = None
            slot.set_visibility(False)
            slot.deselect()

    def update_scrollbar(self):
        """ Change the scroll-bar height when the values
        in the listbox change
        """
        self.scroll_bar.set_visibility(True)

        self.scroll_bar.height = self.nb_slots * \
            (self.panel_size[1] - 2 * self.margin) / len(self.values)

        self.scroll_step_size = (self.slot_height * self.nb_slots -
                                 self.scroll_bar.height) \
            / (len(self.values) - self.nb_slots)

        self.panel.update_element(
            self.scroll_bar, self.panel_size - self.scroll_bar.size -
            self.margin)

        if len(self.values) <= self.nb_slots:
            self.scroll_bar.set_visibility(False)

    def clear_selection(self):
        del self.selected[:]

    def select(self, item, multiselect=False, range_select=False):
        """ Select the item.
        Parameters
        ----------
        item: ListBoxItem2D's object
            Item to select.
        multiselect: {True, False}
            If True and multiselection is allowed, the item is added to the
            selection.
            Otherwise, the selection will only contain the provided item unless
            range_select is True.
        range_select: {True, False}
            If True and multiselection is allowed, all items between the last
            selected item and the current one will be added to the selection.
            Otherwise, the selection will only contain the provided item unless
            multi_select is True.
        """
        selection_idx = self.values.index(item.element)
        if self.multiselection and range_select:
            self.clear_selection()
            step = 1 if selection_idx >= self.last_selection_idx else -1
            for i in range(self.last_selection_idx,
                           selection_idx + step,
                           step):
                self.selected.append(self.values[i])

        elif self.multiselection and multiselect:
            if item.element in self.selected:
                self.selected.remove(item.element)
            else:
                self.selected.append(item.element)
            self.last_selection_idx = selection_idx

        else:
            self.clear_selection()
            self.selected.append(item.element)
            self.last_selection_idx = selection_idx

        self.on_change()  # Call hook.
        self.update()


class CheckBoxItem2D(UI):
    """ The text displayed in a listbox. """

    def __init__(self, list_box, size,
                 text_color=(1.0, 0.0, 0.0),
                 selected_color=(0.4, 0.4, 0.4),
                 unselected_color=(0.9, 0.9, 0.9),
                 background_opacity=1.):
        """ Single ListBox Item
        Parameters
        ----------
        list_box : :class:`ListBox`
            The ListBox reference this text belongs to.
        size : tuple of 2 ints
            The size of the listbox item.
        text_color : tuple of 3 floats
        unselected_color : tuple of 3 floats
        selected_color : tuple of 3 floats
        background_opacity : float
        """
        super(CheckBoxItem2D, self).__init__()
        self._element = None
        self.list_box = list_box
        self.background.resize(size)
        self.background_opacity = background_opacity
        self.selected = False
        self.text_color = text_color
        self.textblock.color = self.text_color
        self.selected_color = selected_color
        self.unselected_color = unselected_color
        self.background.opacity = self.background_opacity
        self.deselect()

    def _setup(self):
        """ Setup this UI component.
        Create the ListBoxItem2D with its background (Rectangle2D) and its
        label (TextBlock2D).
        """
        self.background = Rectangle2D()
        self.textblock = TextBlock2D(justification="left",
                                     vertical_justification="middle")
        self.checkbox = Checkbox()

        # Add default events listener for this UI component.
        self.add_callback(self.textblock.actor, "LeftButtonPressEvent",
                          self.left_button_clicked)
        self.add_callback(self.background.actor, "LeftButtonPressEvent",
                          self.left_button_clicked)

    def _get_actors(self):
        """ Get the actors composing this UI component.
        """
        return self.background.actors + self.textblock.actors

    def _add_to_scene(self, scene):
        """ Add all subcomponents or VTK props that compose this UI component.
        Parameters
        ----------
        scene : scene
        """
        self.background.add_to_scene(scene)
        self.textblock.add_to_scene(scene)

    def _get_size(self):
        return self.background.size

    def _set_position(self, coords):
        """ Position the lower-left corner of this UI component.
        Parameters
        ----------
        coords: (float, float)
            Absolute pixel coordinates (x, y).
        """
        self.textblock.position = coords
        # Center background underneath the text.
        position = coords
        self.background.position = (position[0],
                                    position[1] - self.background.size[1] / 2.)

    def deselect(self):
        self.background.color = self.unselected_color
        self.textblock.bold = False
        self.selected = False

    def select(self):
        self.textblock.bold = True
        self.background.color = self.selected_color
        self.selected = True

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, element):
        self._element = element
        self.textblock.message = "" if self._element is None else str(element)

    def left_button_clicked(self, i_ren, _obj, _list_box_item):
        """ A callback to handle left click for this UI element.
        Parameters
        ----------
        i_ren: :class:`CustomInteractorStyle`
        obj: :class:`vtkActor`
            The picked actor
        _list_box_item: :class:`ListBoxItem2D`
        """
        multiselect = i_ren.event.ctrl_key
        range_select = i_ren.event.shift_key
        self.list_box.select(self, multiselect, range_select)
        i_ren.force_render()

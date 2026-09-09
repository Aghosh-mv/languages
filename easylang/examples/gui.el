# GUI Example

# Create main window
print "=== Creating GUI ==="
let window = gui.createWindow("EasyLang GUI Example", 800, 600)

# Create menu bar
let menu_bar = gui.createMenuBar()
let file_menu = gui.createMenu("File")
file_menu.addItem("New", () -> print "New file")
file_menu.addItem("Open", () -> print "Open file")
file_menu.addItem("Save", () -> print "Save file")
file_menu.addSeparator()
file_menu.addItem("Exit", () -> window.close())
menu_bar.addMenu(file_menu)

let edit_menu = gui.createMenu("Edit")
edit_menu.addItem("Undo", () -> print "Undo")
edit_menu.addItem("Redo", () -> print "Redo")
edit_menu.addSeparator()
edit_menu.addItem("Cut", () -> print "Cut")
edit_menu.addItem("Copy", () -> print "Copy")
edit_menu.addItem("Paste", () -> print "Paste")
menu_bar.addMenu(edit_menu)

window.setMenuBar(menu_bar)

# Create toolbar
let toolbar = gui.createToolbar()
toolbar.addButton("New", "new_icon.png", () -> print "New")
toolbar.addButton("Open", "open_icon.png", () -> print "Open")
toolbar.addButton("Save", "save_icon.png", () -> print "Save")
window.setToolbar(toolbar)

# Create main panel
let panel = gui.createPanel()

# Create text area
let text_area = gui.createTextArea(40, 80)
text_area.setText("Hello, EasyLang GUI!")
panel.add(text_area, "center")

# Create button panel
let button_panel = gui.createPanel()
let button1 = gui.createButton("Click Me")
button1.onClick(() -> print "Button clicked!")
button_panel.add(button1)

let button2 = gui.createButton("Clear")
button2.onClick(() -> text_area.clear())
button_panel.add(button2)

panel.add(button_panel, "south")

# Create status bar
let status_bar = gui.createStatusBar()
status_bar.setText("Ready")
window.setStatusBar(status_bar)

# Create input dialog
let input_button = gui.createButton("Input Dialog")
input_button.onClick(() -> {
  let input = gui.showInputDialog("Enter your name:", "Guest")
  if input != null then
    print "Hello, " + input + "!"
    status_bar.setText("Hello, " + input)
  end
})
button_panel.add(input_button)

# Create message dialog
let message_button = gui.createButton("Message Dialog")
message_button.onClick(() -> {
  gui.showMessageDialog("This is a message box!", "Info")
})
button_panel.add(message_button)

# Create confirmation dialog
let confirm_button = gui.createButton("Confirm Dialog")
confirm_button.onClick(() -> {
  let result = gui.showConfirmDialog("Are you sure?", "Confirm")
  if result then
    print "User confirmed"
  else
    print "User cancelled"
  end
})
button_panel.add(confirm_button)

# Create file chooser
let file_button = gui.createButton("File Chooser")
file_button.onClick(() -> {
  let file = gui.showOpenDialog("Select a file")
  if file != null then
    print "Selected file: " + file
    status_bar.setText("File: " + file)
  end
})
button_panel.add(file_button)

# Create color chooser
let color_button = gui.createButton("Color Chooser")
color_button.onClick(() -> {
  let color = gui.showColorDialog()
  if color != null then
    text_area.setForegroundColor(color)
    print "Color selected: " + color
  end
})
button_panel.add(color_button)

# Create table
let table_panel = gui.createPanel()
let table = gui.createTable(["Name", "Age", "City"])
table.addRow(["Alice", 30, "New York"])
table.addRow(["Bob", 25, "San Francisco"])
table.addRow(["Charlie", 35, "Chicago"])
table_panel.add(table)

# Create tree
let tree_panel = gui.createPanel()
let tree = gui.createTree()
let root = tree.addNode("Root")
let node1 = tree.addNode(root, "Child 1")
let node2 = tree.addNode(root, "Child 2")
let node3 = tree.addNode(node1, "Grandchild 1")
tree_panel.add(tree)

# Create tabbed pane
let tabbed_pane = gui.createTabbedPane()
tabbed_pane.addTab("Table", table_panel)
tabbed_pane.addTab("Tree", tree_panel)
panel.add(tabbed_pane, "center")

# Show window
window.setVisible(true)
print "GUI created successfully"
print ""

# Event handling
print "=== Event Handling ==="

# Window close event
window.onClose(() -> {
  print "Window closing..."
  // Save any unsaved work
  // Clean up resources
  window.dispose()
})

# Key events
window.onKeyPress((key) -> {
  print "Key pressed: " + key
  status_bar.setText("Key: " + key)
})

# Mouse events
window.onMouseMove((x, y) -> {
  status_bar.setText("Mouse: " + str(x) + ", " + str(y))
})

print "Event handlers set up"
print ""

# Timer events
print "=== Timer Events ==="
let timer = gui.createTimer(1000)
timer.onTick(() -> {
  let time = datetime.now()
  status_bar.setText("Time: " + time.toString())
})
timer.start()
print "Timer started"
print ""

# Animation
print "=== Animation ==="
let animation_panel = gui.createPanel()
let label = gui.createLabel("Animation")
animation_panel.add(label)

let animation_timer = gui.createTimer(100)
let animation_step = 0
animation_timer.onTick(() -> {
  animation_step = (animation_step + 1) % 100
  let x = animation_step * 7
  let y = 50 + sin(animation_step / 10.0) * 30
  label.setPosition(x, y)
})
animation_timer.start()
print "Animation started"
print ""

# Drag and drop
print "=== Drag and Drop ==="
let drag_source = gui.createLabel("Drag me")
drag_source.setDraggable(true)
animation_panel.add(drag_source)

let drop_target = gui.createLabel("Drop here")
drop_target.setDropTarget(true)
drop_target.onDrop((data) -> {
  print "Dropped: " + data
  drop_target.setText(data)
})
animation_panel.add(drop_target)

print "Drag and drop enabled"
print ""

# Printing
print "=== Printing ==="
let print_button = gui.createButton("Print")
print_button.onClick(() -> {
  let printer = gui.createPrinter()
  printer.print(text_area.getText())
  print "Printing..."
})
button_panel.add(print_button)

print ""
print "=== GUI Example Complete ==="
print "Interact with the GUI window"

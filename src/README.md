# src

This is the source directory of Code-Generator App.

## Directories

- `assets` - includes image files
- `components` - includes Vue components
- `components/css` - includes the common css code used in components
- `metadata` - includes the data of the app in json format (Distributed/Non-distributed training values, Ignite Handlers, and Loggers)
- `templates` - includes deep learning training template scripts

### Components directory

This directory contains components - building blocks used in the Code-Generator App.

#### Components Description

The following table explains the usage of some notable components. The components that are not in the following table are self-explanatory.

| Component name                                  | Description                                                                                                             |
| :---------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------- |
| [`CodeBlock`](./components/CodeBlock.vue)       | Use for showing the code                                                                                                |
| [`Footer`](./components/Footer.vue)             | Use for footer                                                                                                          |
| [`FormCheckbox`](./components/FormCheckbox.vue) | Use for checkbox input                                                                                                  |
| [`FormInput`](./components/FormInput.vue)       | Use for text/number input                                                                                               |
| [`FormRadio`](./components/FormRadio.vue)       | Use for radio input                                                                                                     |
| [`FormSelect`](./components/FormSelect.vue)     | Use for select item input                                                                                               |
| [`Instruction`](./components/Instruction.vue)   | Use for showing how to get started                                                                                      |
| [`Message`](./components/Message.vue)           | Use for showing the status of user input event (copying code, missing configuration values when attempting to download) |
| [`NavBar`](./components/NavBar.vue)             | Use for navigation bar                                                                                                  |
| [`NavHelp`](./components/NavHelp.vue)           | Use for showing step by step guide                                                                                      |
| [`PaneLeft`](./components/PaneLeft.vue)         | Use for everything in the left pane                                                                                     |
| [`PaneRight`](./components/PaneRight.vue)       | Use for everything in the right pane                                                                                    |
| [`PaneSplit`](./components/PaneSplit.vue)       | Use for how to split the left pane, right pane, and split line                                                          |
| [`TabHandlers`](./components/TabHandlers.vue)   | Use for `Handlers` tab of the left pane                                                                                 |
| [`TabLoggers`](./components/TabLoggers.vue)     | Use for `Loggers` tab of the left pane                                                                                  |
| [`TabTemplates`](./components/TabTemplates.vue) | Use for `Templates` tab of the left pane                                                                                |
| [`TabTraining`](./components/TabTraining.vue)   | Use for `Training` tab of the left pane                                                                                 |

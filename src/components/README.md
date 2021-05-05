# components

This directory contains components - building blocks used in the Code-Generator App.

## components description

- [`CodeBlock.vue`](CodeBlock.vue) – This component is used to display the **code** with respective syntax highlightning and line numbers. This is used in [`PaneRight.vue`](PaneRight.vue).

- [`FormCheckbox.vue`](FormCheckbox.vue) – This component is used to display the **checkbox** with its respective label. This is used in [`TabHandlers.vue`](TabHandlers.vue) and [`TabTraining.vue`](TabTraining.vue).

- [`FormInput.vue`](FormInput.vue) – This component is used to display the **input box** with its respective label. This is used in [`TabHandlers.vue`](TabHandlers.vue), [`TabLoggers.vue`](TabLoggers.vue), and [`TabTraining.vue`](TabTraining.vue).

- [`FormSelect.vue`](FormSelect.vue) – This component is used to display the **select dropdown** with its respective label and options. This is used in [`TabLoggers.vue`](TabLoggers.vue) and [`TabModel.vue`](TabModel.vue).

- [`NavBar.vue`](NavBar.vue) – This component is used to display the **navigation bar (header image, name, download button, and external links)** of the app. This is used in [`App.vue`](../App.vue).

- [`PaneLeft.vue`](PaneLeft.vue) – This component is used to display the **left** pane of the app which includes tab heading and show the respective tab contents.

- [`PaneRight.vue`](PaneRight.vue) – This component is used to display the **right** pane of the app which includes tab heading and show the respective tab contents.

- [`PaneSplit.vue`](PaneSplit.vue) – This component is used to display the **main pane** of the app (excludes navigation bar) which includes the space for left pane, middle split line, and the space of right pane. It does not display any content, it occupies the space needed for left pane, split line, and right pane. And then, in the [`App.vue`](../App.vue), [`PaneLeft.vue`](PaneLeft.vue) takes up the left pane and show content. Same goes for [`PaneRight.vue`](PaneRight.vue).

- [`TabHandlers.vue`](TabHandlers.vue) – This components shows the content of **handlers** tab of the app.

- [`TabLoggers.vue`](TabLoggers.vue) – This components shows the content of **loggers** tab of the app.

- [`TabModel.vue`](TabModel.vue) – This components shows the content of **model** tab of the app.

- [`TabTraining.vue`](TabTraining.vue) – This components shows the content of **training** tab of the app.

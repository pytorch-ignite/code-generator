# [0.4.0](https://github.com/pytorch-ignite/code-generator/compare/v0.2.0...v0.4.0) (2023-09-19)

### Bug Fixes

- feat: show `txt` file extension for text files by @afzal442 in https://github.com/pytorch-ignite/code-generator/pull/179
- feat: add 404 not found page by @afzal442 in https://github.com/pytorch-ignite/code-generator/pull/178
- fix(404): navbar not cover 404 content anymore by @rwiteshbera in https://github.com/pytorch-ignite/code-generator/pull/184
- Removed idist.barrier() where needed by @sayantan1410 in https://github.com/pytorch-ignite/code-generator/pull/194
- Added configuration for local rank for all the templates by @sayantan1410 in https://github.com/pytorch-ignite/code-generator/pull/197
- Replaced torch.distributed.launch with torchrun by @sayantan1410 in https://github.com/pytorch-ignite/code-generator/pull/206
- Update ci.yml by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/220
- Fixed open in colab issue with netlify functions by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/223
- Update CI to use pnpm v7 by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/235
- Update lock file by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/236
- Fix LRScheduler issue of PyTorch by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/241
- Fix open in colab by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/263
- Improve vision classification by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/268
- replace seed 666 -> 777 by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/287
- Fix for "open in colab" opens the same zip after updates by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/295
- Changed default `log_every_iters` to 10 to stay consistent with `defaut_config` by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/299
- Try to enable "launch" for vision-classification/segmentation by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/304
- Fix bug "Open in Colab" returning "undefined" by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/305
- Fix the output_dir logic and bugs for reproducibility by @guptaaryan16 in https://github.com/pytorch-ignite/code-generator/pull/307
- Fix command errors in Nebari server run for templates by @guptaaryan16 in https://github.com/pytorch-ignite/code-generator/pull/317

### New Features

- Added Gloo as a backend option by @sayantan1410 in https://github.com/pytorch-ignite/code-generator/pull/203
- Added code structure to README and fixed remaining torch.dist.launch by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/226
- Added docker folder with Dockerfile for local development by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/237
- Added pip list to report python packages versions by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/240
- Merge common and specific code-templates by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/260
- Added optional attributes by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/264
- Updated output config file to be same as config file by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/267
- Added pyproject.toml and more code formatting and checks by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/274
- Wget option Added along with a new dropdown menu by @guptaaryan16 in https://github.com/pytorch-ignite/code-generator/pull/265
- Added Manual dataset download by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/286
- Add common template for requirements.txt in all templates by @guptaaryan16 in https://github.com/pytorch-ignite/code-generator/pull/288
- Add more options to the global config by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/289
- Change default Namespace to Omegaconf and new method to save config-lock.yaml for reproducibility by @guptaaryan16 in https://github.com/pytorch-ignite/code-generator/pull/292
- Updated UI for ArgParser options in TrainingTab.vue by @guptaaryan16 in https://github.com/pytorch-ignite/code-generator/pull/298
- Introducing Python-Fire in the Code-Generator as a config management system by @guptaaryan16 in https://github.com/pytorch-ignite/code-generator/pull/300
- Updated logger format by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/303
- Added Hydra support as an option in ArgParse UI by @guptaaryan16 in https://github.com/pytorch-ignite/code-generator/pull/302
- Added pytorch-ignite docs nav bar button by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/310
- Added "Contributors" widget and button by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/311
- PR to improve the hash function for uuid by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/312
- Introduce Nebari support in code generator by @guptaaryan16 in https://github.com/pytorch-ignite/code-generator/pull/314
- Add commit hash to the getZipUid function for PR Builds by @guptaaryan16 in https://github.com/pytorch-ignite/code-generator/pull/319

### Maintainence

- Replaced static image with gif on Home page. by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/169
- chore: add google analytics by @ydcjeff in https://github.com/pytorch-ignite/code-generator/pull/172
- ci: split workflow into several jobs, exclude launch for vision tasks by @trsvchn in https://github.com/pytorch-ignite/code-generator/pull/175
- chore: bump dev deps by @ydcjeff in https://github.com/pytorch-ignite/code-generator/pull/181
- Configure Renovate by @renovate in https://github.com/pytorch-ignite/code-generator/pull/182
- chore(deps): update all non-major dependencies by @renovate in https://github.com/pytorch-ignite/code-generator/pull/187
- chore(deps): update dependency execa to v6 by @renovate in https://github.com/pytorch-ignite/code-generator/pull/189
- chore(deps): update all non-major dependencies by @renovate in https://github.com/pytorch-ignite/code-generator/pull/188
- chore(deps): update all non-major dependencies by @renovate in https://github.com/pytorch-ignite/code-generator/pull/190
- chore(deps): update all non-major dependencies by @renovate in https://github.com/pytorch-ignite/code-generator/pull/191
- chore(deps): update all non-major dependencies by @renovate in https://github.com/pytorch-ignite/code-generator/pull/192
- chore(deps): update dependency @vitejs/plugin-vue to v2 by @renovate in https://github.com/pytorch-ignite/code-generator/pull/193
- chore(deps): update all non-major dependencies by @renovate in https://github.com/pytorch-ignite/code-generator/pull/196
- chore(deps): update all non-major dependencies by @renovate in https://github.com/pytorch-ignite/code-generator/pull/198
- chore(deps): update all non-major dependencies by @renovate in https://github.com/pytorch-ignite/code-generator/pull/200
- chore(deps): update actions/setup-node action to v3 by @renovate in https://github.com/pytorch-ignite/code-generator/pull/209
- chore(deps): update actions/checkout action to v3 by @renovate in https://github.com/pytorch-ignite/code-generator/pull/210
- chore(deps): update actions/setup-python action to v3 by @renovate in https://github.com/pytorch-ignite/code-generator/pull/211
- chore(deps): update actions/cache action to v3 by @renovate in https://github.com/pytorch-ignite/code-generator/pull/212
- fix(deps): update dependency @iconify/iconify to v3 by @renovate in https://github.com/pytorch-ignite/code-generator/pull/224
- fix(deps): update dependency start-server-and-test to v2 by @renovate in https://github.com/pytorch-ignite/code-generator/pull/229
- chore(deps): bump playwright-chromium from 1.33.0 to 1.35.1 by @dependabot in https://github.com/pytorch-ignite/code-generator/pull/255
- chore(deps): bump semver from 7.3.5 to 7.5.2 by @dependabot in https://github.com/pytorch-ignite/code-generator/pull/254
- chore(deps): bump ejs from 3.1.6 to 3.1.9 by @dependabot in https://github.com/pytorch-ignite/code-generator/pull/253
- chore(deps): bump prismjs from 1.26.0 to 1.29.0 by @dependabot in https://github.com/pytorch-ignite/code-generator/pull/245
- chore(deps): bump @vitejs/plugin-vue from 2.1.0 to 2.3.4 by @dependabot in https://github.com/pytorch-ignite/code-generator/pull/251
- Restructured config by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/243
- chore(deps): bump prettier from 2.5.1 to 2.8.8 by @dependabot in https://github.com/pytorch-ignite/code-generator/pull/259
- chore(deps): bump vue from 3.2.30 to 3.3.4 by @dependabot in https://github.com/pytorch-ignite/code-generator/pull/257
- chore(deps): bump @vue/compiler-sfc from 3.2.30 to 3.3.4 by @dependabot in https://github.com/pytorch-ignite/code-generator/pull/248
- chore(deps): bump vue-router from 4.0.12 to 4.2.2 by @dependabot in https://github.com/pytorch-ignite/code-generator/pull/250
- fix(deps): update dependency execa to v7 by @renovate in https://github.com/pytorch-ignite/code-generator/pull/228
- Updated deps and versions by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/238
- Update dependencies by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/239
- chore(deps): bump playwright-chromium from 1.35.1 to 1.37.0 by @dependabot in https://github.com/pytorch-ignite/code-generator/pull/285
- chore(deps): update actions/checkout action to v4 by @renovate in https://github.com/pytorch-ignite/code-generator/pull/318
- chore(deps): update all non-major dependencies by @renovate in https://github.com/pytorch-ignite/code-generator/pull/202
- Updated black version by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/195
- Added default backend value by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/204
- Add GHA CI autocancel by @trsvchn in https://github.com/pytorch-ignite/code-generator/pull/208
- Updated app header by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/222
- Updated readmes according to restructured config by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/266
- Removed extra line before main fn by @vfdev-5 in https://github.com/pytorch-ignite/code-generator/pull/272
- CI fix for Code generator by @guptaaryan16 in https://github.com/pytorch-ignite/code-generator/pull/283
- fix(deps): update dependency @octokit/core to v5 by @renovate in https://github.com/pytorch-ignite/code-generator/pull/277
- Refactor the code for the netlify functions by @theory-in-progress in https://github.com/pytorch-ignite/code-generator/pull/296
- fix(deps): update dependency execa to v8 by @renovate in https://github.com/pytorch-ignite/code-generator/pull/297
- Remove extra lines in setup_config for Argparser by @guptaaryan16 in https://github.com/pytorch-ignite/code-generator/pull/313
- Update template-common/config.yaml by @puhuk in https://github.com/pytorch-ignite/code-generator/pull/321

# [0.2.0](https://github.com/pytorch-ignite/code-generator/compare/v0.1.0...v0.2.0) (2021-06-25)

### Bug Fixes

- add score_function in saving best models ([#145](https://github.com/pytorch-ignite/code-generator/issues/145)) ([c349450](https://github.com/pytorch-ignite/code-generator/commit/c349450db8af7e03357d687b7d810c36221084e0))
- address comments from [#136](https://github.com/pytorch-ignite/code-generator/issues/136) ([#137](https://github.com/pytorch-ignite/code-generator/issues/137)) ([9682276](https://github.com/pytorch-ignite/code-generator/commit/96822767d0ba4595447d7de3a48b23ff93c5b447))
- bump epochs batch size to larger ones, update READMEs ([#155](https://github.com/pytorch-ignite/code-generator/issues/155)) ([2145a85](https://github.com/pytorch-ignite/code-generator/commit/2145a858ad5008da817d652a011e46487f016d29))
- change `replaceAll` to `replace` ([ee32211](https://github.com/pytorch-ignite/code-generator/commit/ee32211c4d6235eb984fc01a38f2ae721afb25db))
- change back to have previous UI ([#126](https://github.com/pytorch-ignite/code-generator/issues/126)) ([7d1e510](https://github.com/pytorch-ignite/code-generator/commit/7d1e51076d2f617c5efdec780838909b48a653b0))
- correct naming for loggers ([#149](https://github.com/pytorch-ignite/code-generator/issues/149)) ([a802644](https://github.com/pytorch-ignite/code-generator/commit/a802644402545a1c1f86fb3302686ac49e9e5bc3))
- default value in store, save on mount ([#141](https://github.com/pytorch-ignite/code-generator/issues/141)) ([d799a94](https://github.com/pytorch-ignite/code-generator/commit/d799a947df5a14768b4cc1c35fc26655d5b0b74d))
- disable clicking if no template is chosen ([#153](https://github.com/pytorch-ignite/code-generator/issues/153)) ([7a9e176](https://github.com/pytorch-ignite/code-generator/commit/7a9e176e83320bdd3042906aa45edfab16cb85a6))
- do not download VOCSegmentation by default ([#144](https://github.com/pytorch-ignite/code-generator/issues/144)) ([cff1946](https://github.com/pytorch-ignite/code-generator/commit/cff194697cba706a374a0365d7a1c5393d54e066))
- download after template, move download & colab under each left tab ([#161](https://github.com/pytorch-ignite/code-generator/issues/161)) ([0677621](https://github.com/pytorch-ignite/code-generator/commit/067762107ca6e34b794e154d26a757c545843bd3))
- empty `store.code` after changing templates ([#138](https://github.com/pytorch-ignite/code-generator/issues/138)) ([f0d3094](https://github.com/pytorch-ignite/code-generator/commit/f0d3094e65832640a13d8e34a41d8d51fc197b31)), closes [/github.com/pytorch-ignite/code-generator/pull/131#issuecomment-848225158](https://github.com//github.com/pytorch-ignite/code-generator/pull/131/issues/issuecomment-848225158)
- include pytest in requirements.txt ([#150](https://github.com/pytorch-ignite/code-generator/issues/150)) ([917867c](https://github.com/pytorch-ignite/code-generator/commit/917867c2a6aac0f4e23ac2b1b156a456b0cfa787))
- make sensible default for handlers ([#154](https://github.com/pytorch-ignite/code-generator/issues/154)) ([90b8649](https://github.com/pytorch-ignite/code-generator/commit/90b8649188e32ae8e3dd4bc6a5d0b23b96b57c45))
- make UI consistent across browsers ([#120](https://github.com/pytorch-ignite/code-generator/issues/120)) ([18298cf](https://github.com/pytorch-ignite/code-generator/commit/18298cf6ccdc7f000a1c35b9df973bf3d9de8082))
- margin 0 on mobile ([#140](https://github.com/pytorch-ignite/code-generator/issues/140)) ([bf9e534](https://github.com/pytorch-ignite/code-generator/commit/bf9e534bca2f75092559f0bf8af421a59d1f16c8))
- no alpha in message box bg, origin url in dev mode, change instruction for mobile ([#125](https://github.com/pytorch-ignite/code-generator/issues/125)) ([b662e06](https://github.com/pytorch-ignite/code-generator/commit/b662e06fa839b29eaefcd9c3e1f3ba5720eee394))
- open in colab ([#162](https://github.com/pytorch-ignite/code-generator/issues/162)) ([1564bb9](https://github.com/pytorch-ignite/code-generator/commit/1564bb99e1d5c5ff8afb3afe18dcddd2011aa5ce))
- padding-right for right-pane-tabs ([#139](https://github.com/pytorch-ignite/code-generator/issues/139)) ([3bb7d50](https://github.com/pytorch-ignite/code-generator/commit/3bb7d501c047d93962645c78c94fff6eb18c27ee))
- restructure and add more Ignite core features ([#116](https://github.com/pytorch-ignite/code-generator/issues/116)) ([7483c04](https://github.com/pytorch-ignite/code-generator/commit/7483c0483ee1fc9c4c59796562aa11308bb5a85d))
- scroll to top when navigate ([#151](https://github.com/pytorch-ignite/code-generator/issues/151)) ([ea8e4b7](https://github.com/pytorch-ignite/code-generator/commit/ea8e4b790a877bb4ad640fa3a72825d0dff3ef4b))
- set 2em instead of 2rem for hamburger icon ([fec7efd](https://github.com/pytorch-ignite/code-generator/commit/fec7efda2004b0b3c1e7e2552b393bce6de70140))
- sidebar open from right for right pane on mobile ([#143](https://github.com/pytorch-ignite/code-generator/issues/143)) ([027d036](https://github.com/pytorch-ignite/code-generator/commit/027d03653489d822550b9882b215cba43239c1f0))
- split the panes by 40/60 ([#148](https://github.com/pytorch-ignite/code-generator/issues/148)) ([04023f5](https://github.com/pytorch-ignite/code-generator/commit/04023f5a14de908ef921d3f18f54e1f724154d2f))
- whitespaces and \n(s) ([#152](https://github.com/pytorch-ignite/code-generator/issues/152)) ([7572419](https://github.com/pytorch-ignite/code-generator/commit/7572419f12fb44833a5320f67aa93fc9818bb9b5))
- **sampler:** call set_epoch every epoch start in distributed training ([#130](https://github.com/pytorch-ignite/code-generator/issues/130)) ([0c19ad2](https://github.com/pytorch-ignite/code-generator/commit/0c19ad2f6b98168bd31550ae8b635ca2401ca6cf))
- **template-segmentation:** call .step() / attach to engine ([#134](https://github.com/pytorch-ignite/code-generator/issues/134)) ([3806a38](https://github.com/pytorch-ignite/code-generator/commit/3806a380a526050673960b22ef3168de3fad03d4))

### Features

- add help for getting started steps ([#156](https://github.com/pytorch-ignite/code-generator/issues/156)) ([7834585](https://github.com/pytorch-ignite/code-generator/commit/78345853010f177c8bdf0e95c19ead55d4e3d6f7))
- add open in colab ([#160](https://github.com/pytorch-ignite/code-generator/issues/160)) ([c5d4ad8](https://github.com/pytorch-ignite/code-generator/commit/c5d4ad80719f1e183b0f0e42765ec5a03bdf9532))
- reset state when switching routes ([#158](https://github.com/pytorch-ignite/code-generator/issues/158)) ([44c2a45](https://github.com/pytorch-ignite/code-generator/commit/44c2a455291bfa979e277fd28ce183d51550a9b6))
- **template:** add dcgan template ([#119](https://github.com/pytorch-ignite/code-generator/issues/119)) ([c8cc755](https://github.com/pytorch-ignite/code-generator/commit/c8cc755a4c5be9a03a4d5801b9ec6d14186d5f1d))
- **template:** complete cifar10 classification ([#118](https://github.com/pytorch-ignite/code-generator/issues/118)) ([41e2d14](https://github.com/pytorch-ignite/code-generator/commit/41e2d14cf5b006b94fee0eb5a875e2ac7025ab60))
- **templates:** add a image segmentation template ([#129](https://github.com/pytorch-ignite/code-generator/issues/129)) ([9ca5397](https://github.com/pytorch-ignite/code-generator/commit/9ca5397c9fa1854117574ed91364fbdde51aa9d5))
- **templates:** port text classification template (WIP) ([#131](https://github.com/pytorch-ignite/code-generator/issues/131)) ([7683ede](https://github.com/pytorch-ignite/code-generator/commit/7683edeb37aae848543c0eb7870872619c986aca))
- add copy button for code ([#106](https://github.com/pytorch-ignite/code-generator/issues/106)) ([eeb3b9d](https://github.com/pytorch-ignite/code-generator/commit/eeb3b9da6c97e16c2db0b21d299cb3c12f953874))
- add error and info message box ([#121](https://github.com/pytorch-ignite/code-generator/issues/121)) ([df41cc6](https://github.com/pytorch-ignite/code-generator/commit/df41cc6e639bd748f7ae28d5b3fe764129775185))
- add file icons beside file names ([#110](https://github.com/pytorch-ignite/code-generator/issues/110)) ([db234b8](https://github.com/pytorch-ignite/code-generator/commit/db234b8f433432ace64ad22312c3bd5b52e75eff))
- add getting started instruction and loading code status ([e34da95](https://github.com/pytorch-ignite/code-generator/commit/e34da956f6aa4cd00e4752827bb0a3ca6c3c4f5a))
- add sidebar for left pane for mobile ([#108](https://github.com/pytorch-ignite/code-generator/issues/108)) ([b238b16](https://github.com/pytorch-ignite/code-generator/commit/b238b16f20fcc6145ea7c46bea1c6705eb3a7202))
- make app looks good on mobile ([#105](https://github.com/pytorch-ignite/code-generator/issues/105)) ([6fe04bc](https://github.com/pytorch-ignite/code-generator/commit/6fe04bc2e084e0f15dd86dfbac7ad0f2dce385e5))
- save the configs as config-lock.yaml ([6213893](https://github.com/pytorch-ignite/code-generator/commit/6213893a05aa61a1e1dcf98d6401c915b0ef094b))
- show git commit on nav bar ([#112](https://github.com/pytorch-ignite/code-generator/issues/112)) ([53a645f](https://github.com/pytorch-ignite/code-generator/commit/53a645fb6848314f042cfa01756aeb7136a9f7a8))
- show thanksgiving message after download ([#109](https://github.com/pytorch-ignite/code-generator/issues/109)) ([8b2e9bf](https://github.com/pytorch-ignite/code-generator/commit/8b2e9bfe55895ade1ad5c5ed5e2e6e0729dd5f04))
- template setup and render with ejs ([#111](https://github.com/pytorch-ignite/code-generator/issues/111)) ([7fc6af1](https://github.com/pytorch-ignite/code-generator/commit/7fc6af1f73ce71fdf5cd982cb322ffc996b38f14))

# [0.1.0](https://github.com/pytorch-ignite/code-generator/compare/32c8cea6dce8355764022af04b084cc597e1c5c9...v0.1.0) (2021-04-20)

### Bug Fixes

- add `/` in release badge [skip ci] ([#100](https://github.com/pytorch-ignite/code-generator/issues/100)) ([#101](https://github.com/pytorch-ignite/code-generator/issues/101)) ([873655c](https://github.com/pytorch-ignite/code-generator/commit/873655c2cc6d759ca50b7ea3b2d29c7dd55317f4))
- add test options in text classification ([#99](https://github.com/pytorch-ignite/code-generator/issues/99)) ([0b1b535](https://github.com/pytorch-ignite/code-generator/commit/0b1b5350db231a1b42cb694c8b014e5d5c02f15e))
- bump max_epochs to 5, get_handlers arguments ([#58](https://github.com/pytorch-ignite/code-generator/issues/58)) ([818585e](https://github.com/pytorch-ignite/code-generator/commit/818585e724b6dd2c05f6750a0ba9ffa4bded765c))
- convert `DEV_MODE` to int, mention in contributing.md ([#82](https://github.com/pytorch-ignite/code-generator/issues/82)) ([2342c52](https://github.com/pytorch-ignite/code-generator/commit/2342c52d6508f115bb6865a77ae322e2bfa5d1fd))
- docstring and kwargs ([#59](https://github.com/pytorch-ignite/code-generator/issues/59)) ([fefaa33](https://github.com/pytorch-ignite/code-generator/commit/fefaa33529c3e51557138864a18e6a13c4da0a95))
- download datasets on local rank 0 in multi node ([#65](https://github.com/pytorch-ignite/code-generator/issues/65)) ([e9df949](https://github.com/pytorch-ignite/code-generator/commit/e9df9497c676ad03168ba7acbaf55ab8d282445a))
- make a seed respect to distributed settings ([#60](https://github.com/pytorch-ignite/code-generator/issues/60)) ([b17397b](https://github.com/pytorch-ignite/code-generator/commit/b17397b0069cabdb97a0e08e3403ef2f9edd5130)), closes [#62](https://github.com/pytorch-ignite/code-generator/issues/62) [#64](https://github.com/pytorch-ignite/code-generator/issues/64)
- README -> \_README ([#81](https://github.com/pytorch-ignite/code-generator/issues/81)) ([d709d99](https://github.com/pytorch-ignite/code-generator/commit/d709d99f9474996739509bb16e352ed02baf748d))
- remove warning about earlystop and save best model ([#73](https://github.com/pytorch-ignite/code-generator/issues/73)) ([7a29e98](https://github.com/pytorch-ignite/code-generator/commit/7a29e98d8f4c2b6430279266373bd9bbeb8f18b9))
- **app:** show by filename, sidebar end with ignite specifics ([#54](https://github.com/pytorch-ignite/code-generator/issues/54)) ([23c87b4](https://github.com/pytorch-ignite/code-generator/commit/23c87b424f9fe846ff79a1b5da56dc22e1ef8e4f))
- **templates:** merge handlers.py into utils.py ([#55](https://github.com/pytorch-ignite/code-generator/issues/55)) ([920ac61](https://github.com/pytorch-ignite/code-generator/commit/920ac61c4af02ee112f805cc76f8781699a751ba))
- remade gan template ([#39](https://github.com/pytorch-ignite/code-generator/issues/39)) ([52f0ab0](https://github.com/pytorch-ignite/code-generator/commit/52f0ab0d81c18341ab1054ead96eb70127e6cd94))
- template file extension rename to `.py` ([#43](https://github.com/pytorch-ignite/code-generator/issues/43)) [skip ci] ([df65ca1](https://github.com/pytorch-ignite/code-generator/commit/df65ca18cdc98ded27e6c48364f602fb7d84ea20))

### Features

- **app:** add an option to include test file ([#97](https://github.com/pytorch-ignite/code-generator/issues/97)) ([a9d774b](https://github.com/pytorch-ignite/code-generator/commit/a9d774b24ea0043607f08e15facb25b20dbbd220)), closes [#94](https://github.com/pytorch-ignite/code-generator/issues/94) [#92](https://github.com/pytorch-ignite/code-generator/issues/92) [#93](https://github.com/pytorch-ignite/code-generator/issues/93)
- add ignite loggers in sidebar [wip] ([#29](https://github.com/pytorch-ignite/code-generator/issues/29)) ([78b0def](https://github.com/pytorch-ignite/code-generator/commit/78b0def0a375bc467318c7ad81f90a354f91a50b))
- allow users give project name ([#35](https://github.com/pytorch-ignite/code-generator/issues/35)) ([07b1115](https://github.com/pytorch-ignite/code-generator/commit/07b1115cc541b726839205089be0068d74355ce2))
- color output for logger and mimic `idist.show_config()` for distributed configs ([#63](https://github.com/pytorch-ignite/code-generator/issues/63)) ([c791f60](https://github.com/pytorch-ignite/code-generator/commit/c791f6021d4a47cc0ff56bbcdd43483da6716c2a))
- configurations in separate config file in single template ([#38](https://github.com/pytorch-ignite/code-generator/issues/38)) ([8d1227e](https://github.com/pytorch-ignite/code-generator/commit/8d1227e610c020d49e94b0ca30426659622d69a4))
- run evaluation for 1 epoch before training ([#57](https://github.com/pytorch-ignite/code-generator/issues/57)) ([e79bff3](https://github.com/pytorch-ignite/code-generator/commit/e79bff34da5678b14e20d17ab9ae64c3fdfcaff5))
- show directory tree after generating ([#28](https://github.com/pytorch-ignite/code-generator/issues/28)) ([9b7d661](https://github.com/pytorch-ignite/code-generator/commit/9b7d661b7c0c181543e117a337829c3930bae316))
- single model, single optimizer template ([#34](https://github.com/pytorch-ignite/code-generator/issues/34)) ([ca80e3d](https://github.com/pytorch-ignite/code-generator/commit/ca80e3d6bbdea8dd57897a91414b815d68c29862)), closes [#30](https://github.com/pytorch-ignite/code-generator/issues/30) [#32](https://github.com/pytorch-ignite/code-generator/issues/32) [#32](https://github.com/pytorch-ignite/code-generator/issues/32) [#31](https://github.com/pytorch-ignite/code-generator/issues/31)
- **app:** create a basic app ([#1](https://github.com/pytorch-ignite/code-generator/issues/1)) ([32c8cea](https://github.com/pytorch-ignite/code-generator/commit/32c8cea6dce8355764022af04b084cc597e1c5c9))
- **download:** add an option to archive and download ([#6](https://github.com/pytorch-ignite/code-generator/issues/6)) ([3f87b20](https://github.com/pytorch-ignite/code-generator/commit/3f87b201c06f1f74bb0e17bd71683fad97b6b7a1))
- **handlers:** add common training handlers template ([#26](https://github.com/pytorch-ignite/code-generator/issues/26)) ([5b2cbae](https://github.com/pytorch-ignite/code-generator/commit/5b2cbae9a15f3e15c7d4081e3ceebd048ea3bee2))
- **template:** add a gan template ([#22](https://github.com/pytorch-ignite/code-generator/issues/22)) ([9391807](https://github.com/pytorch-ignite/code-generator/commit/93918070ea4cfea8e7b80d27fd32bb5aef0ac6e3))
- **theme:** upgrade streamlit to 0.79.0, add custom theme config ([#21](https://github.com/pytorch-ignite/code-generator/issues/21)) ([e9b7de0](https://github.com/pytorch-ignite/code-generator/commit/e9b7de08589ebb2a98ca3c682e54dd81bda71a12))

### Reverts

- put version back in app ([9c10693](https://github.com/pytorch-ignite/code-generator/commit/9c10693c54cfcdce6f6f7cec0de4e3a7db492c94))

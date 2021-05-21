# [0.1.0](https://github.com/pytorch-ignite/code-generator/compare/32c8cea6dce8355764022af04b084cc597e1c5c9...v0.1.0) (2021-04-20)

### Bug Fixes

- add / in release badge [skip ci] ([#100](https://github.com/pytorch-ignite/code-generator/issues/100)) ([#101](https://github.com/pytorch-ignite/code-generator/issues/101)) ([873655c](https://github.com/pytorch-ignite/code-generator/commit/873655c2cc6d759ca50b7ea3b2d29c7dd55317f4))
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

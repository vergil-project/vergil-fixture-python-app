# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.7] - 2026-11-24

### CI

- read the automation App secrets from the automation environment (#75)

### Chores

- uv lock --upgrade
- sync the managed files with the released templates (#74)
- sync the managed files with the released templates (#79)

### Features

- the daily agent audit (#78)
- add the local subcommand and roll rich back one release in the lock (#80)

## [0.1.6] - 2026-11-23

### CI

- pass the App secrets to the shared docs workflows (#67)

### Chores

- uv lock --upgrade

### Features

- add the public subcommand and roll rich back one release in the lock (#69)

## [0.1.5] - 2026-11-23

### Chores

- uv lock --upgrade

### Features

- add the base subcommand and roll pyyaml back one release in the lock (#62)

## [0.1.4] - 2026-11-22

### CI

- stop granting actions: read to the security job (#38)

### Chores

- uv lock --upgrade

### Features

- add the bump subcommand and roll rich back one release in the lock (#39)

## [0.1.3] - 2026-11-22

### Chores

- uv lock --upgrade

### Features

- add the match subcommand and roll packaging back in uv.lock (#45)

## [0.1.2] - 2026-11-19

### CI

- pass the automation App secrets to the release (#28)

### Chores

- uv lock --upgrade

### Features

- add the latest subcommand (#33)

## [0.1.1] - 2026-11-18

### CI

- move the nightly ops cron to the 01:xx UTC hour (#12)

### Chores

- uv lock --upgrade
- sync the managed files with the released templates (#15)

### Documentation

- drop the subcommand count and note the whitespace-only greet name (#14)

### Features

- add the normalize subcommand and roll packaging back in uv.lock (#19)

## [0.1.0] - 2026-11-14

### Chores

- step 3 - vergil.toml
- step 4 - config files
- step 6 - CI/CD workflows
- step 7 - docs site

### Features

- add the CLI with greet, compare and keys subcommands, its tests and docs (#2)
- add the sort subcommand and roll rich back in uv.lock (#6)

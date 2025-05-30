Vehicle Application Learning with Eclipse Velocitas

This repository, dev_veh-app_learning, is a personal learning project focused on developing vehicle applications using Eclipse Velocitas, an open-source toolchain for creating containerized and non-containerized in-vehicle applications. It documents my journey exploring software-defined vehicle (SDV) concepts, including vehicle models, gRPC-based data brokers, and containerized app development.

About Eclipse Velocitas

Eclipse Velocitas provides a modular and scalable development toolchain for building in-vehicle applications (Vehicle Apps). It simplifies the development process by offering SDKs (e.g., Python, C++), GitHub template repositories, and integration with the Eclipse KUKSA project for vehicle abstraction via the COVESA Vehicle Signal Specification (VSS). This repository captures my experiments and learning exercises with Velocitas, including asynchronous programming, gRPC communication, and Docker-based debugging.

For more details, visit the Eclipse Velocitas Documentation or the Eclipse KUKSA Project.

Repository Structure

The repository is organized into directories, each focusing on a specific aspect of vehicle app development with Eclipse Velocitas:





async_python: Examples and exercises exploring asynchronous Python programming for Vehicle Apps, leveraging asyncio for non-blocking operations with the KUKSA Databroker.



debugging_docker: Notes and scripts for debugging Vehicle Apps in Docker containers, including setup for Velocitas' devContainer and runtime services.



flow_file: Workflow definitions (e.g., GitHub Actions) for CI/CD pipelines, inspired by Velocitas' build and release processes.



gRPC: Experiments with gRPC for communication with the KUKSA Databroker, including client implementations and service stubs.



OOP_python: Object-oriented Python code implementing vehicle models and abstractions based on the COVESA VSS standard.
Resources





Eclipse Velocitas Official Site – Overview and documentation.



Eclipse KUKSA Project – Vehicle Abstraction Layer (VAL) details.



COVESA Vehicle Signal Specification (VSS) – Standard for vehicle data models.



GitHub Template Repositories – Velocitas Python template for Vehicle Apps.

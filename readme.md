# [pydantic-ai] 🤖

![](https://img.shields.io/gitlab/pipeline-status/engineering-with-ai/python-pydantic-ai?branch=main&logo=gitlab)
![](https://gitlab.com/engineering-with-ai/python-pydantic-ai/badges/main/coverage.svg)
![](https://img.shields.io/badge/3.13.2-gray?logo=python)
![](https://img.shields.io/badge/type_checked-ty-blue)
![](https://img.shields.io/badge/0.10.9-gray?logo=uv)
![](https://img.shields.io/badge/llama-3.1-gray?logo=meta)

> template for an installable python package that use domain mcp server and api tools as well as semantic memory 

```plantuml
database domain_vector_db
database domain_graph_db
rectangle domain_mcp_server
database semantic_memory_db
rectangle agent
domain_vector_db -d- domain_mcp_server 
domain_graph_db -d- domain_mcp_server 
domain_mcp_server -d- agent
semantic_memory_db - agent
```
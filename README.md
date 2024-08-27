# *StreamGraphiti*

`StreamGraphiti` is a template-based stream processor for dynamically updating a *RDF Triplestore*.

## Features
+ An [Apache Kafka](https://kafka.apache.org/) RDF sink,
+ Compliant with the SPARQL Store Protocol,
+ SPARQL queries parametrization,
+ Dynamic URI generation,
+ Customizable *Named Graph* destination

### Built with
+ [Faust](https://github.com/faust-streaming/faust): a real-time data pipeline processor adapting *Kafka Streams* to Python (based on FastAPI)

 
### For debug
Run locally with `faust -A app.main worker`
<!-- Build with dockerfile : `docker-compose up --force-recreate --build` -->


## Usage
`stream_graphiti` is intended to be used in a small-scale application. For scalability, documentation is available with Faust and Kafka Connectors.

## Contributing
Pull requests are welcome. 
For major changes, please open an issue first to discuss what you would like to change.

## Roadmap
**Goals for v2.1** - wip


## License
Open-source project, MIT License.

## Project Status
+ **(v2.0, 27/08/2024)** RDF template package on pypi
+ **(v1.3, 21/03/2023)** Different mappers integrated
+ **(v1.2, 12/11/2022)** Dockerized version of stream-graphiti
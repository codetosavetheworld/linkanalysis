# Team QQ: Link Analysis

This project functions as the 'link analysis' subsystem in a search engine. It is built in Python and uses Neo4j to store network information. Additionally, this project utilizes the Flask framework for RESTful communication with other search engine subsystems (i.e. crawling and ranking).

## Requirements

This project requires that you have [Neo4j](https://neo4j.com/) installed and running.

Other necessary packages can be installed via pip using the command: ``` pip install -r requirements.txt ```

The requirements.txt file is located within the root directory of this project.

## Running Locally

To run locally, you must have a "Project" database instance running in Neo4j.

To run, simply type in ```python app.py```
and an instance of the project will be running on localhost:80

## Running on the VM

An instance of this project is currently running on the VM at teamqq.cs.rpi.edu. 







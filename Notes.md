# How do I start the graph
Three components:
1. Nextflow process that is running: Important to start with weblog flag
1. Server that can accept the weblog messages: Currently a FastAPI project just because
```
cd nf-cloud-studiprojekt2223/test_workflows/weblog_fastapi_project
python -m uvicorn main:app --reload
```
1. 
Start the test workflow. This was designed particulary to need different amounts of time.
```
cd nf-cloud-studiprojekt2223/test_workflows/test_tabea
../../nextflow test_tabea.nf -with-report result.log -with-trace -with-timeline timeline -with-weblog http://127.0.0.1:8000/weblog
```

## Experimental routes to build the graph
Analyse der Nachrichten:
- trace.name: Name des Prozess plus Nummer
- trace.nth_process: Wievielter Prozess in dem Knoten
- utcTime: Zeitstempel


# Overall idea
Steps to conduct
1. Find out how the weblog messages are send via the socket.io connection
    1. Which message events do I need to listen for?
1. Welche Informationen nutze ich, um den Graph aufzubauen?
    1. Wie bekomme ich den Prozess einer Ausführung?
    1. Wieviele Prozesse gibt es?
    1. Zwei Ebenen: jeden Workflow Schritt und jede Ausführung des Workflow Schritts
1. Wie triggere ich die update Funktion des Graphen im Vue Projekt?
    1. Sobald der Graph in meinem Testumfeld funktioniert, muss er in das Vue Projekt portiert werden.
    1. Zuerst Nachrichten filtern und in der Konsole loggen
    1. Danach Graph zusammenbauen und updaten
    1. Verschiedene Darstellungsmöglichkeiten: Unterschiedliche Graph-komponenten wären eine Möglichkeit (siehe Progress-Bar)
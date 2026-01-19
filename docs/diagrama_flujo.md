flowchart TD
    Start([Consulta del Usuario]) --> Planner{Razonar: Planificar Estrategia}
    
    Planner -->|Necesita Evidencia| DecideTool[Actuar: Seleccionar Herramienta]
    Planner -->|Informacion Suficiente| CheckEvidence{Tiene Evidencia de la KB?}
    
    DecideTool -->|search_kb| ToolSearch[Buscar en KB Vectorial/Keyword]
    DecideTool -->|get_doc| ToolDoc[Obtener Documento por ID]
    
    ToolSearch --> Observation[Observar: Analizar Resultados]
    ToolDoc --> Observation
    
    Observation --> EvalResults{Evaluar: Calidad y Relevancia}
    
    EvalResults -->|Score Sobre Umbral| Planner
    EvalResults -->|Score Bajo Umbral| Uncertainty[Reportar: Baja Confianza]
    EvalResults -->|Sin Resultados| NoEvidence[Reportar: Sin Evidencia]
    
    Uncertainty --> Planner
    NoEvidence --> Planner
    
    CheckEvidence -->|Si| BuildAnswer[Construir Respuesta con Citas]
    CheckEvidence -->|No| NoEvidenceAnswer[Respuesta: Sin soporte en KB]
    
    BuildAnswer --> Cite[Aplicar funcion cite]
    Cite --> Answer([Respuesta Final con Fuentes])
    
    NoEvidenceAnswer --> Answer
    
    Answer --> Stop([Fin])
    
    Planner -->|Max Iteraciones Alcanzadas| Stop
    
    style Start fill:#90EE90
    style Stop fill:#FFB6C1
    style Planner fill:#FFD700
    style DecideTool fill:#87CEEB
    style Observation fill:#DDA0DD
    style Answer fill:#98FB98
    style NoEvidence fill:#FFA07A
    style Uncertainty fill:#FFDAB9
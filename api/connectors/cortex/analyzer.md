Author : Rémi ALLAIN (rallain@cyberprotect.fr) - Cyberprotect, SDN International

# Analyzer

## Model definition

Attributes:
 - `id` (string) : Analyzer id
 - `name` (string) : Analyzer name
 - `version` (string) : Analyzer version
 - `description` (text) : Analyzer description
 - `dataTypeList` (multi-string) : List of data type this analyzer can manage
 - `cortexIds` (string) : List of Cortex server id
 
## Analyzer manipulation

### Analyzer methods

|HTTP Method |URI                                     |Action                                |
|------------|----------------------------------------|--------------------------------------|
|GET        |/api/connector/cortex/analyzer              |List all analyzers                      |
|GET        |/api/connector/cortex/analyzer/:analyzerId               |Get details of an analyzer          |
|GET        |/api/connector/cortex/analyzer/type/:dataType              |List analyzers matching the dataType                 |



# Configuration du Workflow Slack dans n8n

Ce document décrit comment configurer le workflow n8n qui sert d'interface entre Slack et la plateforme RAG.

**Emplacement du workflow dans n8n :** `slack_interface`

## 1. Créer une App Slack

Avant de commencer, vous devez créer une App Slack et obtenir les informations suivantes :
- **Bot User OAuth Token** (`SLACK_BOT_TOKEN`)
- **App-Level Token** (`SLACK_APP_TOKEN`)
- **Signing Secret** (`SLACK_SIGNING_SECRET`)

Configurez les **Slash Commands** suivantes dans votre App Slack, en les pointant vers le webhook de votre instance n8n :
- `/query`
- `/graph`
- `/ingest-url`
- `/ingest-file`

## 2. Structure du Workflow n8n

Le workflow est composé des nœuds suivants :

### Nœud 1 : Slack Trigger
- **Type :** `On a Slack command is executed`
- **Credentials :** Connectez votre compte Slack.
- **Event :** `Slash Command`

### Nœud 2 : Switch
- **Type :** `Switch`
- **Mode :** `Value`
- **Input :** `{{ $json.body.command }}`
- **Routage :**
  - **Rule 1 :** `Equals` `/query` -> Output 0
  - **Rule 2 :** `Equals` `/graph` -> Output 1
  - **Rule 3 :** `Equals` `/ingest-url` -> Output 2
  - **Rule 4 :** `Equals` `/ingest-file` -> Output 3

---

### Branche 0 & 1 : Requêtes (`/query` et `/graph`)

#### Nœud 3 : HTTP Request (Call Query Handler)
- **Connecté à :** Outputs 0 et 1 du Switch.
- **Type :** `HTTP Request`
- **Method :** `POST`
- **URL :** `http://query-handler:8000/query/`
- **Body Content Type :** `JSON`
- **Body :**
  ```json
  {
    "query": "{{ $json.body.command + ' ' + $json.body.text }}"
  }
  ```

#### Nœud 4 : Slack (Post Response)
- **Connecté à :** HTTP Request (Call Query Handler)
- **Type :** `Slack`
- **Action :** `Post to Channel`
- **Channel :** `{{ $json.body.channel_name }}`
- **Text :** `{{ $json.answer }}`

---

### Branche 2 : Ingestion d'URL (`/ingest-url`)

#### Nœud 5 : HTTP Request (Call Web Crawler)
- **Connecté à :** Output 2 du Switch.
- **Type :** `HTTP Request`
- **Method :** `POST`
- **URL :** `http://mcp-web-crawler:8001/process-url/`
- **Body Content Type :** `JSON`
- **Body :**
  ```json
  {
    "url": "{{ $json.body.text }}"
  }
  ```

#### Nœud 6 : Slack (Post Ack)
- **Connecté à :** HTTP Request (Call Web Crawler)
- **Type :** `Slack`
- **Action :** `Post to Channel`
- **Channel :** `{{ $json.body.channel_name }}`
- **Text :** `✅ Tâche d'ingestion pour l'URL {{ $json.body.text }} lancée.`

---

### Branche 3 : Ingestion de Fichier (`/ingest-file`)

*Note : Cette branche est plus complexe car elle nécessite de récupérer le fichier depuis Slack.*

#### Nœud 7 : Slack (Get File Info)
- **Connecté à :** Output 3 du Switch.
- **Type :** `Slack`
- **Action :** `Get a File`
- **File ID :** `{{ $json.body.file_id }}` *(Note: Slack doit être configuré pour envoyer cette information)*

#### Nœud 8 : HTTP Request (Download File)
- **Connecté à :** Slack (Get File Info)
- **Type :** `HTTP Request`
- **Method :** `GET`
- **URL :** `{{ $json.url_private_download }}`
- **Authentication :** `Header Auth`
- **Name :** `Authorization`
- **Value :** `Bearer {{ $credentials.SLACK_BOT_TOKEN }}`
- **Options :** `Response Format: File`

#### Nœud 9 : HTTP Request (Call Document Processor)
- **Connecté à :** HTTP Request (Download File)
- **Type :** `HTTP Request`
- **Method :** `POST`
- **URL :** `http://mcp-document-processor:8002/process-document/`
- **Body Content Type :** `Form-Data`
- **Body :**
  - **Key :** `file`
  - **Value :** `{{ $binary.data }}`
  - **Type :** `File`

#### Nœud 10 : Slack (Post Ack)
- **Connecté à :** HTTP Request (Call Document Processor)
- **Type :** `Slack`
- **Action :** `Post to Channel`
- **Channel :** `{{ $json.body.channel_name }}`
- **Text :** `✅ Tâche de traitement pour le fichier uploadé lancée.`

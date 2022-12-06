# Sovelluksen arkkitehtuuri

## Luokkadiagrammi

```mermaid
classDiagram
Database "1" -- "*" Record
```

## Sekvenssikaavio


```mermaid
sequenceDiagram
participant user
participant ui
user->>ui: ajasta laitteet klikkaamalla sopivia pylväsdiagrammeja
ui->>user: vastaa "ok"
```

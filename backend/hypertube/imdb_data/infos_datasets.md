
# https://datasets.imdbws.com

# Détails des Datasets IMDb

Ce document décrit les différents fichiers TSV disponibles dans les datasets IMDb, ainsi que les champs qu'ils contiennent.

---

## 1. `name.basics.tsv`

**Contient** : Les personnes connues dans l’industrie (acteurs, réalisateurs, scénaristes, etc.).

| Champ             | Description                                           |
|-------------------|-------------------------------------------------------|
| `nconst`          | ID IMDb unique d'une personne (ex: `nm0000001`)       |
| `primaryName`     | Nom de la personne                                    |
| `birthYear`       | Année de naissance                                    |
| `deathYear`       | Année de décès                                        |
| `primaryProfession` | Professions principales (séparées par virgule)      |
| `knownForTitles`  | Liste d'ID de films/séries notables (liens vers `title.basics.tsv`) |

---

## 2. `title.basics.tsv`

**Contient** : Les métadonnées principales de chaque film, série, épisode, court-métrage, etc.

| Champ             | Description                                           |
|-------------------|-------------------------------------------------------|
| `tconst`          | ID IMDb unique du titre (ex: `tt0000001`)             |
| `titleType`       | Type (movie, tvEpisode, short, etc.)                  |
| `primaryTitle`    | Titre affiché                                         |
| `originalTitle`   | Titre original                                        |
| `isAdult`         | Film pour adulte (0 ou 1)                             |
| `startYear`       | Année de début                                        |
| `endYear`         | Année de fin (utile pour les séries)                  |
| `runtimeMinutes`  | Durée en minutes                                      |
| `genres`          | Liste des genres (séparés par virgules)               |

---

## 3. `title.akas.tsv`

**Contient** : Les titres alternatifs par pays, langue, ou format (ex: DVD, festival...).

| Champ             | Description                                           |
|-------------------|-------------------------------------------------------|
| `titleId`         | ID du film (vers `title.basics.tsv`)                  |
| `ordering`        | Ordre d'affichage                                     |
| `title`           | Titre alternatif                                      |
| `region`          | Région d’origine                                      |
| `language`        | Langue d’origine                                      |
| `types`           | Type de variation (original, DVD, festival, etc.)     |
| `attributes`      | Infos additionnelles (ex: literal title)              |
| `isOriginalTitle` | 1 si c’est le titre original                          |

---

## 4. `title.crew.tsv`

**Contient** : Les réalisateurs et scénaristes principaux d’un film.

| Champ             | Description                                           |
|-------------------|-------------------------------------------------------|
| `tconst`          | ID du titre                                           |
| `directors`       | Liste des `nconst` des réalisateurs                   |
| `writers`         | Liste des `nconst` des scénaristes                    |

---

## 5. `title.episode.tsv`

**Contient** : Les épisodes de séries, avec liens vers la série parente.

| Champ             | Description                                           |
|-------------------|-------------------------------------------------------|
| `tconst`          | ID de l’épisode                                       |
| `parentTconst`    | ID de la série parente                                |
| `seasonNumber`    | Numéro de la saison                                   |
| `episodeNumber`   | Numéro de l’épisode                                   |

---

## 6. `title.principals.tsv`

**Contient** : Les personnes importantes associées à un titre (acteur, réalisateur, etc.).

| Champ             | Description                                           |
|-------------------|-------------------------------------------------------|
| `tconst`          | ID du titre                                           |
| `nconst`          | ID de la personne                                     |
| `category`        | Rôle (ex: actor, director, writer, self)              |
| `job`             | Métier spécifique                                     |
| `characters`      | Nom(s) du personnage (JSON string)                    |

---

## 7. `title.ratings.tsv`

**Contient** : La note moyenne IMDb et le nombre de votes pour chaque titre.

| Champ             | Description                                           |
|-------------------|-------------------------------------------------------|
| `tconst`          | ID du titre                                           |
| `averageRating`   | Note moyenne sur 10                                   |
| `numVotes`        | Nombre de votes totaux                                |

DROP TABLE IF EXISTS charts;
CREATE TABLE charts(
    chart_id TEXT PRIMARY KEY,
    music_id TEXT REFERENCES music,
    level INTEGER,
    difficulty TEXT
    jacket_path TEXT
);
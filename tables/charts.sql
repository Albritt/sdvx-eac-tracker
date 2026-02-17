CREATE TABLE charts(
    chart_id TEXT PRIMARY KEY,
    music_id TEXT REFERENCES music,
    level INT,
    difficulty TEXT
);
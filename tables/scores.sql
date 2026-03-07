DROP TABLE IF EXISTS scores;
CREATE TABLE scores(
    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_id TEXT REFERENCES charts,
    score INTEGER,
    exscore INTEGER,
    max REAL,
    medal TEXT,
    achieved_at DATE,
    clear_type TEXT
);
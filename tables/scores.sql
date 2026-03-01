DROP TABLE IF EXISTS scores;
CREATE TABLE scores(
    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_id TEXT REFERENCES charts,
    grade TEXT,
    medal TEXT,
    achieved_at DATE,
    clear_type TEXT
);
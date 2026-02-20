CREATE TABLE scores(
    score_id PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    chart_id TEXT REFERENCES charts,
    grade TEXT,
    medal TEXT,
    achieved_at DATE,
    clear_type TEXT
);
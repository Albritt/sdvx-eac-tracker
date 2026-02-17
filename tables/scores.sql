CREATE TABLE scores(
    score_id PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    chart_id TEXT(MAX) REFERENCES charts,
    grade TEXT(MAX),
    medal TEXT(MAX),
    achieved_at DATE,
    clear_type TEXT(MAX)
);
import pynecone as pc


config = pc.Config(
    app_name="library_system",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)

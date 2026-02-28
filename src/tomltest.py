import tomllib

with open("./.streamlit/secrets.toml", "rb") as f:
    file = tomllib.load(f)

# 3. Call/Access the data
a = file["cookie"]
b = file["credentials"]
print(a)
print(b)
import json, sys
from jsonschema import validate, ValidationError
def main(schema_path, data_sample_path):
  with open(schema_path) as f: schema = json.load(f)
  with open(data_sample_path) as f: sample = json.load(f)
  try:
    for rec in sample:
      validate(rec, schema)
  except ValidationError as e:
    print(f"Contract violation: {e.message}")
    sys.exit(1)
if __name__ == "__main__":
  import argparse
  p = argparse.ArgumentParser()
  p.add_argument("--schema"); p.add_argument("--data")
  a = p.parse_args()
  main(a.schema, a.data)

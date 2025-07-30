import csv, json, random, time, os
def save_to_csv(self, data, filename="output.csv"):
    if not data:
        print("保存するデータがありません。")
        return

    with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"データを保存しました: {filename}")

def save_to_json(data, filename="output.json"):
    if not data:
        print("データがありません。")
        return
    
    output_path = os.path.join("output", filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"JSONを保存しました: {filename}")

def random_delay(min_seconds=1, max_seconds=5):
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
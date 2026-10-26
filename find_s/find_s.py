
import csv

ATTRIBUTES = [
    "Sky",
    "AirTemp",
    "Humidity",
    "Wind",
    "Water",
    "Forecast"
]

def read_data():
    data = []

    with open("EnjoySport.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            example = [row[attr] for attr in ATTRIBUTES]
            label = row["EnjoySport"]
            data.append((example, label))

    return data


def find_s(data):
    hypothesis = ["Ø"] * len(ATTRIBUTES)

    print("=== FIND-S ===")

    for number, (example, label) in enumerate(data, start=1):
        if label == "Yes":
            for i in range(len(ATTRIBUTES)):
                if hypothesis[i] == "Ø":
                    hypothesis[i] = example[i]
                elif hypothesis[i] != example[i]:
                    hypothesis[i] = "?"

            print(f"Setelah contoh {number}: {hypothesis}")

    return hypothesis


def predict(hypothesis, new_day):
    for i in range(len(ATTRIBUTES)):
        if hypothesis[i] != "?" and hypothesis[i] != new_day[i]:
            return "No"

    return "Yes"


def main():
    data = read_data()

    hypothesis = find_s(data)

    print("\nHipotesis akhir:", hypothesis)

    print("\nMasukkan data hari baru.")
    new_day = []

    for attribute in ATTRIBUTES:
        value = input(attribute + ": ")
        new_day.append(value)

    result = predict(hypothesis, new_day)

    print("\nPrediksi EnjoySport:", result)


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    lines = []
    with open('output.txt', 'r') as file:
        for line in file:
            lines.append(line.strip())

    good = 0
    bad = 0
    with open('prefix_span_result.txt', 'r') as file:
        for line in file:
            if line.strip() in lines:
                good += 1
            else:
                bad += 1

    print(f"Result: {good}/{good+bad}")
    print(f"Coverage: {good}/{len(lines)}")
    if bad ==0 and good == len(lines):
        print("The results are identical!")
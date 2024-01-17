import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Example usage:\n"
              "\n"
              f"{sys.argv[0]} gsp_result.txt prefix_span_result.txt\n")
        exit()

    print(f"\nComparing {sys.argv[1]} with {sys.argv[2]}...\n")

    lines = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            lines.append(line.strip())

    good = 0
    bad = 0
    with open(sys.argv[2], 'r') as file:
        for line in file:
            if line.strip() in lines:
                good += 1
            else:
                bad += 1

    print(f"Result: {good}/{good+bad}")
    print(f"Coverage: {good}/{len(lines)}\n")
    if bad ==0 and good == len(lines):
        print("The results are identical!\n")
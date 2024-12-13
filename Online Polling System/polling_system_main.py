from polling_system import PollingSystem

def main():
    system = PollingSystem()

    # Create a new poll
    system.create_poll("What is your favorite programming language?", ["Python", "Java", "Ruby", "C++"])

    # Simulate a user voting
    print("\nVoting on poll...")
    system.vote(1, 1)  # User votes for Python (option 1)

    # View poll results
    print("\nViewing poll results...")
    system.view_poll_results(1)

    # Fetch poll and its options
    print("\nFetching the poll and its options...")
    system.get_poll(1)

    system.close()

if __name__ == "__main__":
    main()

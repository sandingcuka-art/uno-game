#!/usr/bin/env python3
import sys

def read_email(file):
    try:
        with open(file, 'r', errors='ignore') as f:
            return f.read().lower()
    except:
        print("Error: Could not read file")
        sys.exit(1)

def check_spam(text):
    # Spam keywords
    spam_words = ['viagra', 'cialis', 'lottery', 'winner', 'free', 'offer', 'cash', 'bonus']
    # Ham keywords
    ham_words = ['meeting', 'project', 'team', 'work', 'please', 'thanks']

    score = 0
    for word in spam_words:
        score += min(text.count(word), 3)  # give more weight to spam
    for word in ham_words:
        score -= min(text.count(word), 1)  # mild ham penalty

    # Extra signals
    if any(x in text for x in ['http:', 'https:', 'www.']):
        score += 2
    if text.count('!') > 2:
        score += 1

    #Lower threshold to catch more spam
    return score >= 2

def main():
    if len(sys.argv) != 2:
        print("Usage: python spam.py path/to/email.txt")
        sys.exit(1)

    email = read_email(sys.argv[1])
    print("spam" if check_spam(email) else "notspam")

if __name__ == "__main__":
    main()

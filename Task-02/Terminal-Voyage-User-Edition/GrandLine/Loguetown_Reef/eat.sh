#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage: ./eat.sh <fruit>"
    exit 1
fi

FRUIT="$1"

if [[ ! -f "$FRUIT" ]]; then
    echo "That fruit does not exist."
    exit 1
fi

if [[ -x "$FRUIT" ]]; then
    echo
    echo "------------------------------------------------------------"
    echo
    echo "*** CRUNCH! ***"
    echo
    echo "The fruit tastes absolutely terrible..."
    echo
    echo "Reality begins to fracture."
    echo
    echo "Forgotten histories rush into your mind."
    echo
    echo "You have awakened the legendary..."
    echo
    echo "          Gito Gito no Mi"
    echo
    echo "AWAKENING_SIGNATURE:"
    echo

    # Replace the ciphertext below with your encrypted flag
    echo "U2FsdGVkX1+uCmgR0ns+u4FKrvHfxhi3bbfdWOB3EpZWwcw4BFHKchR+6/rcU3Xs5EpcM88dLRI49CSbRZK5KQ==" |
    openssl enc -aes-256-cbc -a -d -pbkdf2 \
        -k "GrandLineHistory"

    echo
    echo "------------------------------------------------------------"
else
    echo
    echo "*** CRUNCH! ***"
    echo
    echo "It's just another Marine replica."
    echo "Nothing happens."
fi

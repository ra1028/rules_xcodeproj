#!/bin/bash

set -euo pipefail

root="$PWD"

echo "Updating root fixtures"
echo

bazel run --config=cache //test/fixtures:update --verbose_failures

for dir in examples/*/ ; do
    cd "$root/$dir"
    if [[ ! -f "WORKSPACE" ]]; then
      continue
    fi

    echo
    echo "Updating \"${dir%/}\" fixtures"
    echo
    bazel run --config=cache //test/fixtures:update --verbose_failures
done

#!/usr/bin/env python3
"""Fetch the normalized public GitHub profile snapshot used by future README components."""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen

LOGIN = os.environ.get("GITHUB_PROFILE_LOGIN", "themadjocker")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
OUTPUT = Path(__file__).resolve().parents[1] / "config" / "profile-data.json"

QUERY = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    login
    repositories(first:100, ownerAffiliations:OWNER, privacy:PUBLIC, isFork:false, orderBy:{field:UPDATED_AT, direction:DESC}) {
      totalCount
      nodes {
        name
        url
        description
        isArchived
        stargazerCount
        forkCount
        languages(first:100) { nodes { name } }
      }
    }
    contributionsCollection(from:$from, to:$to) {
      contributionCalendar { totalContributions }
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
    }
  }
}
"""


def request_graphql(query: str, variables: dict) -> dict:
    if not TOKEN:
        raise SystemExit("GITHUB_TOKEN or GH_TOKEN is required")
    body = json.dumps({"query": query, "variables": variables}).encode()
    request = Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "themadjocker-profile-data",
        },
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise SystemExit(json.dumps(payload["errors"], indent=2))
    return payload["data"]["user"]


def main() -> None:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0)
    window_from = generated_at - timedelta(days=365)
    user = request_graphql(
        QUERY,
        {
            "login": LOGIN,
            "from": window_from.isoformat().replace("+00:00", "Z"),
            "to": generated_at.isoformat().replace("+00:00", "Z"),
        },
    )
    repositories = user["repositories"]["nodes"]
    languages = sorted(
        {
            language["name"]
            for repository in repositories
            for language in repository["languages"]["nodes"]
            if language.get("name")
        }
    )
    contributions = user["contributionsCollection"]
    snapshot = {
        "schema_version": 1,
        "login": user["login"],
        "generated_at": generated_at.isoformat().replace("+00:00", "Z"),
        "contribution_window": {
            "from": window_from.date().isoformat(),
            "to": generated_at.date().isoformat(),
            "days": 365,
        },
        "metrics": {
            "repositories": len(repositories),
            "languages": len(languages),
            "contributions": contributions["contributionCalendar"]["totalContributions"],
            "commits": contributions["totalCommitContributions"],
            "pull_requests": contributions["totalPullRequestContributions"],
            "issues": contributions["totalIssueContributions"],
            "stars": sum(repository["stargazerCount"] for repository in repositories),
        },
        "foundation": {
            "repositories_excluding_forks": len(repositories),
            "archived_repositories": sum(1 for repository in repositories if repository["isArchived"]),
            "languages": languages,
            "repositories": [
                {
                    "name": repository["name"],
                    "url": repository["url"],
                    "description": repository["description"],
                    "is_archived": repository["isArchived"],
                    "stars": repository["stargazerCount"],
                    "forks": repository["forkCount"],
                    "languages": sorted(
                        language["name"]
                        for language in repository["languages"]["nodes"]
                        if language.get("name")
                    ),
                }
                for repository in repositories
            ],
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()

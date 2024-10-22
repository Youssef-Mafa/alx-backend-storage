#!/usr/bin/env python3
"""Module for 101-students"""


def top_students(mongo_collection):
    """returns all students sorted by average score"""
    return mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])

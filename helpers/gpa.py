from typing import Dict, List, Tuple

from helpers.gpa_points import gpa_ap_points, gpa_honors_points, gpa_standard_points
from routers.grades.types import Class, CourseWeight
from common.overridden_courses import (
    overridden_ap_courses,
    overridden_honors_courses,
    omitted_courses,
)


def calculate_gpa(
    all_marking_period_grades: List[Tuple[str, List[Class]]],
    weights: List[CourseWeight],
    manual_weights=[],
) -> Tuple[float, float]:
    manual_weights = [
        course
        for course in manual_weights
        if dict(course).get("weight", None) and dict(course).get("name", None)
    ]
    manual_weights = {
        course["name"].lower(): course["weight"] for course in manual_weights
    }

    if len(all_marking_period_grades) == 0:
        # TODO: handle this case better
        return 0, 0

    courses: List[Class] = []
    for _, marking_period_courses in all_marking_period_grades:
        courses.extend(marking_period_courses)

    course_tallied: Dict[str, List[Class]] = {}
    course_loop = []

    single_mp = len(all_marking_period_grades) == len(courses)
    if not single_mp:
        for course in courses:
            sectionId = course.sectionId
            courseId = course.courseId
            key = f"{courseId}-{sectionId}"
            try:
                course_tallied[key].append(course)
            except KeyError:
                course_tallied[key] = [course]

        course_averages = []

        for course_mps in course_tallied.values():
            course_grade_total = 0
            course_count = 0

            for course in course_mps:
                try:
                    percentage = course.grade.percentage
                    if percentage is None:
                        continue
                    percentage = float(percentage)
                    if percentage and percentage > 0:
                        course_grade_total += percentage
                        course_count += 1
                except Exception:
                    continue

            average = course_grade_total / course_count if course_count > 0 else 0
            course_mps[0].grade.percentage = average
            course_averages.append(course_mps[0])
        course_loop = course_averages
    else:
        course_loop = courses

    gpa_unweighted_total = gpa_weighted_total = excluded_courses = course_points = 0

    course_loop = [
        course
        for course in course_loop
        if course.name.lower() not in omitted_courses and course.name[0] != "*"
    ]

    for course in course_loop:
        percentage = course.grade.percentage
        percentage = round(float(percentage)) if percentage else percentage

        if percentage and percentage != 0:
            name = course.name

            # TODO: determine a better default weight
            course_weight = 1.00

            for weight in weights:
                if weight.name == name:
                    course_points += weight.weight if weight.weight else 0.00
                    if weight.weight:
                        course_weight = weight.weight

            points = gpa_standard_points(percentage)
            gpa_unweighted_total += points * course_weight

            manually_set_weight = manual_weights.get(name.lower(), None)

            if manually_set_weight == "ap":
                weighted_point = gpa_ap_points(percentage)
            elif manually_set_weight == "honors":
                weighted_point = gpa_honors_points(percentage)
            elif manually_set_weight == "unweighted":
                weighted_point = gpa_standard_points(percentage)
            else:
                if (
                    "honor" in name.lower().split()
                    or "honors" in name.lower().split()
                    or name.lower() in overridden_honors_courses
                ):
                    weighted_point = gpa_honors_points(percentage)
                elif (
                    "ap" in name.lower().split()
                    or name.lower() in overridden_ap_courses
                ):
                    weighted_point = gpa_ap_points(percentage)
                else:
                    weighted_point = gpa_standard_points(percentage)

            gpa_weighted_total += weighted_point * course_weight
        else:
            excluded_courses += 1

    divisor = (
        course_points if course_points > 0 else (len(course_loop) - excluded_courses)
    )

    final_gpa_weighted = gpa_weighted_total / divisor
    final_gpa_unweighted = gpa_unweighted_total / divisor

    return final_gpa_unweighted, final_gpa_weighted

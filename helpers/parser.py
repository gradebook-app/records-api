import re
from typing import List, Tuple
from pyquery import PyQuery as pq

from common.genesis import SchoolDistrict
from helpers.grades import number_to_letter
from routers.grades.types import Class, CourseWeight, Grade


def parse_marking_periods(html: str) -> Tuple[List[str], str]:
    content = pq(html)
    marking_period_options = content.find("select[name='fldMarkingPeriod']").children(
        "option"
    )

    marking_periods: List[str] = []
    current_marking_period: str = ""

    for i in marking_period_options:
        optionTag = pq(i)
        value = str(optionTag.attr("value"))
        if optionTag.attr("selected") == "selected":
            current_marking_period = value
        marking_periods.append(value)

    return marking_periods, current_marking_period


def parse_classes(html: str, schoolDistrict: SchoolDistrict) -> List[Class]:
    content = pq(html)

    all_classes = content.find("div.itemContainer").children("div.twoColFlex")
    classes: List[Class] = []

    for school_class in all_classes:
        raw_grade = str(
            pq(school_class).find("div.gradebookGrid div:nth-child(1) span").text()
        )

        try:
            courseIdsRaw = str(pq(school_class).attr("onclick"))
            courseIds: List[str] = re.findall("'.*'", courseIdsRaw)
            [courseId, sectionId] = courseIds[0].replace("'", "").split(",")
        except Exception:
            [courseId, sectionId] = ["", ""]

        try:
            grade = (
                int(raw_grade[:-1])
                if schoolDistrict == SchoolDistrict.SB
                else float(raw_grade[:-1])
            )
        except:
            grade = None

        class_name = str(
            pq(school_class).find("div.twoColGridItem div:nth-child(1) span").text()
        )

        raw_teacher = (
            pq(school_class).find("div.twoColGridItem div:nth-child(2) div").text()
        )
        teacher = str(raw_teacher).strip()

        grade_letter = str(
            pq(school_class)
            .find("div.gradebookGrid div:nth-child(2) div")
            .remove()
            .text()
        )

        projected = False

        if grade_letter:
            fg_text = "*PROJECTED"
            if fg_text in grade_letter:
                projected = True
            grade_letter = grade_letter.replace(fg_text, "").strip()

        if not grade_letter and grade:
            grade_letter = number_to_letter(grade)

        classes.append(
            Class(
                grade=Grade(
                    percentage=grade,
                    letter=grade_letter,
                    projected=projected,  # Doesn't work for Montgomery
                ),
                courseId=courseId,
                name=class_name,
                sectionId=sectionId,
                teacher=teacher,
            )
        )

    return classes


def parse_course_weights(html: str) -> List[CourseWeight]:
    content = pq(html)
    table = content.find("table.list")
    rows = table.children('tr:not([class="listheading"])')

    course_weights: List[CourseWeight] = []

    for row in rows:
        try:
            columns = pq(row).children("td")
            name = str(pq(columns[0]).text())
            teacher = str(pq(columns[3]).text())

            weight = str(pq(columns[-2]).text())
            weight = float(weight.strip()) if weight else None

            course_weights.append(
                CourseWeight(
                    name=name,
                    teacher=teacher,
                    weight=weight,
                )
            )
        except Exception:
            continue

    return course_weights

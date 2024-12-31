from typing import List, Tuple
from fastapi import HTTPException
import httpx
from motor.motor_asyncio import AsyncIOMotorDatabase
from pyquery import PyQuery as pq

from common.genesis import SchoolDistrict, get_genesis_config
from helpers.gpa import calculate_gpa
from helpers.parser import parse_classes, parse_course_weights, parse_marking_periods
from routers.grades.dto import WidgetContentDTO
from routers.grades.types import Class, CourseWeight, WidgetClass

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def access_granted(html: str) -> bool:
    title = str(pq(html).find("title").text())
    return not "login" in title.lower()


async def widget_content(
    token: str, userId: str, db: AsyncIOMotorDatabase
) -> WidgetContentDTO:
    schoolDistrict = SchoolDistrict("sbstudents.org")
    genesis_config = get_genesis_config(schoolDistrict)
    studentId = "10024504"

    all_marking_period_grades = await get_all_marking_period_grades(
        schoolDistrict, token, studentId
    )

    # get the classes from the ongoing marking period
    classes = all_marking_period_grades[0][1]

    grading_html = await get_grading_html(schoolDistrict, token, studentId)
    course_weights = parse_course_weights(grading_html)
    unweightedGPA, weightedGPA = calculate_gpa(
        all_marking_period_grades, course_weights
    )

    # return a simplified version of the first 4 classes
    widget_classes = [WidgetClass(grade=c.grade, name=c.name) for c in classes[:4]]

    return WidgetContentDTO(
        classes=widget_classes, unweightedGPA=unweightedGPA, weightedGPA=weightedGPA
    )


# first item in tuple is the ongoing (current) marking period
async def get_all_marking_period_grades(
    schoolDistrict: SchoolDistrict, token: str, studentId: str
) -> List[Tuple[str, List[Class]]]:
    gradebook_html = await get_gradebook_html(schoolDistrict, token, studentId)
    classes = parse_classes(gradebook_html, schoolDistrict)
    marking_periods, queried_marking_period = parse_marking_periods(gradebook_html)

    remaining_marking_periods = marking_periods.copy()
    remaining_marking_periods.remove(queried_marking_period)

    # added initially queried marking period
    all_marking_period_grades = [(queried_marking_period, classes)]
    for marking_period in remaining_marking_periods:
        if marking_period.lower().strip() == "fg":
            continue

        mp_gradebook_html = await get_gradebook_html(
            schoolDistrict, token, studentId, marking_period
        )
        mp_classes = parse_classes(mp_gradebook_html, schoolDistrict)
        all_marking_period_grades.append((marking_period, mp_classes))

    return all_marking_period_grades


async def get_gradebook_html(
    schoolDistrict: SchoolDistrict, token: str, studentId: str, marking_period: str = ""
) -> str:
    genesis_config = get_genesis_config(schoolDistrict)
    root_url = genesis_config.root
    main_route = genesis_config.main
    url = f"{root_url}{main_route}?tab1=studentdata&tab2=gradebook&tab3=weeklysummary&action=form&studentid={studentId}&mpToView={marking_period}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, cookies={"JSESSIONID": token}, headers=headers)

        if not access_granted(response.text):
            raise HTTPException(status_code=401, detail="Genesis Token Expired")

        return response.text


async def get_grading_html(
    schoolDistrict: SchoolDistrict, token: str, studentId: str
) -> str:
    genesis_config = get_genesis_config(schoolDistrict)
    root_url = genesis_config.root
    main_route = genesis_config.main
    url = f"{root_url}{main_route}?tab1=studentdata&tab2=grading&tab3=current&action=form&studentid={studentId}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, cookies={"JSESSIONID": token}, headers=headers)

        if not access_granted(response.text):
            raise HTTPException(status_code=401, detail="Genesis Token Expired")

        return response.text

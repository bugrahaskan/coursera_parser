from bs4 import BeautifulSoup
import requests
import csv
import sys
import argparse
import re

"""
Script to Collect All Data from Coursera.org into CSV File
"""


url = "https://www.coursera.org/browse"
_url = []

"""Extract Data from a Given Course Page"""
def course_page(url):
    course_result = requests.get(url=url)
    if course_result.status_code == 200:
        course_doc = BeautifulSoup(course_result.content, "html.parser")

    course_name = course_doc.find(["h1"], class_="banner-title")
    instructors = course_doc.find(["span"], class_="more-instructors")
    description = course_doc.find(["div"], class_="description")
    students = course_doc.find(text=re.compile(r'already enrolled$'))
    ratings = course_doc.find(text=re.compile(r'ratings$'))


    if course_name:
        r1 = course_name.string
        print(r1)
    else:
        r1 = "NaN"
        print(r1)
    
    if instructors:
        r2 = instructors.parent.parent.img["alt"][21:]
        print(r2)
    else:
        r2 = "NaN"
        print(r2)
    
    if description:
        r3 = description.div.string
        print(r3)
    else:
        r3 = "NaN"
        print(r3)

    try:
        if students.parent.span:
            r4 = students.parent.span.string
            print(r4)
        elif students.parent.strong.span:
            r4 = students.parent.strong.span.string
            print(r4)
    except:
        r4 = "NaN"
        print(r4)

    if ratings:
        # print it without " ratings"
        r5 = ratings[:-8]
        print(r5)
    else:
        r5 = "NaN"
        print(r5)
    
    return map(str,[r1,r2,r3,r4,r5])

"""Initialize Soup"""
def init_connect():
    result = requests.get(url)

    if result.status_code == 200:
        doc = BeautifulSoup(result.content, "html.parser")
    print(doc.title.string)

    cats = doc.find_all(["span"], class_="domain-card-name")
    for i, cat in enumerate(cats):
        print("{}. {}".format(i+1, cat.string))
        _url.append(url+"/"+"-".join(cat.string.lower().split()))
    
    return cats, _url

"""Initialize CSV File in Write Mode"""
def init_csv(title):
    file = open(title, "w", newline="")
    writer = csv.writer(file, delimiter=",")
    writer.writerow(["Category Name","Course Name","Course URL","First Instructor","Course Description","# of Students","# of Ratings"])

    return file, writer

"""Collect Data from All Courses of Coursera.org"""
def collect_all_data(title):
    cats, _url = init_connect()
    file, writer = init_csv(title)
    for cat,_ in zip(cats,_url):
        result = requests.get(_)
        if result.status_code == 200:
            doc = BeautifulSoup(result.content, "html.parser")

        course = doc.find_all("a", class_="CardText-link")
        for c in course:
            o1 = cat.string
            print(o1)
            o2 = c.string
            print(o2)
            o3 = "https://www.coursera.org"+c["href"]
            print(o3)
            r1,r2,r3,r4,r5 = course_page("https://www.coursera.org"+c["href"])
            #file.write("{};{};{};{};{};{};{};{}".format(o1,o2,o3,r1,r2,r3,r4,r5))
            writer.writerow([o1,o2,o3,r2,r3,r4,r5])
    file.close()

def collect_cat_data(num):
    title = str(args.cat)+".csv"
    cats, _url = init_connect()
    file, writer = init_csv(title)

    #print(cats[num-1].string)
    result = requests.get(_url[num-1])
    if result.status_code == 200:
            doc = BeautifulSoup(result.content, "html.parser")

    course = doc.find_all("a", class_="CardText-link")
    for c in course:
        o1 = cats[num-1].string
        print(o1)
        o2 = c.string
        print(o2)
        o3 = "https://www.coursera.org"+c["href"]
        print(o3)
        r1,r2,r3,r4,r5 = course_page("https://www.coursera.org"+c["href"])
        #file.write("{};{};{};{};{};{};{};{}".format(o1,o2,o3,r1,r2,r3,r4,r5))
        writer.writerow([o1,o2,o3,r2,r3,r4,r5])

    file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coursera.org Parser")
    parser.add_argument('--list', dest='list', type=str)
    parser.add_argument('--data', dest='data', type=str)
    parser.add_argument('--cat', dest='cat', type=int)

    args = parser.parse_args()
    if args.list == "category":
        init_connect()
    if args.data == "all":
        collect_all_data("courses.csv")
    if args.cat:
        collect_cat_data(args.cat)
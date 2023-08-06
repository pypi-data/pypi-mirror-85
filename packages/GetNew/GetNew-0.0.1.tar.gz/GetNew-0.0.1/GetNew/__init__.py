# -*-coding:utf-8-*-

import requests


class GetNew:
    def __init__(self):
        pass

    def getNew(self) -> bool:
        return True

    def getPython(self) -> str:
        url = "https://www.python.org/downloads/"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63", }
        data = {}
        session = requests.Session()
        result = session.get(url=url, headers=headers)
        session.close()
        status = ""
        try:
            status = \
                result.text.split("Download the latest version for Windows")[1].split("download-buttons")[1].split(
                    "<a")[
                    1].split("\">")[1].split("</")[0].split("Download ")[1]
        except Exception as error:
            status = error
        finally:
            return status

    def getJavaSE(self) -> str:
        url = "https://www.oracle.com/java/technologies/javase-downloads.html"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63", }
        data = {}
        session = requests.Session()
        result = session.get(url=url, headers=headers)
        session.close()
        status = ""
        try:
            status = result.text.split("is the latest release for the Java SE Platform")[0].split(">\r\n\t\t\t\t")[
                -1]
        except Exception as error:
            status = error
        finally:
            return status

    def getIDEA(self) -> str:
        url = "https://www.jetbrains.com/idea/download/"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63", }
        data = {}
        session = requests.Session()
        result = session.get(url=url, headers=headers)
        session.close()
        status = ""
        try:
            status = result.text.split("is the latest release for the Java SE Platform")[0].split(">\r\n\t\t\t\t")[
                -1]
        except Exception as error:
            status = error
        finally:
            return status


class TestGetNew:

    def testGetPython(self) -> str:
        url = "https://www.python.org/downloads/"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63", }
        data = {}
        session = requests.Session()
        result = session.get(url=url, headers=headers)
        session.close()
        return result.text

    def testGetJavaSE(self) -> str:
        url = "https://www.oracle.com/java/technologies/javase-downloads.html"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63", }
        data = {}
        session = requests.Session()
        result = session.get(url=url, headers=headers)
        session.close()
        return result.text

    def testGetIDEA(self) -> str:
        url = "https://www.jetbrains.com/idea/download/"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63", }
        data = {}
        session = requests.Session()
        result = session.get(url=url, headers=headers)
        session.close()
        return result.text


if __name__ == "__main__":
    # Create New Test Class
    # Return HTML Source Code
    testGetNew = TestGetNew()

    # Create New GetNew Class
    # Return Latest Version
    getNew = GetNew()

    # Get Python
    # testGetPython = testGetNew.testGetPython()
    # print(testGetPython)
    # getPython = getNew.getPython()
    # print(getPython)

    # Get JavaSE
    # testGetJavaSE = testGetNew.testGetJavaSE()
    # print(testGetJavaSE)
    # getJavaSE = getNew.getJavaSE()
    # print(getJavaSE)

    # Get IDEA
    testGetIDEA = testGetNew.testGetIDEA()
    print(testGetIDEA)
    # getIDEA = getNew.getIDEA()
    # print(getIDEA)

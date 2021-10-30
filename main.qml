import QtQuick 2.9
import QtQuick.Window 2.3

Window {
    id: applicationWindow
    visible: true
    width: 1280
    height: 800
    flags: Qt.FramelessWindowHint | Qt.Window
    color: "transparent"

    property QtObject backend

    property string current_date: "[Date Placeholder]"
    property string current_time: "[Time Placeholder]"
    property string current_monthyear: "[MonthYear Placeholder]"

    Connections {
        target: backend

        function onCurrentDate(msg) {
            current_date = msg;
        }
        function onCurrentTime(msg) {
            current_time = msg;
        }
        function onCurrentMonthYear(msg) {
            current_monthyear = msg;
        }
    }

    Rectangle {
        id: applicationWindowBackground
        color: "#171D22"
        anchors.fill: parent
        radius: 35

        MouseArea {
            anchors.fill: parent
            onClicked: {
                Qt.quit()
            }
        }

        Rectangle {
            id: mainContentBackground
            width: applicationWindow.width * 0.78
            height: applicationWindow.height
            color: "#333c47"
            anchors.left: applicationWindowBackground.left
            anchors.top: applicationWindowBackground.top
            radius: 35

            Rectangle {
                id: leftOverviewPane
                width: applicationWindow.width * 0.19
                height: applicationWindow.height - 44
                color: "#444f60"
                anchors.left: mainContentBackground.left
                anchors.top: mainContentBackground.top
                anchors.leftMargin: 22
                anchors.topMargin: 22
                radius: 25

                Text {
                    id: overviewPaneDateText

                    text: current_date

                    color: "lightgrey"
                    font.family: "Century Gothic"
                    font.pixelSize: 14
                    font.bold: true

                    anchors.horizontalCenter: leftOverviewPane.horizontalCenter
                    anchors.top: leftOverviewPane.top
                    anchors.topMargin: 40
                }

                Text {
                    id: overviewPaneTimeText

                    text: current_time

                    color: "white"
                    font.family: "Century Gothic"
                    font.pixelSize: 32
                    font.bold: true

                    anchors.horizontalCenter: leftOverviewPane.horizontalCenter
                    anchors.top: overviewPaneDateText.bottom
                    anchors.topMargin: 4
                }

                Text {
                    id: overviewPaneMonthYearText

                    text: current_monthyear

                    color: "darkgrey"
                    font.family: "Century Gothic"
                    font.pixelSize: 14
                    font.bold: true

                    anchors.horizontalCenter: leftOverviewPane.horizontalCenter
                    anchors.top: overviewPaneTimeText.bottom
                    anchors.topMargin: 4
                }
            }
        }
    }
}
